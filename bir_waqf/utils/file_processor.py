import frappe, os, re, json
import pandas as pd
from frappe.utils import now_datetime

def extract_project_name_and_amount(project_str):
	if not project_str or pd.isna(project_str):
		return "", 0.0
	text = str(project_str).strip().strip('"\'')
	if text == '-' or not text:
		return "", 0.0

	match = re.search(r'^(.*?)(?:\s*\(([-+]?[0-9]*\.?[0-9]+)\))?$', text)
	if match:
		p_name = match.group(1).strip().strip('"\'')
		sub_amt = float(match.group(2)) if match.group(2) else 0.0
		if not p_name or p_name == '-':
			return "", 0.0
		return p_name, sub_amt
	return text, 0.0

def process_bir_file(file_path, file_name=None):
	if not file_name:
		file_name = os.path.basename(file_path)
		
	if file_path.endswith('.csv'):
		try:
			df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig')
		except Exception:
			df = pd.read_csv(file_path, encoding='utf-8-sig')
	else:
		df = pd.read_excel(file_path)
	
	df.columns = [str(c).strip() for c in df.columns]
	
	transactions = {}
	current_tx_id = None
	
	for idx, row in df.iterrows():
		tx_id = row.get('رقم المعاملة')
		req_id = row.get('رقم طلب المساهمة')
		transfer_no = row.get('رقم الحوالة/الصك')
		bank = row.get('مصرف') or row.get('طريقة الدفع') or 'مصرف الوقف'
		proj_raw = row.get('المشاريع')
		donor = row.get('المستخدم')
		phone = row.get('الهاتف')
		pay_method = row.get('طريقة الدفع')
		val = row.get('القيمة')
		dt = row.get('تاريخ المعاملة')
		tx_status = row.get('حالة المعاملة') or 'مكتمل'
		
		valid_tx_id = None
		if not pd.isna(tx_id) and str(tx_id).strip().isdigit():
			valid_tx_id = str(int(float(tx_id)))
		
		if valid_tx_id:
			current_tx_id = valid_tx_id
			if current_tx_id not in transactions:
				transactions[current_tx_id] = {
					'transaction_id': current_tx_id,
					'contribution_request_id': '',
					'transfer_number': '',
					'bank_name': 'مصرف الوقف',
					'projects': [],
					'donor_name': '',
					'phone': '',
					'payment_method': '',
					'raw_total_val': 0.0,
					'transaction_date': None,
					'transaction_status': 'مكتمل'
				}
		
		target_id = valid_tx_id or current_tx_id
		if not target_id or target_id not in transactions:
			continue
		
		tx_data = transactions[target_id]
		
		if not pd.isna(req_id) and str(req_id).replace('.','').isdigit():
			tx_data['contribution_request_id'] = str(int(float(req_id)))
			
		if not pd.isna(transfer_no) and str(transfer_no).strip() and str(transfer_no).strip() != '-':
			tx_data['transfer_number'] = str(transfer_no).strip()
			
		if not pd.isna(bank) and str(bank).strip() and str(bank).strip() != '-':
			tx_data['bank_name'] = str(bank).strip()
		
		if not pd.isna(proj_raw):
			p_name, s_amt = extract_project_name_and_amount(proj_raw)
			if p_name and p_name != '-':
				tx_data['projects'].append({'project_name': p_name, 'sub_amount': s_amt})
		
		if not pd.isna(donor) and str(donor).strip() and str(donor).strip() != '-' and not str(donor).startswith('('):
			tx_data['donor_name'] = str(donor).strip()
			
		if not pd.isna(phone) and str(phone).strip() and str(phone).strip() != '-':
			p_str = str(phone).strip()
			if p_str.startswith('218') or p_str.startswith('09') or len(p_str) >= 8:
				tx_data['phone'] = p_str
				
		if not pd.isna(pay_method) and str(pay_method).strip() and str(pay_method).strip() != '-':
			tx_data['payment_method'] = str(pay_method).strip()
			
		if not pd.isna(val):
			try:
				clean_val = float(re.sub(r'[^0-9.]', '', str(val)))
				if clean_val > tx_data['raw_total_val']:
					tx_data['raw_total_val'] = clean_val
			except Exception:
				pass
			
		if not pd.isna(dt) and str(dt).strip() and str(dt).strip() != '-':
			dt_str = str(dt).strip()
			if len(dt_str) >= 10:
				tx_data['transaction_date'] = dt_str

	created_count = 0
	exceptions_count = 0
	basket_count = 0
	total_donations_sum = 0.0
	
	# Create Import Batch Document
	batch_doc = frappe.new_doc("Bir Import Batch")
	batch_doc.file_name = file_name
	batch_doc.import_date = now_datetime()
	batch_doc.flags.ignore_permissions = True
	batch_doc.insert()
	
	for tx_id, item in transactions.items():
		is_basket = len(item['projects']) > 1
		if is_basket: 
			basket_count += 1
			calculated_total = sum(p['sub_amount'] for p in item['projects'])
			item['total_amount'] = calculated_total if calculated_total > 0 else item['raw_total_val']
		else:
			item['total_amount'] = item['raw_total_val']
			if len(item['projects']) == 1 and item['projects'][0]['sub_amount'] == 0:
				item['projects'][0]['sub_amount'] = item['total_amount']
		
		total_donations_sum += item['total_amount']
		
		has_exception = False
		reason = ""
		
		if not item['transfer_number']:
			has_exception = True
			reason += "رقم الحوالة/الصك مفقود. "
			
		if item['total_amount'] <= 0:
			has_exception = True
			reason += "القيمة الإجمالية غير محددة أو صفرية. "
			
		if has_exception:
			exceptions_count += 1

		if frappe.db.exists("Bir Transaction", tx_id):
			doc = frappe.get_doc("Bir Transaction", tx_id)
		else:
			doc = frappe.new_doc("Bir Transaction")
			doc.transaction_id = tx_id
			
		doc.contribution_request_id = item['contribution_request_id']
		doc.transfer_number = item['transfer_number']
		doc.bank_name = item['bank_name']
		doc.donor_name = item['donor_name'] or "فاعل خير"
		doc.phone = item['phone']
		doc.payment_method = item['payment_method'] or "تحويل مصرفي"
		doc.total_amount = item['total_amount']
		doc.transaction_status = item['transaction_status']
		doc.import_batch = batch_doc.name
		
		if item['transaction_date']:
			try:
				doc.transaction_date = pd.to_datetime(item['transaction_date']).strftime('%Y-%m-%d %H:%M:%S')
			except Exception:
				doc.transaction_date = None
		else:
			doc.transaction_date = None

		doc.is_basket = 1 if is_basket else 0
		doc.basket_items_count = len(item['projects'])
		doc.has_exception = 1 if has_exception else 0
		doc.exception_reason = reason.strip()
		
		doc.set("basket_projects", [])
		for p in item['projects']:
			if p['project_name'] and p['project_name'] != '-':
				doc.append("basket_projects", {
					"project_name": p['project_name'],
					"sub_amount": p['sub_amount']
				})
			
		doc.flags.ignore_permissions = True
		doc.save()
		created_count += 1
		
	# Update batch summary
	batch_doc.total_transactions = created_count
	batch_doc.basket_transactions = basket_count
	batch_doc.total_donations = total_donations_sum
	batch_doc.exceptions_count = exceptions_count
	batch_doc.save()

	frappe.db.commit()
	
	return {
		"batch_id": batch_doc.name,
		"file_name": file_name,
		"total_transactions": created_count,
		"basket_transactions": basket_count,
		"total_donations": total_donations_sum,
		"exceptions_count": exceptions_count
	}
