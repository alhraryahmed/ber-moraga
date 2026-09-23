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
						description: __('اختر مشروعاً أو أكثر لجلب معاملاتها، أو اتركه فارغاً لجلب كافة المشاريع المرتبطة تلقائياً')
					}
				],
				primary_action_label: __('تصفية وجلب المعاملات الآن'),
				primary_action: function(values) {
					d.hide();
					var selected_bank = values.bank || frm.doc.bank || '';
					var selected_projects = values.projects || '';

					if (!frm.doc.statement_name || frm.doc.statement_name.indexOf('كشف حساب') === -1) {
						var title_bank = selected_bank || 'المصرف';
						frm.set_value('statement_name', `كشف حساب ${title_bank} - ${values.import_batch}`);
					}
					if (selected_bank && !frm.doc.bank) {
						frm.set_value('bank', selected_bank);
					}

					frappe.show_alert({message: __('جاري فحص قيود الدفعة والمصرف وجلب كافة المشاريع والمعاملات...'), indicator: 'blue'});

					frappe.call({
						method: 'bir_waqf.api.get_batch_transactions_by_bank',
						args: {
							import_batch: values.import_batch,
							bank: selected_bank,
							projects: selected_projects
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
								render_grouped_view_in_form(frm, values.import_batch, selected_bank, selected_projects);
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
			// Auto Reconcile Statement Button - checks all transactions
			frm.add_custom_button(__('تشغيل المطابقة الآلية الكلية'), function() {
				frappe.show_alert({message: __('جاري تفعيل المطابقة الكلية لكافة المعاملات...'), indicator: 'orange'});
				frappe.call({
					method: 'bir_waqf.api.reconcile_all_statement_entries',
					args: { statement_name: frm.doc.name },
					callback: function(r) {
						if(r.message && r.message.status === 'success') {
							frappe.msgprint(r.message.message);
							frm.reload_doc();
						}
					}
				});
			}).addClass('btn-success');
		}

		// Automatically render grouped project table on form refresh whenever batch & bank exist
		var auto_batch = '';
		var auto_bank = frm.doc.bank || '';

		if (frm.doc.statement_name) {
			var match_batch = frm.doc.statement_name.match(/(BATCH-[0-9]+-[0-9]+)/i);
			if (match_batch) {
				auto_batch = match_batch[1];
			}
		}

		if (!auto_batch && frm.doc.entries && frm.doc.entries.length > 0) {
			var first_desc = frm.doc.entries[0].description || '';
			var match_b = first_desc.match(/(BATCH-[0-9]+-[0-9]+)/i);
			if (match_b) auto_batch = match_b[1];
		}

		if (auto_batch) {
			render_grouped_view_in_form(frm, auto_batch, auto_bank, '');
		}
	}
});

function render_grouped_view_in_form(frm, import_batch, bank, projects) {
	if (!import_batch) return;

	var $container = null;
	if (frm.fields_dict.grouped_projects_html && frm.fields_dict.grouped_projects_html.$wrapper) {
		$container = frm.fields_dict.grouped_projects_html.$wrapper;
	} else {
		$('#bir-grouped-container-in-form').remove();
		var $target = $(frm.wrapper).find('[data-fieldname="entries"], .form-page:visible').first();
		$container = $('<div id="bir-grouped-container-in-form" class="margin-top" style="margin-top:20px;"></div>');
		if ($target && $target.length) {
			$target.before($container);
		} else {
			$(frm.wrapper).append($container);
		}
	}

	$container.html('<div class="text-muted" style="padding:15px;background:#fff;border-radius:8px;border:1px solid #e2e8f0;"><i class="fa fa-spinner fa-spin"></i> جاري تحميل التقرير المجمّع لكافة المشاريع المرتبطة بالدفعة والمصرف...</div>');

	frappe.call({
		method: 'bir_waqf.api.get_grouped_transactions_by_projects',
		args: {
			import_batch: import_batch,
			bank: bank,
			projects: projects
		},
		callback: function(r) {
			if (!r.message || r.message.length === 0) {
				$container.html('<div class="alert alert-warning text-center">لا توجد معاملات تبرع مقترنة بالمشاريع للدفعة والمصرف المحددين.</div>');
				return;
			}

			var active_groups = r.message.filter(function(g) { return g.donations && g.donations.length > 0; });
			if (active_groups.length === 0) {
				active_groups = r.message;
			}

			var grand_total_amount = 0.0;
			var grand_total_count = 0;

			var html = `
				<div style="background:#fff;border:1px solid #E2E8F0;padding:15px;border-radius:8px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,0.03);">
					<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;">
						<h4 style="margin:0;color:#0A4D2E;font-weight:700;"><i class="fa fa-list-alt"></i> جدول كشف الحساب المجمّع حسب المشاريع (${active_groups.length} مشروع)</h4>
						<button class="btn btn-sm btn-success" id="btn-export-excel-in-form" style="font-weight:bold;"><i class="fa fa-file-excel-o"></i> تصدير كشف حساب المصرف (Excel)</button>
					</div>
			`;

			active_groups.forEach(function(g) {
				grand_total_amount += parseFloat(g.subtotal || 0.0);
				grand_total_count += (g.donations ? g.donations.length : 0);

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
									<th>مبلغ التبرع</th>
									<th style="text-align:center;">تاريخ المعاملة</th>
									<th style="width:100px;text-align:center;">تمت المطابقة</th>
								</tr>
							</thead>
							<tbody>
				`;

				if (g.donations.length === 0) {
					html += `<tr><td colspan="6" class="text-center text-muted">لا توجد تبرعات مسجلة لهذا المشروع.</td></tr>`;
				} else {
					g.donations.forEach(function(d, idx) {
						var chk = d.is_reconciled ? 'checked' : '';
						html += `
							<tr>
								<td style="text-align:center;">${idx + 1}</td>
								<td><b>${d.transaction_id}</b></td>
								<td>${d.transfer_number}</td>
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
									<td colspan="3" class="text-left">إجمالي تبرعات مشروع (${g.project_name}):</td>
									<td style="font-weight:bold;color:#92400E;">${parseFloat(g.subtotal).toFixed(2)} د.ل</td>
									<td colspan="2"></td>
								</tr>
							</tfoot>
						</table>
					</div>
				`;
			});

			// Grand Total Banner for Statement
			html += `
				<div style="background:#0A4D2E;color:#ffffff;padding:14px 20px;border-radius:8px;margin-top:15px;display:flex;justify-content:space-between;align-items:center;font-size:14px;font-weight:bold;box-shadow:0 3px 10px rgba(10,77,46,0.2);">
					<span>📊 إجمالي كافة مشاريع المصرف في هذه الدفعة (${active_groups.length} مشروع | ${grand_total_count} معاملة):</span>
					<span style="font-size:16px;color:#F1C40F;">${parseFloat(grand_total_amount).toFixed(2)} د.ل</span>
				</div>
			`;

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
