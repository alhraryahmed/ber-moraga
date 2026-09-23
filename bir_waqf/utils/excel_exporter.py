import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
import io, json
import frappe
from bir_waqf.utils.project_utils import get_project_title, resolve_project_tokens

def build_transactions_excel(transactions):
	"""
	Generates an openpyxl Workbook in-memory for selected Bir Transactions.
	Applies RTL direction, custom Arabic styling, and auto column width calculations.
	Basket transactions are expanded into dedicated sub-project rows with their specific sub-amounts.
	"""
	wb = openpyxl.Workbook()
	ws = wb.active
	ws.title = "المعاملات المحددة"

	ws.views.sheetView[0].rightToLeft = True

	title_fill = PatternFill(start_color="0A4D2E", end_color="0A4D2E", fill_type="solid")
	title_font = Font(name="Tajawal", size=14, bold=True, color="FFFFFF")

	header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
	header_font = Font(name="Tajawal", size=10, bold=True, color="FFFFFF")

	thin_border = Border(
		left=Side(style='thin', color='E2E8F0'),
		right=Side(style='thin', color='E2E8F0'),
		top=Side(style='thin', color='E2E8F0'),
		bottom=Side(style='thin', color='E2E8F0')
	)

	ws.merge_cells("A1:I1")
	ws["A1"] = "تقرير قائمة معاملات منصة البر الوقفية المحددة للمطابقة"
	ws["A1"].fill = title_fill
	ws["A1"].font = title_font
	ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
	ws.row_dimensions[1].height = 35

	ws.append([]) # empty row 2

	headers = [
		"#", "رقم المعاملة", "رقم الحوالة / الصك", "اسم المتبرع",
		"المصرف", "المشروع", "مبلغ المشاركة (د.ل)", "تاريخ المعاملة", "حالة المطابقة"
	]
	ws.append(headers)
	ws.row_dimensions[3].height = 25

	for col_num in range(1, len(headers) + 1):
		cell = ws.cell(row=3, column=col_num)
		cell.fill = header_fill
		cell.font = header_font
		cell.alignment = Alignment(horizontal="center", vertical="center")
		cell.border = thin_border

	row_counter = 1
	for tx_info in transactions:
		tx = frappe.get_doc("Bir Transaction", tx_info.get("name") or tx_info.get("transaction_id"))
		dt_str = str(tx.transaction_date)[:16] if tx.transaction_date else "-"
		rec_status = tx.reconciliation_status or "غير مطابق"

		if tx.is_basket and tx.basket_projects:
			for sub in tx.basket_projects:
				sub_title = get_project_title(sub.project_name)
				sub_amt = float(sub.sub_amount or 0.0)
				row_data = [
					row_counter,
					f"{tx.transaction_id or '-'} (سلة)",
					tx.transfer_number or "-",
					tx.donor_name or "فاعل خير",
					tx.bank_name or "-",
					sub_title,
					sub_amt,
					dt_str,
					rec_status
				]
				ws.append(row_data)

				row_idx = ws.max_row
				ws.row_dimensions[row_idx].height = 20
				for col_num in range(1, len(headers) + 1):
					c = ws.cell(row=row_idx, column=col_num)
					c.border = thin_border
					c.alignment = Alignment(horizontal="right", vertical="center")
					if col_num in [1, 8, 9]:
						c.alignment = Alignment(horizontal="center", vertical="center")
					if col_num == 7:
						c.number_format = '#,##0.00 "د.ل"'
						c.font = Font(name="Tajawal", bold=True, color="0A4D2E")
				row_counter += 1
		else:
			proj_display = get_project_title(tx.project) if tx.project else "-"
			row_data = [
				row_counter,
				tx.transaction_id or "-",
				tx.transfer_number or "-",
				tx.donor_name or "فاعل خير",
				tx.bank_name or "-",
				proj_display,
				float(tx.total_amount or 0.0),
				dt_str,
				rec_status
			]
			ws.append(row_data)

			row_idx = ws.max_row
			ws.row_dimensions[row_idx].height = 20
			for col_num in range(1, len(headers) + 1):
				c = ws.cell(row=row_idx, column=col_num)
				c.border = thin_border
				c.alignment = Alignment(horizontal="right", vertical="center")
				if col_num in [1, 8, 9]:
					c.alignment = Alignment(horizontal="center", vertical="center")
				if col_num == 7:
					c.number_format = '#,##0.00 "د.ل"'
					c.font = Font(name="Tajawal", bold=True, color="0A4D2E")
			row_counter += 1

	for col in ws.columns:
		max_len = 0
		col_letter = get_column_letter(col[0].column)
		for cell in col:
			val_str = str(cell.value or "")
			if cell.row > 1 and len(val_str) > max_len:
				max_len = len(val_str)
		ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

	output = io.BytesIO()
	wb.save(output)
	return output.getvalue()


