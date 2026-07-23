import frappe, os, json
from bir_waqf.utils.file_processor import process_bir_file
from bir_waqf.utils.reconciliation import (
	reconcile_bank_statement, 
	bulk_reconcile_by_date_and_bank,
	fetch_tx_for_statement,
	post_txs_to_statement
)
from bir_waqf.utils.bank_statement_processor import process_bank_statement_file

@frappe.whitelist()
def process_uploaded_file(file_url):
	file_doc = frappe.get_doc("File", {"file_url": file_url})
	file_path = file_doc.get_full_path()
	res = process_bir_file(file_path, file_doc.file_name)
	return res

@frappe.whitelist()
def import_bank_statement_file(file_url, statement_name):
	file_doc = frappe.get_doc("File", {"file_url": file_url})
	file_path = file_doc.get_full_path()
	res = process_bank_statement_file(file_path, statement_name)
	return res

@frappe.whitelist()
def get_batch_transactions(import_batch):
	txs = frappe.get_all("Bir Transaction", filters={"import_batch": import_batch}, fields=[
		"name", "transaction_id", "transfer_number", "total_amount", "transaction_date", "donor_name", "bank_name"
	])
	return txs

@frappe.whitelist()
def post_batch_transactions_to_entries(import_batch, statement_name=None):
	txs = frappe.get_all("Bir Transaction", filters={"import_batch": import_batch}, fields=[
		"name", "transaction_id", "transfer_number", "total_amount", "transaction_date", "donor_name", "bank_name"
	])
	
	if not txs:
		return {"status": "error", "message": "لا توجد معاملات تابعة لدفعة الاستيراد المحددة"}
		
	if not statement_name:
		st_title = f"كشف حساب دفعة {import_batch}"
		if frappe.db.exists("Bir Bank Statement", st_title):
			doc = frappe.get_doc("Bir Bank Statement", st_title)
		else:
			doc = frappe.new_doc("Bir Bank Statement")
			doc.statement_name = st_title
			doc.bank = txs[0].get("bank_name") if txs[0].get("bank_name") and frappe.db.exists("Bank", txs[0].get("bank_name")) else None
			doc.flags.ignore_permissions = True
			doc.insert()
			statement_name = doc.name
	else:
		doc = frappe.get_doc("Bir Bank Statement", statement_name)
		
	added = 0
	existing_refs = [e.reference_number for e in doc.entries]
	
	for tx in txs:
		ref = tx.transfer_number or tx.transaction_id
		if ref in existing_refs:
			continue
		doc.append("entries", {
			"reference_number": ref,
			"posting_date": tx.transaction_date,
			"description": f"{tx.donor_name or 'متبرع'} - {tx.transaction_id}",
			"amount": tx.total_amount,
			"is_reconciled": 0,
			"matched_transaction": tx.name
		})
		added += 1
		
	doc.flags.ignore_permissions = True
	doc.save()
	frappe.db.commit()
	return {"status": "success", "statement_name": doc.name, "added_count": added}

@frappe.whitelist()
def get_transaction_list_print_html(names=None, import_batch=None):
	parsed_names = []
	if names is not None:
		if isinstance(names, (int, str)):
			s_val = str(names).strip()
			if s_val.startswith('[') and s_val.endswith(']'):
				try:
					parsed_names = [str(x) for x in json.loads(s_val)]
				except Exception:
					parsed_names = [s_val]
			else:
				parsed_names = [s_val]
		elif isinstance(names, (tuple, list)):
			parsed_names = [str(n) for n in names]
			
	where_clause = ""
	if parsed_names and len(parsed_names) > 0:
		quoted = ["'%s'" % str(n).replace("'", "") for n in parsed_names]
		where_clause = f"WHERE name IN ({','.join(quoted)})"
	elif import_batch:
		clean_batch = str(import_batch).replace("'", "")
		where_clause = f"WHERE import_batch = '{clean_batch}'"
		
	query = f"""
		SELECT 
			transaction_id, donor_name, contribution_request_id, transfer_number, bank_name,
			total_amount, transaction_date, transaction_status, reconciliation_status,
			is_basket, has_exception, import_batch
		FROM `tabBir Transaction`
		{where_clause}
		ORDER BY modified DESC
	"""
	rows = frappe.db.sql(query, as_dict=True)
	
	total_sum = sum(r['total_amount'] or 0 for r in rows)
	total_count = len(rows)
	
	html_table_rows = ""
	for idx, r in enumerate(rows, 1):
		amount_str = f"ل.د {r['total_amount']:,.2f}" if r['total_amount'] else "—"
		dt_str = r['transaction_date'].strftime('%d-%m-%Y %H:%M:%S') if r['transaction_date'] else "—"
		basket_badge = "<span style='color:#1C6B3F;font-weight:bold;'>سلة</span>" if r['is_basket'] else "مفرد"
		exc_badge = "<span style='color:#A03A3A;font-weight:bold;'>استثناء</span>" if r['has_exception'] else "سليم"
		
		html_table_rows += f"""
		<tr>
			<td>{idx}</td>
			<td><b>{r['transaction_id']}</b></td>
			<td>{r['donor_name'] or 'فاعل خير'}</td>
			<td>{r['contribution_request_id'] or '—'}</td>
			<td>{r['transfer_number'] or '—'}</td>
			<td>{r['bank_name'] or '—'}</td>
			<td style='font-weight:bold; color:#0B3D2E;'>{amount_str}</td>
			<td>{dt_str}</td>
			<td>{r['transaction_status'] or 'مكتمل'}</td>
			<td>{r['reconciliation_status'] or 'غير مطابق'}</td>
			<td>{basket_badge}</td>
			<td>{exc_badge}</td>
		</tr>
		"""
		
	full_html = f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="utf-8">
