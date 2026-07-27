import frappe, re

def get_or_create_project(project_name):
	"""
	Gets an existing Project document name by matching project_name (case-insensitive and whitespace-stripped).
	If not found, creates a new Project document and returns its name (ID e.g. PROJ-0001).
	"""
	if not project_name or not str(project_name).strip():
		return None

	clean_name = " ".join(str(project_name).strip().split())

	if not clean_name:
		return None

	# Check existing project by exact name or project_name
	existing = frappe.db.sql("""
		SELECT name FROM `tabProject`
		WHERE LOWER(TRIM(project_name)) = LOWER(%s) OR LOWER(TRIM(name)) = LOWER(%s)
		LIMIT 1
	""", (clean_name, clean_name))

	if existing and existing[0][0]:
		return existing[0][0]

	# Create new Project
	try:
		doc = frappe.new_doc("Project")
		doc.project_name = clean_name
		doc.flags.ignore_permissions = True
		doc.insert()
		frappe.db.commit()
		return doc.name
	except Exception as e:
		frappe.log_error(f"Error creating project {clean_name}: {str(e)}", "get_or_create_project")
		existing = frappe.db.get_value("Project", {"project_name": clean_name}, "name")
		if existing:
			return existing
		return None

def get_project_title(project_name_or_id):
	"""
	Returns the human-readable project_name (Arabic Title e.g. 'مشروع بناء مسجد...') for a given
	Project ID (e.g. PROJ-0001) or title.
	"""
	if not project_name_or_id or not str(project_name_or_id).strip():
		return "-"

	val = str(project_name_or_id).strip()

	title = frappe.db.get_value("Project", val, "project_name")
	if title and str(title).strip():
		return str(title).strip()

	by_title = frappe.db.get_value("Project", {"project_name": val}, "project_name")
	if by_title and str(by_title).strip():
		return str(by_title).strip()

	return val

def resolve_project_tokens(p_str):
	"""
	Given any project input string (e.g. 'PROJ-0001', 'مشروع كذا', or 'مشروع كذا (PROJ-0001)'),
	returns set of matching project IDs and titles (in lowercase) for database matching.
	"""
	tokens = set()
	if not p_str or not str(p_str).strip():
		return tokens

	text = str(p_str).strip()
	tokens.add(text.lower())

	match_id = re.search(r'\((PROJ-[0-9]+)\)', text)
	if match_id:
		proj_id = match_id.group(1).strip()
		tokens.add(proj_id.lower())
		title = frappe.db.get_value("Project", proj_id, "project_name")
		if title:
			tokens.add(str(title).strip().lower())

	raw_title = text.split('(')[0].strip()
	if raw_title:
		tokens.add(raw_title.lower())
		p_id = frappe.db.get_value("Project", {"project_name": raw_title}, "name")
		if p_id:
			tokens.add(str(p_id).strip().lower())

	p_title = frappe.db.get_value("Project", text, "project_name")
	if p_title:
		tokens.add(str(p_title).strip().lower())

	return tokens
