frappe.listview_settings['Bir Transaction'] = {
	onload: function(listview) {
		// Post to Statement Entries Dialog Button (By Import Batch & Bank)
		listview.page.add_inner_button(__('ترحيل الدفعة والمصرف للمطابقة'), function() {
			var d = new frappe.ui.Dialog({
				title: __('ترحيل معاملات (الدفعة + المصرف) إلى بنود كشف الحساب'),
				fields: [
					{
						label: __('اختر دفعة الاستيراد (Import Batch)'),
						fieldname: 'import_batch',
						fieldtype: 'Link',
						options: 'Bir Import Batch',
						reqd: 1,
						description: __('اختر دفعة الاستيراد لترحيل معاملاتها')
					},
					{
						label: __('تصفية حسب المصرف'),
						fieldname: 'bank',
						fieldtype: 'Link',
						options: 'Bank',
						description: __('اختر المصرف لترحيل معاملات هذا المصرف فقط داخل كشف حسابه')
					}
				],
				primary_action_label: __('إنشاء/ترحيل الآن إلى كشف الحساب'),
				primary_action: function(values) {
					d.hide();
					frappe.show_alert({message: __('جاري ترحيل معاملات المصرف والدفعة إلى كشف الحساب...'), indicator: 'blue'});
					frappe.call({
						method: 'bir_waqf.api.post_batch_transactions_to_entries',
						args: {
							import_batch: values.import_batch,
							bank: values.bank
						},
						callback: function(r) {
							if (r.message && r.message.status === 'success') {
								frappe.msgprint(__('تم إنشاء/تحديث كشف الحساب [{0}] وترحيل {1} معاملة بنجاح.', [r.message.statement_name, r.message.added_count]));
								frappe.set_route('Form', 'Bir Bank Statement', r.message.statement_name);
							}
						}
					});
				}
			});
			d.show();
		}).addClass('btn-primary');

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
	}
};