<title>تقرير قائمة معاملات منصة البر الوقفية</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Tajawal:wght@400;600;700;800&display=swap');

body {{
  direction: rtl;
  font-family: 'Tajawal', sans-serif;
  color: #1C2B24;
  background: #fff;
  margin: 0;
  padding: 15mm;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}}

.report-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 3px solid #C6A15B;
  padding-bottom: 15px;
  margin-bottom: 20px;
}}
.brand-title {{
  font-family: 'Amiri', serif;
  font-size: 24px;
  font-weight: 700;
  color: #0B3D2E;
}}
.brand-sub {{
  font-size: 13px;
  color: #5C6B63;
}}
.report-meta {{
  text-align: left;
  font-size: 12px;
  color: #5C6B63;
}}

.summary-cards {{
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  background: #FAF7F0;
  padding: 12px 20px;
  border-radius: 8px;
  border: 1px solid #D9CFB8;
}}
.card-item {{
  flex: 1;
  text-align: center;
}}
.card-label {{
  font-size: 11px;
  color: #5C6B63;
}}
.card-val {{
  font-size: 18px;
  font-weight: 800;
  color: #0B3D2E;
  font-family: 'Amiri', serif;
}}

table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 11px;
}}
th {{
  background: #0B3D2E;
  color: #fff;
  font-weight: 700;
  padding: 8px 6px;
  border: 1px solid #0B3D2E;
  text-align: center;
}}
td {{
  padding: 7px 6px;
  border: 1px solid #E0E0E0;
  text-align: center;
}}
tr:nth-child(even) {{
  background: #F9FAF9;
}}

.report-footer {{
  margin-top: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #D9CFB8;
  padding-top: 10px;
  font-size: 11px;
  color: #5C6B63;
}}
.verse {{
  font-family: 'Amiri', serif;
  font-size: 14px;
  color: #145C43;
  font-style: italic;
}}
@media print {{
  body {{ padding: 5mm; }}
  @page {{ size: A4 landscape; margin: 10mm; }}
}}
</style>
</head>
<body>

<div class="report-header">
  <div style="display: flex; align-items: center; gap: 15px;">
    <img src="/files/Screenshot 2026-07-23 013547.png" alt="منصة البر الوقفية" style="max-height: 60px; width: auto; object-fit: contain;">
    <div>
      <div class="brand-title">منصة البر الوقفية — تقرير قائمة المعاملات</div>
      <div class="brand-sub">الهيئة العامة للأوقاف والشؤون الإسلامية</div>
    </div>
  </div>
  <div class="report-meta">
    تاريخ الإصدار: {frappe.utils.format_datetime(frappe.utils.now())}<br>
    إجمالي السجلات: {total_count} معاملة
  </div>
</div>

<div class="summary-cards">
  <div class="card-item">
    <div class="card-label">عدد المعاملات في التقرير</div>
    <div class="card-val">{total_count}</div>
  </div>
  <div class="card-item">
    <div class="card-label">إجمالي القيمة المحددة</div>
    <div class="card-val" style="color:#C6A15B;">ل.د {total_sum:,.2f}</div>
  </div>
</div>

<table>
  <thead>
    <tr>
      <th>#</th>
      <th>ID المعاملة</th>
      <th>المستخدم / المتبرع</th>
      <th>رقم الطلب</th>
      <th>رقم الحوالة/الصك</th>
      <th>المصرف</th>
      <th>القيمة الإجمالية</th>
      <th>تاريخ المعاملة</th>
      <th>حالة المعاملة</th>
      <th>حالة المطابقة</th>
      <th>النوع</th>
      <th>الاستثناء</th>
    </tr>
  </thead>
  <tbody>
    {html_table_rows}
  </tbody>
</table>

<div class="report-footer">
  <div class="verse">﴿ لَن تَنَالُوا الْبِرَّ حَتَّىٰ تُنفِقُوا مِمَّا تُحِبُّونَ ﴾</div>
  <div>منصة البر الوقفية — albir.ly</div>
</div>

</body>
</html>"""
	return full_html

@frappe.whitelist()
def get_multi_print_html(doc_type, names, print_format="Bir Transaction Receipt"):
	if isinstance(names, str):
		names = json.loads(names)
	html_outs = []
	for name in names:
		try:
			html_outs.append(frappe.get_print(doc_type, name, print_format=print_format, no_letterhead=1))
		except Exception as e:
			html_outs.append(f"<div class='alert alert-danger'>خطأ في طباعة المعاملة {name}: {str(e)}</div>")
			
	full_html = """<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="utf-8">
