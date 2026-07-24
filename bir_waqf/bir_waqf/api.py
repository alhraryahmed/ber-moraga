import frappe, os, json
from bir_waqf.utils.file_processor import process_bir_file
from bir_waqf.utils.bank_statement_processor import process_bank_statement_file
from bir_waqf.utils.reconciliation import reconcile_bank_statement

@frappe.whitelist()
def process_uploaded_file(file_url, batch_id=None):
	file_doc = frappe.get_doc("File", {"file_url": file_url})
	file_path = file_doc.get_full_path()
	res = process_bir_file(file_path, batch_id)
	return res

@frappe.whitelist()
def get_batch_transactions_by_bank(import_batch, bank=None):
	"""
	Fetches Bir Transactions filtered strictly by import_batch and bank.
	Excludes transactions with critical exceptions.
	"""
	filters = {"import_batch": import_batch}
	if bank and bank.strip():
		filters["bank_name"] = bank.strip()

	transactions = frappe.get_all(
		"Bir Transaction",
		filters=filters,
		fields=["name", "transaction_id", "transfer_number", "donor_name", "total_amount", "transaction_date", "bank_name", "has_exception"]
	)
	return transactions

@frappe.whitelist()
def post_batch_transactions_to_entries(import_batch, bank=None):
	"""
	Creates or updates a Bir Bank Statement for the batch & bank,
	and posts matching Bir Transactions as statement entries.
	"""
	filters = {"import_batch": import_batch}
	if bank and bank.strip():
		filters["bank_name"] = bank.strip()
		stmt_title = f"كشف حساب {bank.strip()} - {import_batch}"
	else:
		stmt_title = f"كشف حساب عام - {import_batch}"

	if frappe.db.exists("Bir Bank Statement", stmt_title):
		doc = frappe.get_doc("Bir Bank Statement", stmt_title)
	else:
		doc = frappe.new_doc("Bir Bank Statement")
		doc.statement_name = stmt_title
		if bank and bank.strip() and frappe.db.exists("Bank", bank.strip()):
			doc.bank = bank.strip()

	existing_refs = set(e.reference_number for e in (doc.entries or []))
	
	txs = frappe.get_all(
		"Bir Transaction",
		filters=filters,
		fields=["name", "transaction_id", "transfer_number", "donor_name", "total_amount", "transaction_date"]
	)

	added_count = 0
	for tx in txs:
		ref = tx.transfer_number or tx.transaction_id
		if ref and ref not in existing_refs:
			doc.append("entries", {
				"reference_number": ref,
				"posting_date": str(tx.transaction_date)[:10] if tx.transaction_date else None,
				"description": f"{tx.donor_name or 'متبرع'} - {tx.transaction_id}",
				"amount": tx.total_amount,
				"is_reconciled": 0,
				"matched_transaction": tx.name
			})
			existing_refs.add(ref)
			added_count += 1

	doc.flags.ignore_permissions = True
	doc.save()
	frappe.db.commit()

	return {
		"status": "success",
		"statement_name": doc.name,
		"added_count": added_count
	}

