import frappe

def get_or_create_project(project_name):
	"""
	Gets an existing Project document name by matching project_name (case-insensitive and whitespace-stripped).
	If not found, creates a new Project document and returns its name.
	"""
	if not project_name or not str(project_name).strip():
		return None

	clean_name = " ".join(str(project_name).strip().split())

	if not clean_name:
		return None

	# Check existing project by exact name or project_name (case-insensitive & whitespace trimmed)
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
		# Fallback: check again if inserted in parallel
		existing = frappe.db.get_value("Project", {"project_name": clean_name}, "name")
		if existing:
			return existing
		return None