<title>طباعة إيصالات المعاملات</title>
<style>
@media print {
  .page-break { page-break-after: always; }
}
</style>
</head>
<body style="margin:0; padding:0; background:#f4f5f7;">
""" + '<div class="page-break" style="page-break-after: always; height: 1px;"></div>'.join(html_outs) + """
</body>
</html>"""
	return full_html

@frappe.whitelist()
def fetch_statement_transactions(statement_name, import_batch=None, from_date=None, to_date=None):
	res = fetch_tx_for_statement(statement_name, import_batch, from_date, to_date)
	return res

@frappe.whitelist()
def reconcile_statement_doc(statement_name):
	if frappe.db.exists("Bir Bank Statement", statement_name):
		doc = frappe.get_doc("Bir Bank Statement", statement_name)
		matched = reconcile_bank_statement(doc)
		return {"status": "success", "matched_count": matched}
	return {"status": "error", "message": "كشف الحساب غير موجود"}

@frappe.whitelist()
def post_transactions_to_statement_api(statement_name, transaction_names=None, import_batch=None):
	if isinstance(transaction_names, str):
		transaction_names = json.loads(transaction_names)
	res = post_txs_to_statement(transaction_names or [], statement_name, import_batch)
	return res

@frappe.whitelist()
def run_auto_reconciliation(from_date=None, to_date=None, bank=None):
	res = bulk_reconcile_by_date_and_bank(from_date, to_date, bank)
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
def sync_workspace():
	from bir_waqf.utils.setup_block import setup_custom_block
	setup_custom_block()

	if frappe.db.exists("Workspace", "البر الوقفية"):
		frappe.delete_doc("Workspace", "البر الوقفية", force=True)

	ws_title = "المراجعة والتدقيق"
	if frappe.db.exists("Workspace", ws_title):
		doc = frappe.get_doc("Workspace", ws_title)
	else:
		doc = frappe.new_doc("Workspace")
		doc.name = ws_title

	doc.title = ws_title
	doc.label = ws_title
	doc.category = "Modules"
	doc.module = "Bir Waqf"
	doc.icon = "bank"
	doc.public = 1

	filter_basket_json = json.dumps([["Bir Transaction", "is_basket", "=", 1]])

	doc.content = json.dumps([
		
		{"type": "header", "data": {"text": "المراجعة الداخلية والتدقيق (منصة البر الوقفية)"}},
		{"type": "shortcut", "data": {"shortcut_name": "مركز معالجة البيانات", "type": "Page", "link_to": "bir_data_processor"}},
		{"type": "shortcut", "data": {"shortcut_name": "دفعات الاستيراد", "type": "DocType", "link_to": "Bir Import Batch"}},
		{"type": "shortcut", "data": {"shortcut_name": "جميع المعاملات", "type": "DocType", "link_to": "Bir Transaction"}},
		{"type": "shortcut", "data": {"shortcut_name": "معاملات السلة", "type": "DocType", "link_to": "Bir Transaction", "stats_filter": filter_basket_json}},
		{"type": "shortcut", "data": {"shortcut_name": "كشوف الحساب المصرفية", "type": "DocType", "link_to": "Bir Bank Statement"}}
	])

	doc.set("shortcuts", [
		{"label": "مركز معالجة البيانات", "type": "Page", "link_to": "bir_data_processor", "color": "Green"},
		{"label": "دفعات الاستيراد", "type": "DocType", "link_to": "Bir Import Batch", "color": "Purple"},
		{"label": "جميع المعاملات", "type": "DocType", "link_to": "Bir Transaction", "color": "Blue"},
		{"label": "معاملات السلة", "type": "DocType", "link_to": "Bir Transaction", "stats_filter": filter_basket_json, "color": "Orange"},
		{"label": "كشوف الحساب المصرفية", "type": "DocType", "link_to": "Bir Bank Statement", "color": "Green"}
	])

	doc.flags.ignore_permissions = True
	doc.save()
	frappe.db.commit()
	return "Workspace Synced with Custom HTML Block: " + doc.name

@frappe.whitelist()
def get_dashboard_stats():
	total_tx = frappe.db.count("Bir Transaction")
	total_amount = frappe.db.sql("SELECT SUM(total_amount) FROM `tabBir Transaction`")[0][0] or 0.0
	matched_tx = frappe.db.count("Bir Transaction", {"reconciliation_status": ["in", ["مطابق آليًا", "مطابق يدويًا"]]})
	exceptions_tx = frappe.db.count("Bir Transaction", {"has_exception": 1})
	basket_tx = frappe.db.count("Bir Transaction", {"is_basket": 1})
	batches_count = frappe.db.count("Bir Import Batch")
	
	projects = frappe.db.sql("""
		SELECT project_name, SUM(sub_amount) as total 
		FROM `tabBir Basket Project` 
		WHERE project_name IS NOT NULL AND project_name != '' AND project_name != '-'
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
		"batches_count": batches_count,
		"top_projects": projects
	}
