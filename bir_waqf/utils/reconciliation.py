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
	doc.save()
	frappe.db.commit()
	return matched

def fetch_tx_for_statement(statement_name, import_batch=None, from_date=None, to_date=None):
	doc = frappe.get_doc("Bir Bank Statement", statement_name)
	filters = {"reconciliation_status": "غير مطابق"}
	
	if import_batch:
		filters["import_batch"] = import_batch
	if doc.bank:
		filters["bank_name"] = doc.bank
	if from_date and to_date:
		filters["transaction_date"] = ["between", [from_date, to_date]]
		
	txs = frappe.get_all("Bir Transaction", filters=filters, fields=["name", "transfer_number", "total_amount"])
	matched = 0
	
	for tx in txs:
		if not tx.transfer_number:
			continue
		for entry in doc.entries:
			if not entry.is_reconciled and entry.reference_number == tx.transfer_number and abs(entry.amount - tx.total_amount) < 0.05:
				entry.is_reconciled = 1
				entry.matched_transaction = tx.name
				matched += 1
				frappe.db.set_value("Bir Transaction", tx.name, {
					"reconciliation_status": "مطابق آليًا",
					"has_exception": 0
				})
				break
				
	doc.save()
	frappe.db.commit()
	return {"matched_count": matched, "total_scanned": len(txs)}

def post_txs_to_statement(tx_names, statement_name, import_batch=None):
	doc = frappe.get_doc("Bir Bank Statement", statement_name)
	
	if import_batch and not tx_names:
		txs = frappe.get_all("Bir Transaction", filters={"import_batch": import_batch, "reconciliation_status": "غير مطابق"}, fields=["name"])
		tx_names = [t.name for t in txs]

	matched = 0
	for name in tx_names:
		tx = frappe.get_doc("Bir Transaction", name)
		if not tx.transfer_number:
			continue
		for entry in doc.entries:
			if not entry.is_reconciled and entry.reference_number == tx.transfer_number and abs(entry.amount - tx.total_amount) < 0.05:
				entry.is_reconciled = 1
				entry.matched_transaction = tx.name
				matched += 1
				frappe.db.set_value("Bir Transaction", tx.name, {
					"reconciliation_status": "مطابق يدويًا",
					"has_exception": 0
				})
				break
				
	doc.save()
	frappe.db.commit()
	return {"posted_count": len(tx_names), "matched_count": matched}

def bulk_reconcile_by_date_and_bank(from_date=None, to_date=None, bank=None):
	filters = {"reconciliation_status": "غير مطابق"}
	if bank:
		filters["bank_name"] = bank
	if from_date and to_date:
		filters["transaction_date"] = ["between", [from_date, to_date]]

	unmatched_txs = frappe.get_all("Bir Transaction", filters=filters, fields=["name", "transfer_number", "total_amount"])
	matched_count = 0
	total_matched_amount = 0.0

	for tx in unmatched_txs:
		if not tx.transfer_number:
			continue
		entry_name = frappe.db.get_value("Bir Bank Statement Entry", {
			"reference_number": tx.transfer_number,
			"amount": tx.total_amount,
			"is_reconciled": 0
		}, "name")
		
		if entry_name:
			frappe.db.set_value("Bir Transaction", tx.name, {
				"reconciliation_status": "مطابق آليًا",
				"has_exception": 0
			})
			frappe.db.set_value("Bir Bank Statement Entry", entry_name, {
				"is_reconciled": 1,
				"matched_transaction": tx.name
			})
			matched_count += 1
			total_matched_amount += tx.total_amount

	frappe.db.commit()
	return {
		"matched_count": matched_count,
		"matched_amount": total_matched_amount
	}
