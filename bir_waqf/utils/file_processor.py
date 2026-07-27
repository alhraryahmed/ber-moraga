import frappe, os, re, json
import pandas as pd
from frappe.utils import nowdate, getdate, now_datetime
from bir_waqf.utils.project_utils import get_or_create_project

def parse_project_line(line):
	"""
	Extracts project_name and sub_amount from a single line.
	Line format example: 'مشروع استكمال مسجد الإمام الشافعي بمنطقة أبوسليم بمدينة (طرابلس) (100)'
	Also handles trailing quotes like: 'مشروع حفر بئر (50)"'
	"""
	if not line or pd.isna(line):
		return None
	text = str(line).strip().strip('"').strip("'")
	if not text:
		return None
		
	match = re.search(r'^(.*?)(?:\s*\(([-+]?[0-9]*\.?[0-9]+)\))?"?\s*$', text)
	if match:
		p_name = match.group(1).strip().strip('"').strip("'")
		sub_amt = float(match.group(2)) if match.group(2) else 0.0
		if not p_name:
			p_name = text
		return {"project_name": p_name, "sub_amount": sub_amt}
	return {"project_name": text, "sub_amount": 0.0}

def parse_multi_projects(proj_raw):
	"""
	Parses Pattern A (multi-line inside single cell) or single line project string.
	"""
	if not proj_raw or pd.isna(proj_raw):
		return []
	text = str(proj_raw).strip()
	if not text:
		return []
	lines = text.split('\n')
	projects = []
	for line in lines:
		item = parse_project_line(line)
		if item:
			projects.append(item)
	return projects

def is_numeric_tx_id(val):
	if pd.isna(val):
		return False
	s = str(val).strip()
	if not s:
		return False
	try:
		f = float(s)
		return f > 0 and s.replace('.', '').isdigit()
	except Exception:
		return False

def clean_str(val):
	if pd.isna(val):
		return ""
	s = str(val).strip()
	if s.lower() == 'nan' or s == 'none' or s == '-':
		return ""
	return s

