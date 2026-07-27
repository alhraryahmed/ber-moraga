import frappe

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

	# If val is a Project ID (e.g. PROJ-0001), fetch project_name field
	title = frappe.db.get_value("Project", val, "project_name")
	if title and str(title).strip():
		return str(title).strip()

	# Check if val matches project_name
	by_title = frappe.db.get_value("Project", {"project_name": val}, "project_name")
	if by_title and str(by_title).strip():
		return str(by_title).strip()

	return val
