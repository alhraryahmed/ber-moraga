frappe.ui.form.on('Bir Bank Statement', {
	refresh: function(frm) {
		// Fetch Transactions filtered by Import Batch & Bank (Works on New Forms too!)
		frm.add_custom_button(__('جلب المعاملات (دفعة + مصرف)'), function() {
			var d = new frappe.ui.Dialog({
				title: __('جلب المعاملات — تصفية حسب الدفعة والمصرف'),
				fields: [
					{
						label: __('دفعة الاستيراد (Import Batch)'),
						fieldname: 'import_batch',
						fieldtype: 'Link',
						options: 'Bir Import Batch',
						reqd: 1,
						description: __('اختر دفعة الاستيراد للجلب منها')
					},
					{
						label: __('المصرف'),
						fieldname: 'bank',
						fieldtype: 'Link',
						options: 'Bank',
						default: frm.doc.bank || '',
						description: __('اختر المصرف لتصفية معاملات الدفعة على هذا المصرف فقط')
					}
				],
				primary_action_label: __('تصفية وجلب المعاملات'),
				primary_action: function(values) {
					d.hide();
					var selected_bank = values.bank || frm.doc.bank || '';
					
					// Auto set statement title to: كشف حساب {المصرف} - {الدفعة}
					if (!frm.doc.statement_name || frm.doc.statement_name.indexOf('كشف حساب') === -1) {
						var title_bank = selected_bank || 'المصرف';
						frm.set_value('statement_name', `كشف حساب ${title_bank} - ${values.import_batch}`);
					}
					if (selected_bank && !frm.doc.bank) {
						frm.set_value('bank', selected_bank);
					}
					
					frappe.show_alert({message: __('جاري تصفية المعاملات وتعبئة كشف الحساب...'), indicator: 'blue'});
					
					frappe.call({
						method: 'bir_waqf.api.get_batch_transactions_by_bank',
						args: {
							import_batch: values.import_batch,
							bank: selected_bank
						},
						callback: function(r) {
							if (r.message && r.message.length > 0) {
								var existing_refs = (frm.doc.entries || []).map(function(e) { return e.reference_number; });
								var added = 0;
								
								r.message.forEach(function(tx) {
									var ref = tx.transfer_number || tx.transaction_id;
									if (existing_refs.indexOf(ref) === -1) {
										var child = frm.add_child('entries');
										child.reference_number = ref;
										child.posting_date = tx.transaction_date;
										child.description = (tx.donor_name || 'متبرع') + ' - ' + tx.transaction_id;
										child.amount = tx.total_amount;
										child.is_reconciled = 0;
										child.matched_transaction = tx.name;
										added++;
									}
								});
								
								frm.refresh_field('entries');
								frappe.msgprint(__('تم جلب وتعبئة {0} معاملة مصفاة لـ [{1}] من الدفعة {2} بنجاح.', [added, selected_bank || 'كافة المصارف', values.import_batch]));
							} else {
								frappe.msgprint(__('لم يتم العثور على معاملات تابعة للدفعة والمصرف المحددين.'));
							}
						}
					});
				}
			});
			d.show();
		}).addClass('btn-primary');

		if (!frm.is_new()) {
			// Auto Reconcile Statement Button
			frm.add_custom_button(__('تشغيل المطابقة الآلية الكلية'), function() {
				frappe.show_alert({message: __('جاري تنفيذ المطابقة الكلية لكشف الحساب...'), indicator: 'orange'});
				frappe.call({
					method: 'bir_waqf.api.reconcile_statement_doc',
					args: { statement_name: frm.doc.name },
					callback: function(r) {
						if(r.message) {
							frappe.msgprint(__('تمت عملية المطابقة الآلية: تم مطابقة {0} بنود مصرفية جديد.', [r.message.matched_count]));
							frm.reload_doc();
						}
					}
				});
			}).addClass('btn-success');

			// File Import Button
			frm.add_custom_button(__('رفع كشف الحساب (Excel / CSV)'), function() {
				new frappe.ui.FileUploader({
					make_attachments_public: 1,
					on_success: function(file_doc) {
						frappe.show_alert({message: __('جاري استيراد بنود كشف الحساب المصرفي...'), indicator: 'blue'});
						frappe.call({
							method: 'bir_waqf.api.import_bank_statement_file',
							args: {
								file_url: file_doc.file_url,
								statement_name: frm.doc.name
							},
							callback: function(r) {
								if(r.message) {
									frappe.show_alert({message: __('تم استيراد {0} بند بنجاح!', [r.message.count]), indicator: 'green'});
									frm.reload_doc();
								}
							}
						});
					}
				});
			});
		}
	}
});