def build_grouped_bank_statement_excel(import_batch, bank, selected_projects):
	"""
	Generates an openpyxl Workbook grouped by Project for Quick Entry / Bank Reconciliation.
	Displays Arabic Project Titles, excludes Donor column, and adds Grand Total row at bottom.
	"""
	wb = openpyxl.Workbook()
	ws = wb.active
	ws.title = "كشف حساب المصرف - المشاريع"

	ws.views.sheetView[0].rightToLeft = True

	title_fill = PatternFill(start_color="0A4D2E", end_color="0A4D2E", fill_type="solid")
	title_font = Font(name="Tajawal", size=13, bold=True, color="FFFFFF")
	
	proj_header_fill = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")
	proj_header_font = Font(name="Tajawal", size=11, bold=True, color="0A4D2E")
	
	subtotal_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
	subtotal_font = Font(name="Tajawal", size=11, bold=True, color="92400E")

	header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
	header_font = Font(name="Tajawal", size=10, bold=True, color="FFFFFF")

	thin_border = Border(
		left=Side(style='thin', color='CBD5E1'),
		right=Side(style='thin', color='CBD5E1'),
		top=Side(style='thin', color='CBD5E1'),
		bottom=Side(style='thin', color='CBD5E1')
	)

	# Title Banner
	ws.merge_cells("A1:F1")
	ws["A1"] = f"كشف الحساب وتوزيع التبرعات — المصرف: {bank or 'الكل'} (الدفعة: {import_batch or 'الكل'})"
	ws["A1"].fill = title_fill
	ws["A1"].font = title_font
	ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
	ws.row_dimensions[1].height = 32

	ws.append([]) # empty row 2

	# Header without Donor column
	headers = ["#", "رقم المعاملة", "رقم الحوالة / الصك", "مبلغ التبرع (د.ل)", "تاريخ المعاملة", "تمت المطابقة"]
	ws.append(headers)
	ws.row_dimensions[3].height = 24
	for c_idx in range(1, len(headers) + 1):
		cell = ws.cell(row=3, column=c_idx)
		cell.fill = header_fill
		cell.font = header_font
		cell.alignment = Alignment(horizontal="center", vertical="center")
		cell.border = thin_border

	if isinstance(selected_projects, str):
		if selected_projects.startswith("["):
			try:
				selected_projects = json.loads(selected_projects)
			except Exception:
				selected_projects = [p.strip() for p in selected_projects.split(",") if p.strip()]
		else:
			selected_projects = [p.strip() for p in selected_projects.split(",") if p.strip()]

	if not selected_projects:
		from bir_waqf.api import get_all_linked_projects
		selected_projects = get_all_linked_projects(import_batch, bank)

	cur_row = 4
	grand_total_all = 0.0

	for p_input in selected_projects:
		if not p_input or not str(p_input).strip():
			continue

		clean_p = str(p_input).strip()
		p_title = get_project_title(clean_p)
		tokens = list(resolve_project_tokens(clean_p))

		if not tokens:
			tokens = [clean_p]

		clean_batch = str(import_batch).strip() if import_batch else ""
		clean_bank = str(bank).strip() if bank and str(bank).strip() else None

		# Query matching single and basket transactions
		tx_filters = {"is_basket": 0, "project": ["in", tokens]}
		if clean_batch:
			tx_filters["import_batch"] = clean_batch
		if clean_bank:
			tx_filters["bank_name"] = clean_bank

		txs_single = frappe.get_all(
			"Bir Transaction",
			filters=tx_filters,
			fields=["name", "transaction_id", "transfer_number", "donor_name", "total_amount", "transaction_date", "reconciliation_status"]
		)

		sub_conditions = []
		sub_params = []
		if clean_batch:
			sub_conditions.append("t.import_batch = %s")
			sub_params.append(clean_batch)
		if clean_bank:
			sub_conditions.append("(TRIM(t.bank_name) = %s OR TRIM(t.bank_name) LIKE %s)")
			sub_params.extend([clean_bank, f"%{clean_bank}%"])

		proj_or_list = []
		for tk in tokens:
			proj_or_list.append("(LOWER(TRIM(b.project_name)) = %s OR LOWER(TRIM(b.project_name)) LIKE %s)")
			sub_params.extend([tk.lower(), f"%{tk.lower()}%"])

		cond_sql = " AND ".join(sub_conditions)
		if cond_sql:
			cond_sql = " AND " + cond_sql
		proj_sql = " OR ".join(proj_or_list)

		sql_query = f"""
			SELECT t.name, t.transaction_id, t.transfer_number, t.donor_name, b.sub_amount as total_amount, t.transaction_date, t.reconciliation_status
			FROM `tabBir Transaction` t
			INNER JOIN `tabBir Basket Project` b ON b.parent = t.name
			WHERE t.is_basket = 1
			{cond_sql}
			AND ({proj_sql})
		"""
		txs_basket_rows = frappe.db.sql(sql_query, tuple(sub_params), as_dict=True) or []

		items = txs_single + txs_basket_rows
		seen_keys = set()
		unique_items = []
		for i in items:
			key = f"{i.name}_{i.transaction_id}_{i.total_amount}"
			if key not in seen_keys:
				seen_keys.add(key)
				unique_items.append(i)

		if not unique_items:
			continue

		# Group Section Header with Arabic Title
		ws.merge_cells(start_row=cur_row, start_column=1, end_row=cur_row, end_column=6)
		header_cell = ws.cell(row=cur_row, column=1)
		header_cell.value = f"📌 مشروع: {p_title} (عدد التبرعات: {len(unique_items)})"
		header_cell.fill = proj_header_fill
		header_cell.font = proj_header_font
		header_cell.alignment = Alignment(horizontal="right", vertical="center")
		ws.row_dimensions[cur_row].height = 24
		cur_row += 1

		proj_sum = 0.0
		for t_idx, tx in enumerate(unique_items, 1):
			amt = float(tx.total_amount or 0.0)
			proj_sum += amt
			is_reconciled = "نعم" if tx.reconciliation_status in ["مطابق آليًا", "مطابق يدويًا"] else "لا"
			dt_str = str(tx.transaction_date)[:16] if tx.transaction_date else "-"

			row_vals = [
				t_idx,
				tx.transaction_id or "-",
				tx.transfer_number or "-",
				amt,
				dt_str,
				is_reconciled
			]
			ws.append(row_vals)
			ws.cell(row=cur_row, column=4).number_format = '#,##0.00 "د.ل"'
			ws.cell(row=cur_row, column=6).alignment = Alignment(horizontal="center")
			
			for c_col in range(1, 7):
				ws.cell(row=cur_row, column=c_col).border = thin_border

			ws.row_dimensions[cur_row].height = 20
			cur_row += 1

		grand_total_all += proj_sum

		# Subtotal Row
		ws.merge_cells(start_row=cur_row, start_column=1, end_row=cur_row, end_column=3)
		ws.cell(row=cur_row, column=1).value = f"إجمالي تبرعات مشروع ({p_title}):"
		ws.cell(row=cur_row, column=1).fill = subtotal_fill
		ws.cell(row=cur_row, column=1).font = subtotal_font
		ws.cell(row=cur_row, column=1).alignment = Alignment(horizontal="left", vertical="center")

		ws.cell(row=cur_row, column=4).value = proj_sum
		ws.cell(row=cur_row, column=4).fill = subtotal_fill
		ws.cell(row=cur_row, column=4).font = subtotal_font
		ws.cell(row=cur_row, column=4).number_format = '#,##0.00 "د.ل"'

		ws.merge_cells(start_row=cur_row, start_column=5, end_row=cur_row, end_column=6)
		ws.cell(row=cur_row, column=5).fill = subtotal_fill

		for c_col in range(1, 7):
			ws.cell(row=cur_row, column=c_col).border = thin_border

		ws.row_dimensions[cur_row].height = 22
		cur_row += 2

	# Grand Total Row for All Projects at bottom of Excel
	if grand_total_all > 0:
		ws.merge_cells(start_row=cur_row, start_column=1, end_row=cur_row, end_column=3)
		ws.cell(row=cur_row, column=1).value = f"📊 إجمالي كافة مشاريع المصرف في هذه الدفعة:"
		ws.cell(row=cur_row, column=1).fill = title_fill
		ws.cell(row=cur_row, column=1).font = title_font
		ws.cell(row=cur_row, column=1).alignment = Alignment(horizontal="left", vertical="center")

		ws.cell(row=cur_row, column=4).value = grand_total_all
		ws.cell(row=cur_row, column=4).fill = title_fill
		ws.cell(row=cur_row, column=4).font = Font(name="Tajawal", size=12, bold=True, color="F1C40F")
		ws.cell(row=cur_row, column=4).number_format = '#,##0.00 "د.ل"'

		ws.merge_cells(start_row=cur_row, start_column=5, end_row=cur_row, end_column=6)
		ws.cell(row=cur_row, column=5).fill = title_fill

		for c_col in range(1, 7):
			ws.cell(row=cur_row, column=c_col).border = thin_border
		ws.row_dimensions[cur_row].height = 26

	for col in ws.columns:
		max_len = 0
		col_letter = get_column_letter(col[0].column)
		for cell in col:
			val_str = str(cell.value or "")
			if cell.row > 1 and len(val_str) > max_len:
				max_len = len(val_str)
		ws.column_dimensions[col_letter].width = max(max_len + 4, 15)

	output = io.BytesIO()
	wb.save(output)
	return output.getvalue()
