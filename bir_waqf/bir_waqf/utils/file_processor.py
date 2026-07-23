import frappe, os, re, json
import pandas as pd
from frappe.utils import nowdate, getdate

def parse_sub_project_amount(project_str):
	if not project_str or pd.isna(project_str):
		return "", 0.0
	text = str(project_str).strip()
	match = re.search(r'^(.*?)(?:\s*\(([-+]?[0-9]*\.?[0-9]+)\))?$', text)
	if match:
		p_name = match.group(1).strip()
		sub_amt = float(match.group(2)) if match.group(2) else 0.0
		return p_name, sub_amt
	return text, 0.0

def process_bir_file(file_path):
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
					'contribution_request_id': str(int(float(req_id))) if not pd.isna(req_id) and str(req_id).replace('.','').isdigit() else '',
					'transfer_number': str(transfer_no).strip() if not pd.isna(transfer_no) else '',
					'bank_name': str(bank).strip() if not pd.isna(bank) else 'مصرف الوقف',
					'projects': [],
					'donor_name': '',
					'phone': '',
					'payment_method': '',
					'total_amount': 0.0,
					'transaction_date': None,
					'transaction_status': 'مكتمل'
				}
		
		target_id = valid_tx_id or current_tx_id
		if not target_id or target_id not in transactions:
			continue
		
		tx_data = transactions[target_id]
		
		if not pd.isna(proj_raw):
			p_name, s_amt = parse_sub_project_amount(proj_raw)
			if p_name:
				tx_data['projects'].append({'project_name': p_name, 'sub_amount': s_amt})
		
		if not pd.isna(donor) and str(donor).strip() and not str(donor).startswith('('):
			tx_data['donor_name'] = str(donor).strip()
		if not pd.isna(phone) and str(phone).strip():
			tx_data['phone'] = str(phone).strip()
		if not pd.isna(pay_method) and str(pay_method).strip():
			tx_data['payment_method'] = str(pay_method).strip()
		if not pd.isna(val) and float(val) > 0:
			tx_data['total_amount'] = float(val)
		if not pd.isna(dt):
			tx_data['transaction_date'] = str(dt)
		if not pd.isna(tx_status) and str(tx_status).strip() in ['مكتمل', 'معلق', 'ملغى']:
			tx_data['transaction_status'] = str(tx_status).strip()

	created_count = 0
	exceptions_count = 0
	basket_count = 0
	
	for tx_id, item in transactions.items():
		sub_sum = sum(p['sub_amount'] for p in item['projects'])
		is_basket = len(item['projects']) > 1
		if is_basket: basket_count += 1
		
		has_exception = False
		reason = ""
		
		if not item['transfer_number']:
			has_exception = True
			reason += "رقم الحوالة/الصك مفقود. "
			
		if item['total_amount'] <= 0:
			item['total_amount'] = sub_sum
			
		if is_basket and abs(sub_sum - item['total_amount']) > 0.05:
			has_exception = True
			reason += f"اختلاف في إجمالي السلة: المجموع الفرعي ({sub_sum}) لا يساوي الإجمالي ({item['total_amount']}). "
			
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
		doc.is_basket = 1 if is_basket else 0
		doc.basket_items_count = len(item['projects'])
		doc.has_exception = 1 if has_exception else 0
		doc.exception_reason = reason.strip()
		
		doc.set("basket_projects", [])
		for p in item['projects']:
			doc.append("basket_projects", {
				"project_name": p['project_name'],
				"sub_amount": p['sub_amount']
			})
			
		doc.flags.ignore_permissions = True
		doc.save()
		created_count += 1
		
	frappe.db.commit()
	
	return {
		"total_transactions": created_count,
		"basket_transactions": basket_count,
		"exceptions_count": exceptions_count
	}
