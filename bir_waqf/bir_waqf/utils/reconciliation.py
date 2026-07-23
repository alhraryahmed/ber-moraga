import frappe

def reconcile_bank_statement(doc, method=None):
	matched = 0
	for entry in doc.entries:
		if entry.is_reconciled:
			continue
		tx_name = frappe.db.get_value("Bir Transaction", {
			"transfer_number": entry.reference_number,
			"total_amount": entry.amount
		}, "name")
		
		if tx_name:
			entry.is_reconciled = 1
			entry.matched_transaction = tx_name
			matched += 1
			frappe.db.set_value("Bir Transaction", tx_name, {
				"reconciliation_status": "مطابق آليًا",
				"has_exception": 0
			})
	frappe.msgprint(f"تمت المطابقة الآلية بنجاح لـ {matched} عملية مصرفية.")
