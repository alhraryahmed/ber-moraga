frappe.ui.form.on('Bir Bank Statement', {
	refresh: function(frm) {
		// Custom Button: Fetch Transactions by Batch + Bank + MultiSelect Projects
		frm.add_custom_button(__('جلب المعاملات (دفعة + مصرف + مشاريع)'), function() {
			var d = new frappe.ui.Dialog({
				title: __('جلب المعاملات — تصفية حسب الدفعة والمصرف والمشاريع'),
				fields: [
					{
						label: __('1. اختر دفعة الاستيراد (Import Batch)'),
						fieldname: 'import_batch',
						fieldtype: 'Link',
						options: 'Bir Import Batch',
						reqd: 1,
						description: __('اختر دفعة الاستيراد للجلب منها')
					},
					{
						label: __('2. اختر المصرف (Bank)'),
						fieldname: 'bank',
						fieldtype: 'Link',
						options: 'Bank',
						default: frm.doc.bank || '',
						description: __('اختر المصرف لتصفية معاملات هذا المصرف فقط')
					},
					{
						label: __('3. اختر المشاريع المرادة (متعدد التحديد - اختياري)'),
						fieldname: 'projects',
						fieldtype: 'MultiSelect',
						get_data: function(txt) {
							var projects_list = [];
							frappe.call({
								method: 'bir_waqf.api.get_all_projects_for_multiselect',
								args: { txt: txt || '' },
								async: false,
								callback: function(r) {
									if (r.message && Array.isArray(r.message)) {
										projects_list = r.message.map(function(item) {
											return item.label || item.value;
										});
									}
								}
							});
							return projects_list;
						},
						description: __('اختر مشروعاً أو أكثر لجلب معاملاتها، أو اتركه فارغاً لجلب كافة المعاملات')
					}
				],
				primary_action_label: __('تصفية وجلب المعاملات الآن'),
				primary_action: function(values) {
					d.hide();
					var selected_bank = values.bank || frm.doc.bank || '';
					
					if (!frm.doc.statement_name || frm.doc.statement_name.indexOf('كشف حساب') === -1) {
						var title_bank = selected_bank || 'المصرف';
						frm.set_value('statement_name', `كشف حساب ${title_bank} - ${values.import_batch}`);
					}
					if (selected_bank && !frm.doc.bank) {
						frm.set_value('bank', selected_bank);
					}

					frappe.show_alert({message: __('جاري تصفية وجلب المعاملات...'), indicator: 'blue'});

					frappe.call({
						method: 'bir_waqf.api.get_batch_transactions_by_bank',
						args: {
							import_batch: values.import_batch,
							bank: selected_bank,
							projects: values.projects
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
										child.description = (tx.donor_name || 'متبرع') + ' - ' + tx.transaction_id + (tx.project_title ? (' (' + tx.project_title + ')') : '');
										child.amount = tx.total_amount;
										child.is_reconciled = 0;
										child.matched_transaction = tx.name;
										added++;
									}
								});
								
								frm.refresh_field('entries');
								frappe.msgprint(__('تم جلب وتعبئة {0} معاملة مصفاة لـ [{1}] من الدفعة {2} بنجاح.', [added, selected_bank || 'كافة المصارف', values.import_batch]));

								// Render interactive Grouped Project Table inside Bir Bank Statement form view
								render_grouped_view_in_form(frm, values.import_batch, selected_bank, values.projects);
							} else {
								frappe.msgprint(__('لم يتم العثور على معاملات تابعة للدفعة والمصرف والمشاريع المحددة.'));
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

function render_grouped_view_in_form(frm, import_batch, bank, projects) {
	if (!projects) return;

	var $wrapper = $(frm.fields_dict.entries.wrapper);
	$('#bir-grouped-container-in-form').remove();

	var $container = $('<div id="bir-grouped-container-in-form" class="margin-top" style="margin-top:20px;"></div>');
	$wrapper.before($container);

	$container.html('<div class="text-muted"><i class="fa fa-spinner fa-spin"></i> جاري تحميل التقرير المجمّع حسب المشاريع...</div>');

	frappe.call({
		method: 'bir_waqf.api.get_grouped_transactions_by_projects',
		args: {
			import_batch: import_batch,
			bank: bank,
			projects: projects
		},
		callback: function(r) {
			if (!r.message || r.message.length === 0) {
				$container.html('<div class="alert alert-warning text-center">لا توجد معاملات تبرع مقترنة بالمشاريع المختارة.</div>');
				return;
			}

			var html = `
				<div style="background:#fff;border:1px solid #E2E8F0;padding:15px;border-radius:8px;margin-bottom:20px;">
					<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;">
						<h4 style="margin:0;color:#0A4D2E;"><i class="fa fa-list-alt"></i> جدول كشف الحساب المجمّع حسب المشاريع</h4>
						<button class="btn btn-sm btn-success" id="btn-export-excel-in-form"><i class="fa fa-file-excel-o"></i> تصدير كشف حساب المصرف (Excel)</button>
					</div>
			`;

			r.message.forEach(function(g) {
				html += `
					<div style="background:#F8FAFC;border:1px solid #CBD5E1;border-radius:8px;margin-bottom:15px;overflow:hidden;">
						<div style="background:#E6F4EA;border-bottom:2px solid #0A4D2E;padding:10px 15px;font-weight:bold;color:#0A4D2E;display:flex;justify-content:space-between;">
							<span>📌 مشروع: ${g.project_name}</span>
							<span class="badge badge-success" style="font-size:12px;">عدد التبرعات: ${g.donations.length}</span>
						</div>
						<table class="table table-bordered table-hover" style="margin-bottom:0;font-size:12px;background:#fff;">
							<thead style="background:#1E293B;color:#fff;">
								<tr>
									<th style="width:35px;text-align:center;">#</th>
									<th>رقم المعاملة</th>
									<th>رقم الحوالة / الصك</th>
									<th>المستخدم / المتبرع</th>
									<th>مبلغ التبرع</th>
									<th style="text-align:center;">تاريخ المعاملة</th>
									<th style="width:100px;text-align:center;">تمت المطابقة</th>
								</tr>
							</thead>
							<tbody>
				`;

				if (g.donations.length === 0) {
					html += `<tr><td colspan="7" class="text-center text-muted">لا توجد تبرعات مسجلة لهذا المشروع.</td></tr>`;
				} else {
					g.donations.forEach(function(d, idx) {
						var chk = d.is_reconciled ? 'checked' : '';
						html += `
							<tr>
								<td style="text-align:center;">${idx + 1}</td>
								<td><b>${d.transaction_id}</b></td>
								<td>${d.transfer_number}</td>
								<td>${d.donor_name}</td>
								<td style="font-weight:bold;color:#0A4D2E;">${parseFloat(d.amount).toFixed(2)} د.ل</td>
								<td style="text-align:center;">${d.transaction_date}</td>
								<td style="text-align:center;">
									<input type="checkbox" class="rec-form-chk" data-tx-name="${d.name}" ${chk} style="width:16px;height:16px;cursor:pointer;accent-color:#0A4D2E;">
								</td>
							</tr>
						`;
					});
				}

				html += `
							</tbody>
							<tfoot>
								<tr style="background:#FEF3C7;font-weight:bold;color:#92400E;">
									<td colspan="4" class="text-left">إجمالي تبرعات مشروع (${g.project_name}):</td>
									<td style="font-weight:bold;color:#92400E;">${parseFloat(g.subtotal).toFixed(2)} د.ل</td>
									<td colspan="2"></td>
								</tr>
							</tfoot>
						</table>
					</div>
				`;
			});

			html += `</div>`;
			$container.html(html);

			// Bind Checkbox to toggle_transaction_reconciliation API
			$container.find('.rec-form-chk').on('change', function() {
				var $chk = $(this);
				var tx_name = $chk.attr('data-tx-name');
				var is_checked = $chk.is(':checked') ? 1 : 0;

				frappe.call({
					method: 'bir_waqf.api.toggle_transaction_reconciliation',
					args: {
						transaction_id: tx_name,
						is_reconciled: is_checked
					},
					callback: function(r) {
						if (r.message && r.message.status === 'success') {
							frappe.show_alert({
								message: is_checked ? __('تمت المطابقة وحفظ الحالة بنجاح.') : __('تم إلغاء المطابقة وتحديث السجل.'),
								indicator: is_checked ? 'green' : 'orange'
							});
						}
					}
				});
			});

			// Bind Export Excel button
			$container.find('#btn-export-excel-in-form').on('click', function() {
				frappe.show_alert({message: __('جاري إنشاء وتوليد كشف حساب المصرف Excel...'), indicator: 'blue'});
				frappe.call({
					method: 'bir_waqf.api.export_grouped_bank_statement_excel',
					args: {
						import_batch: import_batch,
						bank: bank,
						projects: projects
					},
					callback: function(r) {
						if (r.message && r.message.file_url) {
							window.open(r.message.file_url, '_blank');
						}
					}
				});
			});
		}
	});
}
