frappe.listview_settings['Bir Transaction'] = {
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

		// Custom Print Button for List View Table Report
		listview.page.add_inner_button(__('طباعة جدول المعاملات'), function() {
			var selected = listview.get_checked_items();
			var names = selected && selected.length ? selected.map(function(item) { return item.name; }) : null;
			
			frappe.show_alert({message: __('جاري تجهيز تقرير قائمة المعاملات للطباعة...'), indicator: 'blue'});
			
			frappe.call({
				method: 'bir_waqf.api.get_transaction_list_print_html',
				args: {
					names: names
				},
				callback: function(r) {
					if (r.message) {
						var w = window.open('', '_blank');
						w.document.write(r.message);
						w.document.close();
						w.focus();
						setTimeout(function() { w.print(); }, 800);
					}
				}
			});
		}).addClass('btn-default');

		// Export Excel Button for Selected Transactions
		listview.page.add_inner_button(__('تصدير إكسل للمعاملات المحددة'), function() {
			var selected = listview.get_checked_items();
			var names = selected && selected.length ? selected.map(function(item) { return item.name; }) : null;
			
			frappe.show_alert({message: __('جاري توليد ملف الإكسل للمعاملات المحددة...'), indicator: 'blue'});
			
			frappe.call({
				method: 'bir_waqf.api.export_selected_transactions_excel',
				args: {
					names: names
				},
				callback: function(r) {
					if (r.message && r.message.file_url) {
						window.open(r.message.file_url, '_blank');
					}
				}
			});
		}).addClass('btn-success');
	}
};
