import frappe, openpyxl, io, json, base64
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def apply_excel_styling(ws):
	"""
	Applies RTL layout, auto column width, and freeze panes to an openpyxl worksheet.
	"""
	ws.views.sheetView[0].rightToLeft = True
	ws.freeze_panes = "A2"

	thin_border = Border(
		left=Side(style='thin', color='D0D5DD'),
		right=Side(style='thin', color='D0D5DD'),
		top=Side(style='thin', color='D0D5DD'),
		bottom=Side(style='thin', color='D0D5DD')
	)

	for col in ws.columns:
		max_len = 0
		col_letter = get_column_letter(col[0].column)
		for cell in col:
			cell.border = thin_border
			val_str = str(cell.value or '')
			if len(val_str) > max_len:
				max_len = len(val_str)
		ws.column_dimensions[col_letter].width = max(max_len + 5, 14)

def build_transactions_excel(tx_list):
	"""
	Generates an openpyxl Workbook for selected transactions (with basket sub-rows).
	"""
	wb = openpyxl.Workbook()
	ws = wb.active
	ws.title = "المعاملات المحددة"

	header_fill = PatternFill(start_color="0A4D2E", end_color="0A4D2E", fill_type="solid")
	header_font = Font(name="Tajawal", size=11, bold=True, color="FFFFFF")
	sub_header_fill = PatternFill(start_color="F0FDF4", end_color="F0FDF4", fill_type="solid")
	sub_font = Font(name="Tajawal", size=10, italic=True, color="166534")

	headers = [
		"#", "رقم المعاملة", "رقم طلب المساهمة", "رقم الحوالة/الصك",
		"المستخدم / المتبرع", "المصرف", "طريقة الدفع", "المشروع",
		"القيمة الإجمالية (د.ل)", "التاريخ", "حالة المطابقة", "نوع المعاملة"
	]
	
	ws.append(headers)
	ws.row_dimensions[1].height = 26

	for col_idx in range(1, len(headers) + 1):
		cell = ws.cell(row=1, column=col_idx)
		cell.fill = header_fill
		cell.font = header_font
		cell.alignment = Alignment(horizontal="center", vertical="center")

	row_num = 2
	for idx, tx in enumerate(tx_list, 1):
		tx_doc = frappe.get_doc("Bir Transaction", tx.name)
		is_basket = bool(tx_doc.is_basket)
		tx_type = "سلة مشاريع" if is_basket else "معاملة مفردة"
		proj_display = tx_doc.project
		if not proj_display:
			if tx_doc.basket_projects:
				proj_display = ", ".join(p.project_name for p in tx_doc.basket_projects if p.project_name)
			else:
				proj_display = "-"
		dt_str = str(tx_doc.transaction_date)[:16] if tx_doc.transaction_date else "-"

		main_row = [
			idx,
			tx_doc.transaction_id or "-",
			tx_doc.contribution_request_id or "-",
			tx_doc.transfer_number or "-",
			tx_doc.donor_name or "فاعل خير",
			tx_doc.bank_name or "-",
			tx_doc.payment_method or "-",
			proj_display,
			float(tx_doc.total_amount or 0.0),
			dt_str,
			tx_doc.reconciliation_status or "غير مطابق",
			tx_type
		]
		ws.append(main_row)
		ws.cell(row=row_num, column=9).number_format = '#,##0.00 "د.ل"'
		ws.row_dimensions[row_num].height = 22
		row_num += 1

		# If basket transaction, append indented sub-rows for projects
		if is_basket and tx_doc.basket_projects:
			for sub_idx, sub in enumerate(tx_doc.basket_projects, 1):
				sub_row = [
					f"  └ {idx}.{sub_idx}",
					"-",
					"-",
					"-",
					f"↳ فرعي: {sub.project_name}",
					"-",
					"-",
					sub.project_name,
					float(sub.sub_amount or 0.0),
					"-",
					"-",
					"مشروع فرعي"
				]
				ws.append(sub_row)
				ws.cell(row=row_num, column=9).number_format = '#,##0.00 "د.ل"'
				ws.row_dimensions[row_num].height = 20
				for c in range(1, len(sub_row) + 1):
					cell = ws.cell(row=row_num, column=c)
					cell.fill = sub_header_fill
					cell.font = sub_font
				row_num += 1

	apply_excel_styling(ws)
	
	output = io.BytesIO()
	wb.save(output)
	return output.getvalue()


