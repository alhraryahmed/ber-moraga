frappe.listview_settings['Bir Transaction'] = {
	add_fields: ["reconciliation_status", "has_exception", "is_basket"],
	onload: function(listview) {
		// Assign Bank Button (تضمين المصرف للمعاملات المحددة)
		listview.page.add_inner_button(__('تضمين المصرف'), function() {
			var selected = listview.get_checked_items();
			if (!selected || selected.length === 0) {
				frappe.msgprint({
					title: __('تنبيه التحديد'),
					indicator: 'orange',
					message: __('يرجى تحديد المعاملات من القائمة أولاً لتضمين المصرف.')
				});
				return;
			}

			// Pre-extract batch if all selected items share the same batch
			var default_batch = null;
			var batches = selected.map(function(item) { return item.import_batch; }).filter(Boolean);
			if (batches.length > 0 && batches.every(function(b) { return b === batches[0]; })) {
				default_batch = batches[0];
			}

			var d = new frappe.ui.Dialog({
				title: __('تضمين المصرف للمعاملات المحددة ({0})', [selected.length]),
				fields: [
					{
						label: __('دفعة الاستيراد (Import Batch)'),
						fieldname: 'import_batch',
						fieldtype: 'Link',
						options: 'Bir Import Batch',
						default: default_batch,
						description: __('الدفعة التابعة للمعاملات المختارة (مستخرجة آلياً إن كانت موحدة)')
					},
					{
						label: __('اختر المصرف لتضمينه'),
						fieldname: 'bank',
						fieldtype: 'Link',
						options: 'Bank',
						reqd: 1,
						description: __('اختر المصرف المراد تخزينه في حقل المصرف للمعاملات المحددة (مثل: مصرف الجمهورية)')
					}
				],
				primary_action_label: __('تضمين المصرف الآن'),
				primary_action: function(values) {
					d.hide();
					var names = selected.map(function(item) { return item.name; });
					frappe.show_alert({message: __('جاري تضمين المصرف للمعاملات المحددة...'), indicator: 'blue'});
					frappe.call({
						method: 'bir_waqf.api.assign_bank_to_transactions',
						args: {
							names: names,
							bank: values.bank,
							import_batch: values.import_batch
						},
						callback: function(r) {
							if (r.message && r.message.status === 'success') {
								frappe.show_alert({
									message: __('تم تضمين المصرف ({0}) لـ {1} معاملة بنجاح.', [values.bank, r.message.updated_count]),
									indicator: 'green'
								});
								listview.refresh();
							}
						}
					});
				}
			});
			d.show();
		}).addClass('btn-secondary');
	},
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
