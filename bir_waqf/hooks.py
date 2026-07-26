app_name = "bir_waqf"
app_title = "البر الوقفية"
app_publisher = "البر الوقفية"
app_description = "نظام معالجة بيانات ومطابقة منصة البر الوقفية"
app_email = "info@waqf.ly"
app_license = "mit"

app_include_css = "/assets/bir_waqf/css/bir_waqf.css"

doc_events = {
	"Bir Bank Statement": {
		"on_submit": "bir_waqf.utils.reconciliation.reconcile_bank_statement"
	}
}

fixtures = [
	"Custom HTML Block",
	"Client Script",
	"Server Script",
	"Custom Field",
	"Property Setter",
	"Print Format",
	"Workspace",
	"Page"
]