def build_grouped_bank_statement_excel(import_batch, bank, selected_projects):
	"""
	Generates an openpyxl Workbook grouped by Project for Quick Entry / Bank Reconciliation.
	"""
	wb = openpyxl.Workbook()
	ws = wb.active
	ws.title = "كشف حساب المصرف - المشاريع"

	title_fill = PatternFill(start_color="0A4D2E", end_color="0A4D2E", fill_type="solid")
	title_font = Font(name="Tajawal", size=13, bold=True, color="FFFFFF")
	
	proj_header_fill = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")
	proj_header_font = Font(name="Tajawal", size=11, bold=True, color="0A4D2E")
	
	subtotal_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
	subtotal_font = Font(name="Tajawal", size=11, bold=True, color="92400E")

	header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
	header_font = Font(name="Tajawal", size=10, bold=True, color="FFFFFF")

	# Title Banner
	ws.merge_cells("A1:G1")
	ws["A1"] = f"كشف الحساب وتوزيع التبرعات — المصرف: {bank or 'الكل'} (الدفعة: {import_batch or 'الكل'})"
	ws["A1"].fill = title_fill
	ws["A1"].font = title_font
	ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
	ws.row_dimensions[1].height = 32

	ws.append([]) # empty row 2

	headers = ["#", "رقم المعاملة", "رقم الحوالة / الصك", "المستخدم / المتبرع", "مبلغ التبرع (د.ل)", "تاريخ المعاملة", "تمت المطابقة"]
	ws.append(headers)
	ws.row_dimensions[3].height = 24
	for c_idx in range(1, len(headers) + 1):
		cell = ws.cell(row=3, column=c_idx)
		cell.fill = header_fill
		cell.font = header_font
		cell.alignment = Alignment(horizontal="center", vertical="center")

	# Fetch data grouped by project
	filters = {}
	if import_batch and str(import_batch).strip():
		filters["import_batch"] = str(import_batch).strip()
	if bank and str(bank).strip():
		filters["bank_name"] = str(bank).strip()

	if isinstance(selected_projects, str):
		try:
			selected_projects = json.loads(selected_projects)
		except Exception:
			selected_projects = [selected_projects]

	if not selected_projects:
		selected_projects = []

	cur_row = 4

	for p_name in selected_projects:
		if not p_name or not str(p_name).strip():
			continue

		clean_p = str(p_name).strip()

		# Single transactions matching project OR basket transactions containing child project
		txs_single = frappe.get_all(
			"Bir Transaction",
			filters={**filters, "is_basket": 0, "project": clean_p},
			fields=["name", "transaction_id", "transfer_number", "donor_name", "total_amount", "transaction_date", "reconciliation_status"]
		)

		txs_basket_rows = frappe.db.sql("""
			SELECT t.name, t.transaction_id, t.transfer_number, t.donor_name, b.sub_amount as total_amount, t.transaction_date, t.reconciliation_status
			FROM `tabBir Transaction` t
			INNER JOIN `tabBir Basket Project` b ON b.parent = t.name
			WHERE t.is_basket = 1
			""" + (" AND t.import_batch = %s" if import_batch else "") + """
			""" + (" AND t.bank_name = %s" if bank else "") + """
			AND (b.project_name = %s OR LOWER(TRIM(b.project_name)) = LOWER(%s))
		""", tuple([v for v in [import_batch, bank] if v] + [clean_p, clean_p]), as_dict=True) or []

		all_project_txs = txs_single + txs_basket_rows

		# Group Section Header
		ws.merge_cells(start_row=cur_row, start_column=1, end_row=cur_row, end_column=7)
		header_cell = ws.cell(row=cur_row, column=1)
		header_cell.value = f"📌 مشروع: {clean_p} (عدد التبرعات: {len(all_project_txs)})"
		header_cell.fill = proj_header_fill
		header_cell.font = proj_header_font
		header_cell.alignment = Alignment(horizontal="right", vertical="center")
		ws.row_dimensions[cur_row].height = 24
		cur_row += 1

		proj_sum = 0.0
		for t_idx, tx in enumerate(all_project_txs, 1):
			amt = float(tx.total_amount or 0.0)
			proj_sum += amt
			is_reconciled = "نعم" if tx.reconciliation_status in ["مطابق آليًا", "مطابق يدويًا"] else "لا"
			dt_str = str(tx.transaction_date)[:16] if tx.transaction_date else "-"

			row_vals = [
				t_idx,
				tx.transaction_id or "-",
				tx.transfer_number or "-",
				tx.donor_name or "فاعل خير",
				amt,
				dt_str,
				is_reconciled
			]
			ws.append(row_vals)
			ws.cell(row=cur_row, column=5).number_format = '#,##0.00 "د.ل"'
			ws.cell(row=cur_row, column=7).alignment = Alignment(horizontal="center")
			ws.row_dimensions[cur_row].height = 20
			cur_row += 1

		# Subtotal Row
		ws.merge_cells(start_row=cur_row, start_column=1, end_row=cur_row, end_column=4)
		ws.cell(row=cur_row, column=1).value = f"إجمالي تبرعات مشروع ({clean_p}):"
		ws.cell(row=cur_row, column=1).fill = subtotal_fill
		ws.cell(row=cur_row, column=1).font = subtotal_font
		ws.cell(row=cur_row, column=1).alignment = Alignment(horizontal="left", vertical="center")

		ws.cell(row=cur_row, column=5).value = proj_sum
		ws.cell(row=cur_row, column=5).number_format = '#,##0.00 "د.ل"'
		ws.cell(row=cur_row, column=5).fill = subtotal_fill
		ws.cell(row=cur_row, column=5).font = subtotal_font

		for col_c in range(6, 8):
			cell = ws.cell(row=cur_row, column=col_c)
			cell.fill = subtotal_fill

		ws.row_dimensions[cur_row].height = 22
		cur_row += 1

		# Empty spacing row
		ws.append([])
		cur_row += 1

	apply_excel_styling(ws)

	output = io.BytesIO()
	wb.save(output)
	return output.getvalue()