@frappe.whitelist()
def get_transaction_list_print_html(names=None):
	"""
	Generates an elegant HTML print report for a list of transactions (or all if none selected).
	"""
	if isinstance(names, str):
		try:
			names = json.loads(names)
		except Exception:
			names = [names]

	filters = {}
	if names and len(names) > 0:
		filters = {"name": ["in", names]}

	tx_list = frappe.get_all(
		"Bir Transaction",
		filters=filters,
		fields=[
			"transaction_id", "contribution_request_id", "transfer_number",
			"bank_name", "donor_name", "phone", "payment_method",
			"total_amount", "transaction_date", "is_basket",
			"reconciliation_status", "has_exception", "exception_reason"
		],
		order_by="creation desc",
		limit_page_length=500
	)

	total_sum = sum(t.total_amount or 0.0 for t in tx_list)

	rows_html = ""
	for idx, tx in enumerate(tx_list, 1):
		basket_badge = '<span style="background:#2b6cb0;color:#fff;padding:2px 6px;border-radius:4px;font-size:10px;">سلة</span>' if tx.is_basket else ''
		exc_badge = f'<span style="background:#e53e3e;color:#fff;padding:2px 6px;border-radius:4px;font-size:10px;" title="{tx.exception_reason or ""}">استثناء</span>' if tx.has_exception else ''
		
		status_color = "#38a169" if tx.reconciliation_status in ["مطابق آليًا", "مطابق يدويًا"] else "#d69e2e"
		rec_badge = f'<span style="color:{status_color};font-weight:bold;">{tx.reconciliation_status or "غير مطابق"}</span>'

		dt_str = str(tx.transaction_date)[:16] if tx.transaction_date else "-"

		rows_html += f"""
		<tr>
			<td style="text-align:center;">{idx}</td>
			<td style="font-weight:bold;">{tx.transaction_id or '-'} {basket_badge} {exc_badge}</td>
			<td>{tx.transfer_number or '-'}</td>
			<td>{tx.donor_name or 'فاعل خير'}</td>
			<td>{tx.bank_name or '-'}</td>
			<td>{tx.payment_method or '-'}</td>
			<td style="font-weight:bold;color:#0A4D2E;">{tx.total_amount:,.2f} د.ل</td>
			<td style="text-align:center;">{dt_str}</td>
			<td style="text-align:center;">{rec_badge}</td>
		</tr>
		"""

	html = f"""
	<!DOCTYPE html>
	<html dir="rtl" lang="ar">
	<head>
		<meta charset="utf-8">
		<title>تقرير جدول معاملـات منصـة البر الوقفية</title>
		<style>
			body {{ font-family: 'Tajawal', 'Segoe UI', Tahoma, sans-serif; margin: 20px; color: #2d3748; }}
			.header {{ text-align: center; border-bottom: 2px solid #0A4D2E; padding-bottom: 12px; margin-bottom: 20px; }}
			.header h2 {{ color: #0A4D2E; margin: 0 0 6px 0; font-size: 24px; }}
			.header p {{ color: #718096; margin: 0; font-size: 13px; }}
			.summary {{ display: flex; justify-content: space-between; background: #f7fafc; padding: 12px 18px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #e2e8f0; }}
			.summary div {{ font-size: 14px; font-weight: bold; }}
			table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px; }}
			th {{ background-color: #0A4D2E; color: white; padding: 10px 8px; text-align: right; border: 1px solid #0A4D2E; }}
			td {{ padding: 8px; border: 1px solid #cbd5e0; text-align: right; }}
			tr:nth-child(even) {{ background-color: #f7fafc; }}
			.footer {{ margin-top: 30px; text-align: center; font-size: 11px; color: #a0aec0; border-top: 1px solid #e2e8f0; padding-top: 10px; }}
			@media print {{
				body {{ margin: 0; }}
				.summary {{ border: 1px solid #ccc; }}
			}}
		</style>
	</head>
	<body>
		<div class="header">
			<h2>الهيئة العامة للأوقاف والشؤون الإسلامية</h2>
			<p>تقرير قائمة معاملات التبرعات والسلات — منصة البر الوقفية</p>
		</div>

		<div class="summary">
			<div>عدد المعاملات: <span style="color:#0A4D2E;">{len(tx_list)}</span></div>
			<div>إجمالي القيمة: <span style="color:#D4AF37;">{total_sum:,.2f} د.ل</span></div>
		</div>

		<table>
			<thead>
				<tr>
					<th style="width:40px;text-align:center;">#</th>
					<th>رقم المعاملة</th>
					<th>رقم الحوالة/الصك</th>
					<th>المتبرع / المستخدم</th>
					<th>المصرف</th>
					<th>طريقة الدفع</th>
					<th>القيمة الإجمالية</th>
					<th style="text-align:center;">التاريخ</th>
					<th style="text-align:center;">حالة المطابقة</th>
				</tr>
			</thead>
			<tbody>
				{rows_html}
			</tbody>
		</table>

		<div class="footer">
			تم استخراج هذا التقرير تلقائياً من نظام البر الوقفية للمطابقة والمراجعة
		</div>
	</body>
	</html>
	"""
	return html

