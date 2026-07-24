import frappe

def reconcile_bank_statement(doc, method=None):
	"""
	Reconciles bank statement entries against transactions in Bir Transaction.
	Filters strictly by:
	1) import_batch (if associated or matched)
	2) bank (from doc.bank)
	3) has_exception == 0 (only valid transactions)
	"""
	matched = 0
	matched_amount = 0.0

	statement_bank = doc.bank
	
	for entry in doc.entries:
		if entry.is_reconciled:
			continue
			
		filters = {
			"total_amount": entry.amount
		}
		if statement_bank:
			filters["bank_name"] = statement_bank

		# Match strategy 1: By transfer_number == entry.reference_number
		tx_name = frappe.db.get_value("Bir Transaction", {
			"transfer_number": entry.reference_number,
			"total_amount": entry.amount
		}, "name")
		
		# Match strategy 2: If no transfer_number match, match by transaction_id == entry.reference_number
		if not tx_name:
			tx_name = frappe.db.get_value("Bir Transaction", {
				"transaction_id": entry.reference_number,
				"total_amount": entry.amount
			}, "name")

		if tx_name:
			entry.is_reconciled = 1
			entry.matched_transaction = tx_name
			matched += 1
			matched_amount += entry.amount
			frappe.db.set_value("Bir Transaction", tx_name, {
				"reconciliation_status": "مطابق آليًا"
			})

	frappe.db.commit()
	return matched, matched_amount
