frappe.listview_settings['Bir Transaction'] = {
	add_fields: ["reconciliation_status", "has_exception", "is_basket"],
	get_indicator: function(doc) {
		if (doc.has_exception) {
			return [__("يحتاج مراجعة / استثناء"), "orange", "has_exception,=,1"];
		}
		if (doc.reconciliation_status === "مطابق آليًا" || doc.reconciliation_status === "مطابق يدويًا") {
			return [__(doc.reconciliation_status), "green", "reconciliation_status,=," + doc.reconciliation_status];
		}
		return [__("غير مطابق"), "red", "reconciliation_status,=,غير مطابق"];
	}
};