def process_bir_file(file_path, batch_id=None):
	"""
	Processes Bir Waqf Excel (.xlsx) or CSV (.csv) file.
	Supports Pattern A (multi-line in 1 cell) and Pattern B (scattered multi-row).
	"""
	if file_path.endswith('.csv'):
		sep = ';'
		try:
			with open(file_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
				first_line = f.readline()
				if first_line.count(',') > first_line.count(';'):
					sep = ','
		except Exception:
			sep = ';'
			
		try:
			df = pd.read_csv(file_path, sep=sep, encoding='utf-8-sig', dtype=str)
		except Exception:
			df = pd.read_csv(file_path, encoding='utf-8-sig', dtype=str)
		is_excel = False
	else:
		df = pd.read_excel(file_path, dtype=str)
		is_excel = True

	df.columns = [str(c).strip() for c in df.columns]

	if not batch_id:
		batch_doc = frappe.new_doc("Bir Import Batch")
		batch_doc.file_name = os.path.basename(file_path)
		batch_doc.import_date = now_datetime()
		batch_doc.save(ignore_permissions=True)
		batch_id = batch_doc.name
	else:
		batch_doc = frappe.get_doc("Bir Import Batch", batch_id)

	transactions = []
	current_basket = None
	missing_id_counter = 1

	for idx, row in df.iterrows():
		row_dict = {str(k).strip(): clean_str(v) for k, v in row.items()}
		
		tx_id_raw = row_dict.get('رقم المعاملة')
		req_id_raw = row_dict.get('رقم طلب المساهمة')
		transfer_no_raw = row_dict.get('رقم الحوالة/الصك')
		bank_raw = row_dict.get('مصرف')
		proj_raw = row_dict.get('المشاريع')
		donor_raw = row_dict.get('المستخدم')
		phone_raw = row_dict.get('الهاتف')
		pay_method_raw = row_dict.get('طريقة الدفع')
		val_raw = row_dict.get('القيمة')
		date_raw = row_dict.get('تاريخ المعاملة')
		status_raw = row_dict.get('حالة المعاملة') or 'مكتمل'
		if status_raw not in ['مكتمل', 'معلق', 'ملغى']:
			status_raw = 'مكتمل'

		has_valid_id = is_numeric_tx_id(tx_id_raw)

		if current_basket:
			if has_valid_id and not donor_raw and not val_raw and not date_raw:
				current_basket['has_exception'] = True
				current_basket['exception_reasons'].append("سلة غير مكتملة الإغلاق (صف إغلاق مفقود).")
				transactions.append(current_basket)
				current_basket = None
			elif has_valid_id and (donor_raw or val_raw or date_raw):
				current_basket['has_exception'] = True
				current_basket['exception_reasons'].append("سلة غير مكتملة الإغلاق (تلتها معاملة مستقلة).")
				transactions.append(current_basket)
				current_basket = None

		if current_basket:
			proj_text = proj_raw or (tx_id_raw if not has_valid_id else '')
			if proj_text:
				sub_projs = parse_multi_projects(proj_text)
				current_basket['projects'].extend(sub_projs)
				
			for col_name, cell_val in row_dict.items():
				if not cell_val:
					continue
				if not current_basket['phone'] and (cell_val.startswith('218') or cell_val.startswith('219')):
					current_basket['phone'] = cell_val
				elif not current_basket['donor_name'] and col_name in ['المستخدم', 'طريقة الدفع', 'المشاريع'] and not cell_val.replace('.','').isdigit():
					if '(' in cell_val and ')' in cell_val and not cell_val.endswith(')'):
						current_basket['donor_name'] = cell_val
					elif col_name == 'المستخدم':
						current_basket['donor_name'] = cell_val
				elif current_basket['total_amount'] == 0.0 and col_name in ['القيمة', 'المشاريع']:
					try:
						v = float(re.sub(r'[^0-9.]', '', cell_val))
						if v > 0:
							current_basket['total_amount'] = v
					except Exception:
						pass
				elif not current_basket['transaction_date'] and col_name in ['تاريخ المعاملة', 'طريقة الدفع']:
					if '/' in cell_val or '-' in cell_val:
						current_basket['transaction_date'] = cell_val
				elif not current_basket['payment_method'] and col_name in ['طريقة الدفع', 'نوع الرسوم']:
					if cell_val in ['بطاقة مسبوقة الدفع', 'تحويل مصرفي', 'سداد', 'تداول', 'ادفع لي']:
						current_basket['payment_method'] = cell_val

			if donor_raw or val_raw or date_raw:
				if not current_basket['donor_name'] and donor_raw:
					current_basket['donor_name'] = donor_raw
				if val_raw:
					try:
						current_basket['total_amount'] = float(re.sub(r'[^0-9.]', '', val_raw))
					except Exception:
						pass
				if date_raw:
					current_basket['transaction_date'] = date_raw

				transactions.append(current_basket)
				current_basket = None
			continue

		if has_valid_id:
			clean_tx_id = str(int(float(tx_id_raw)))
			if not donor_raw and not val_raw and not date_raw:
				first_projs = parse_multi_projects(proj_raw)
				current_basket = {
					'transaction_id': clean_tx_id,
					'contribution_request_id': clean_str(req_id_raw),
					'transfer_number': clean_str(transfer_no_raw),
					'bank_name': clean_str(bank_raw) if is_excel else '',
					'projects': first_projs,
					'donor_name': '',
					'phone': '',
					'payment_method': '',
					'total_amount': 0.0,
					'transaction_date': None,
					'transaction_status': status_raw,
					'has_exception': False,
					'exception_reasons': []
				}
				continue
			else:
				projs = parse_multi_projects(proj_raw)
				tot_amt = 0.0
				if val_raw:
					try:
						tot_amt = float(re.sub(r'[^0-9.]', '', val_raw))
					except Exception:
						tot_amt = 0.0

				tx_obj = {
					'transaction_id': clean_tx_id,
					'contribution_request_id': clean_str(req_id_raw),
					'transfer_number': clean_str(transfer_no_raw),
					'bank_name': clean_str(bank_raw) if is_excel else '',
					'projects': projs,
					'donor_name': donor_raw,
					'phone': phone_raw,
					'payment_method': pay_method_raw,
					'total_amount': tot_amt,
					'transaction_date': date_raw,
					'transaction_status': status_raw,
					'has_exception': False,
					'exception_reasons': []
				}
				transactions.append(tx_obj)
		else:
			projs = parse_multi_projects(proj_raw or tx_id_raw)
			if not projs and not donor_raw and not val_raw:
				continue

			tot_amt = 0.0
			if val_raw:
				try:
					tot_amt = float(re.sub(r'[^0-9.]', '', val_raw))
				except Exception:
					tot_amt = 0.0

			temp_id = f"MISSING-TX-{missing_id_counter:05d}"
			missing_id_counter += 1

			tx_obj = {
				'transaction_id': temp_id,
				'is_missing_id': True,
				'contribution_request_id': clean_str(req_id_raw),
				'transfer_number': clean_str(transfer_no_raw),
				'bank_name': clean_str(bank_raw) if is_excel else '',
				'projects': projs,
				'donor_name': donor_raw,
				'phone': phone_raw,
				'payment_method': pay_method_raw,
				'total_amount': tot_amt,
				'transaction_date': date_raw,
				'transaction_status': status_raw,
				'has_exception': True,
				'exception_reasons': ["رقم المعاملة مفقود من المصدر."]
			}
			transactions.append(tx_obj)

	if current_basket:
		current_basket['has_exception'] = True
		current_basket['exception_reasons'].append("سلة غير مكتملة الإغلاق بنهاية الملف.")
		transactions.append(current_basket)

	created_count = 0
	basket_count = 0
	exceptions_count = 0
	total_donations_sum = 0.0

	for item in transactions:
		sub_sum = sum(p['sub_amount'] for p in item['projects'])
		is_basket = len(item['projects']) > 1
		if is_basket:
			basket_count += 1

		has_exception = item['has_exception']
		reasons = list(item['exception_reasons'])

		if item['total_amount'] <= 0:
			if sub_sum > 0:
				item['total_amount'] = sub_sum
			else:
				has_exception = True
				reasons.append("القيمة الإجمالية مفقودة.")

		if is_basket and abs(sub_sum - item['total_amount']) > 0.05:
			has_exception = True
			reasons.append(f"اختلاف في إجمالي السلة: المجموع الفرعي ({sub_sum}) لا يساوي الإجمالي ({item['total_amount']}).")

		if not item['transfer_number']:
			has_exception = True
			reasons.append("رقم الحوالة/الصك مفقود (بانتظار المطابقة المصرفية).")

		if has_exception:
			exceptions_count += 1

		total_donations_sum += item['total_amount']

		tx_id = item['transaction_id']

		if frappe.db.exists("Bir Transaction", tx_id):
			doc = frappe.get_doc("Bir Transaction", tx_id)
		else:
			doc = frappe.new_doc("Bir Transaction")
			doc.transaction_id = tx_id

		doc.import_batch = batch_id
		doc.contribution_request_id = item['contribution_request_id']
		doc.transfer_number = item['transfer_number']
		doc.bank_name = item['bank_name'] or "غير محدد"
		doc.donor_name = item['donor_name'] or "فاعل خير"
		doc.phone = item['phone']
		doc.payment_method = item['payment_method'] or "تحويل مصرفي"
		doc.total_amount = item['total_amount']
		
		# Validate transaction_status option
		st = item['transaction_status']
		if st not in ['مكتمل', 'معلق', 'ملغى']:
			st = 'مكتمل'
		doc.transaction_status = st

		doc.is_basket = 1 if is_basket else 0
		doc.basket_items_count = len(item['projects'])
		doc.has_exception = 1 if has_exception else 0
		doc.exception_reason = " ".join(reasons).strip()

		# Datetime parsing fix
		doc.transaction_date = None
		if item['transaction_date']:
			dt_str = str(item['transaction_date']).strip()
			if dt_str and dt_str != '-':
				try:
					if '/' in dt_str:
						parts = dt_str.split(' ')
						d_parts = parts[0].split('/')
						if len(d_parts) == 3:
							formatted_dt = f"{d_parts[2]}-{int(d_parts[1]):02d}-{int(d_parts[0]):02d}"
							if len(parts) > 1:
								formatted_dt += f" {parts[1]}:00"
							doc.transaction_date = formatted_dt
					else:
						doc.transaction_date = dt_str
				except Exception:
					doc.transaction_date = None

		doc.set("basket_projects", [])
		for p in item['projects']:
			proj_name = p['project_name']
			proj_link = get_or_create_project(proj_name)
			doc.append("basket_projects", {
				"project_name": proj_link or proj_name,
				"sub_amount": p['sub_amount']
			})

		if not is_basket and item['projects']:
			doc.project = get_or_create_project(item['projects'][0]['project_name'])

		doc.flags.ignore_permissions = True
		doc.save()
		created_count += 1

	batch_doc.total_transactions = created_count
	batch_doc.basket_transactions = basket_count
	batch_doc.total_donations = total_donations_sum
	batch_doc.save(ignore_permissions=True)

	frappe.db.commit()

	return {
		"batch_id": batch_id,
		"total_transactions": created_count,
		"basket_transactions": basket_count,
		"exceptions_count": exceptions_count,
		"total_donations": total_donations_sum
	}
