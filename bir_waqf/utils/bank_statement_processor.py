import frappe, os, re
import pandas as pd

def process_bank_statement_file(file_path, statement_name):
	if file_path.endswith('.csv'):
		try:
			df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig')
		except Exception:
			df = pd.read_csv(file_path, encoding='utf-8-sig')
	else:
		df = pd.read_excel(file_path)
		
	df.columns = [str(c).strip() for c in df.columns]
	
	doc = frappe.get_doc("Bir Bank Statement", statement_name)
	added = 0
	
	for idx, row in df.iterrows():
		ref_no = row.get('رقم الحوالة') or row.get('رقم المرجع') or row.get('المرجع') or row.get('رقم الصك')
		dt = row.get('تاريخ القيد') or row.get('التاريخ')
		desc = row.get('البيان') or row.get('الوصف') or row.get('البيان / الوصف')
		amt = row.get('المبلغ') or row.get('القيمة') or row.get('المبلغ د.ل')
		
		if pd.isna(ref_no) or not str(ref_no).strip():
			continue
			
		ref_str = str(ref_no).strip()
		amt_val = 0.0
		if not pd.isna(amt):
			try:
				amt_val = float(re.sub(r'[^0-9.]', '', str(amt)))
			except Exception:
				amt_val = 0.0
				
		dt_val = None
		if not pd.isna(dt):
			try:
				dt_val = pd.to_datetime(str(dt)).strftime('%Y-%m-%d')
			except Exception:
				dt_val = None
				
		doc.append("entries", {
			"reference_number": ref_str,
			"posting_date": dt_val,
			"description": str(desc) if not pd.isna(desc) else "قيد مصرفي",
			"amount": amt_val,
			"is_reconciled": 0
		})
		added += 1
		
	doc.flags.ignore_permissions = True
	doc.save()
	frappe.db.commit()
	return {"count": added}
