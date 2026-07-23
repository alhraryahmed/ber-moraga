import frappe, os
from bir_waqf.utils.file_processor import process_bir_file

@frappe.whitelist()
def process_uploaded_file(file_url):
	file_doc = frappe.get_doc("File", {"file_url": file_url})
	file_path = file_doc.get_full_path()
	res = process_bir_file(file_path)
	return res

@frappe.whitelist()
def manual_reconcile(transaction_id, reference_number):
	if frappe.db.exists("Bir Transaction", transaction_id):
		frappe.db.set_value("Bir Transaction", transaction_id, {
			"reconciliation_status": "مطابق يدويًا",
			"has_exception": 0,
			"transfer_number": reference_number
		})
		frappe.db.commit()
		return {"status": "success"}
	return {"status": "error", "message": "المعاملة غير موجودة"}

@frappe.whitelist()
def get_dashboard_stats():
	total_tx = frappe.db.count("Bir Transaction")
	total_amount = frappe.db.sql("SELECT SUM(total_amount) FROM `tabBir Transaction`")[0][0] or 0.0
	matched_tx = frappe.db.count("Bir Transaction", {"reconciliation_status": ["in", ["مطابق آليًا", "مطابق يدويًا"]]})
	exceptions_tx = frappe.db.count("Bir Transaction", {"has_exception": 1})
	basket_tx = frappe.db.count("Bir Transaction", {"is_basket": 1})
	
	projects = frappe.db.sql("""
		SELECT project_name, SUM(sub_amount) as total 
		FROM `tabBir Basket Project` 
		GROUP BY project_name 
		ORDER BY total DESC 
		LIMIT 5
	""", as_dict=True)
	
	return {
		"total_transactions": total_tx,
		"total_donations": total_amount,
		"matched_transactions": matched_tx,
		"exceptions_count": exceptions_tx,
		"basket_count": basket_tx,
		"top_projects": projects
	}
