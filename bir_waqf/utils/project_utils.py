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
	Given any project input string (e.g. 'PROJ-0001', 'مشروع كذا', or '(PROJ-0001) مشروع كذا'),
	returns set of matching project IDs and titles (in original, lowercase, and uppercase) for database matching.
	"""
	tokens = set()
	if not p_str or not str(p_str).strip():
		return tokens

	text = str(p_str).strip()
	tokens.add(text)
	tokens.add(text.lower())
	tokens.add(text.upper())

	# Extract PROJ-XXXX if present anywhere in text
	match_ids = re.findall(r'PROJ-[0-9]+', text, re.IGNORECASE)
	for proj_id in match_ids:
		pid = proj_id.strip()
		tokens.add(pid)
		tokens.add(pid.lower())
		tokens.add(pid.upper())
		title = frappe.db.get_value("Project", pid, "project_name")
		if title:
			t = str(title).strip()
			tokens.add(t)
			tokens.add(t.lower())
			tokens.add(t.upper())

	# Try exact lookup in Project DocType by name or project_name
	p_doc = frappe.db.sql("""
		SELECT name, project_name FROM `tabProject`
		WHERE LOWER(TRIM(name)) = LOWER(%s) OR LOWER(TRIM(project_name)) = LOWER(%s)
		LIMIT 1
	""", (text, text), as_dict=True)

	if p_doc:
		pid = p_doc[0].name
		pname = p_doc[0].project_name or pid
		tokens.add(pid)
		tokens.add(pid.lower())
		tokens.add(pid.upper())
		tokens.add(pname)
		tokens.add(pname.lower())
		tokens.add(pname.upper())

	return tokens