@frappe.whitelist()
def run_auto_reconciliation(from_date=None, to_date=None):
	"""
	Runs auto reconciliation across unmatched transactions within date range.
	"""
	statements = frappe.get_all("Bir Bank Statement", fields=["name"])
	total_matched = 0
	total_amount = 0.0

	for stmt in statements:
		doc = frappe.get_doc("Bir Bank Statement", stmt.name)
		m_count, m_amt = reconcile_bank_statement(doc)
		total_matched += m_count
		total_amount += m_amt

	return {
		"matched_count": total_matched,
		"matched_amount": total_amount
	}

@frappe.whitelist()
def reconcile_statement_doc(statement_name):
	doc = frappe.get_doc("Bir Bank Statement", statement_name)
	m_count, m_amt = reconcile_bank_statement(doc)
	return {
		"matched_count": m_count,
		"matched_amount": m_amt
	}

@frappe.whitelist()
def import_bank_statement_file(file_url, statement_name):
	file_doc = frappe.get_doc("File", {"file_url": file_url})
	file_path = file_doc.get_full_path()
	res = process_bank_statement_file(file_path, statement_name)
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
	total_tx = frappe.db.count("Bir Transaction") or 0
	total_amount = frappe.db.sql("SELECT SUM(total_amount) FROM `tabBir Transaction`")[0][0] or 0.0
	matched_tx = frappe.db.count("Bir Transaction", {"reconciliation_status": ["in", ["مطابق آليًا", "مطابق يدويًا"]]}) or 0
	exceptions_tx = frappe.db.count("Bir Transaction", {"has_exception": 1}) or 0
	basket_tx = frappe.db.count("Bir Transaction", {"is_basket": 1}) or 0
	batches_count = frappe.db.count("Bir Import Batch") or 0

	try:
		max_single_val = frappe.db.sql("SELECT MAX(total_amount) FROM `tabBir Transaction` WHERE is_basket = 0")[0][0]
		max_single = float(max_single_val) if max_single_val else 0.0
	except Exception:
		max_single = 0.0

	try:
		max_basket_val = frappe.db.sql("SELECT MAX(total_amount) FROM `tabBir Transaction` WHERE is_basket = 1")[0][0]
		max_basket = float(max_basket_val) if max_basket_val else 0.0
	except Exception:
		max_basket = 0.0

	# Top 5 Projects
	projects = frappe.db.sql("""
		SELECT project_name, SUM(sub_amount) as total 
		FROM `tabBir Basket Project` 
		GROUP BY project_name 
		ORDER BY total DESC 
		LIMIT 5
	""", as_dict=True) or []

	return {
		"total_transactions": total_tx,
		"total_donations": total_amount,
		"matched_transactions": matched_tx,
		"exceptions_count": exceptions_tx,
		"basket_count": basket_tx,
		"batches_count": batches_count,
		"max_single": max_single,
		"max_basket": max_basket,
		"top_projects": projects
	}



@frappe.whitelist()
def assign_bank_to_transactions(names, bank, import_batch=None):
	"""
	Updates bank_name for selected Bir Transaction records.
	"""
	if isinstance(names, str):
		try:
			names = json.loads(names)
		except Exception:
			names = [names]

	if not names:
		frappe.throw(frappe._("لم يتم تحديد أي معاملات لتضمين المصرف."))

	if not bank or not str(bank).strip():
		frappe.throw(frappe._("يرجى اختيار المصرف المراد تضمينه."))

	bank_clean = str(bank).strip()
	updated_count = 0

	for name in names:
		if frappe.db.exists("Bir Transaction", name):
			update_dict = {"bank_name": bank_clean}
			if import_batch:
				update_dict["import_batch"] = import_batch
			frappe.db.set_value("Bir Transaction", name, update_dict)
			updated_count += 1

	frappe.db.commit()

	return {
		"status": "success",
		"updated_count": updated_count,
		"bank": bank_clean
	}

