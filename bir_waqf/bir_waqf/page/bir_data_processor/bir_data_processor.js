frappe.pages['bir_data_processor'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'مركز معالجة ومطابقة البر الوقفية',
		single_column: true
	});

	$(wrapper).find('.layout-main-section').html(`
		<style>
			.bir-waqf-header { background: linear-gradient(135deg, #0A4D2E 0%, #15803D 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(10, 77, 46, 0.15); }
			.bir-waqf-title { margin: 0 0 5px 0; font-size: 20px; font-weight: 700; color: #FFFFFF; }
			.bir-card { background: #ffffff; border: 1px solid #E2E8F0; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.03); }
			.bir-stat-num { font-size: 24px; font-weight: 800; color: #0A4D2E; margin-top: 5px; }
			.bir-btn-primary { background-color: #0A4D2E; color: white; border: none; padding: 10px 18px; border-radius: 6px; font-weight: 600; }
			.bir-btn-primary:hover { background-color: #073822; color: white; }
			.proj-group-card { background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 8px; margin-bottom: 20px; overflow: hidden; }
			.proj-group-header { background: #E6F4EA; border-bottom: 2px solid #0A4D2E; padding: 12px 18px; font-weight: 700; font-size: 15px; color: #0A4D2E; display: flex; justify-content: space-between; align-items: center; }
			.proj-subtotal-row { background: #FEF3C7; font-weight: 700; color: #92400E; }
			.rec-checkbox { width: 18px; height: 18px; cursor: pointer; accent-color: #0A4D2E; }
		</style>

		<div class="bir-waqf-header">
			<h2 class="bir-waqf-title"><i class="fa fa-university"></i> نظام البر الوقفية — معالجة البيانات والمطابقة المصرفية</h2>
			<p style="margin:0;opacity:0.9;">رفع وتصفية ملفات التبرعات والسلات والمطابقة الآلية والتصنيف حسب المشاريع</p>
		</div>

		<div class="row" id="bir-stats-row">
			<div class="col-md-3"><div class="bir-card"><small>إجمالي المعاملات</small><div class="bir-stat-num" id="st-total">-</div></div></div>
			<div class="col-md-3"><div class="bir-card"><small>إجمالي التبرعات</small><div class="bir-stat-num" id="st-amount" style="color:#D4AF37;">-</div></div></div>
			<div class="col-md-3"><div class="bir-card"><small>معاملات سلة</small><div class="bir-stat-num" id="st-basket" style="color:#2b6cb0;">-</div></div></div>
			<div class="col-md-3"><div class="bir-card"><small>دفعات الاستيراد</small><div class="bir-stat-num" id="st-batches" style="color:#805ad5;">-</div></div></div>
		</div>

		<!-- SECTION: UPLOAD & AUTO RECONCILE -->
		<div class="row">
			<div class="col-md-6">
				<div class="bir-card">
					<h4><i class="fa fa-upload"></i> رفع ملف واستجلاب دفعة جديدة (Excel / CSV)</h4>
					<p class="text-muted">اختر ملف المعاملات المصدّر لمعالجته وإنشاء دفعة استيراد رقمية</p>
					<div id="file-upload-area" style="padding: 20px; border: 2px dashed #0A4D2E; text-align: center; border-radius: 8px; background:#FAFBFD;">
						<button class="btn bir-btn-primary" id="btn-upload-file"><i class="fa fa-folder-open"></i> اختيار الملف والاستجلاب</button>
					</div>
					<div id="upload-result" class="margin-top"></div>
					<a class="btn btn-default btn-block margin-top" href="/app/bir-import-batch"><i class="fa fa-folder"></i> عرض سجل دفعات الاستيراد (Import Batches)</a>
				</div>
			</div>
			<div class="col-md-6">
				<div class="bir-card">
					<h4><i class="fa fa-check-circle"></i> المطابقة المصرفية الجماعية حسب الفترة</h4>
					<p class="text-muted">اختر فترة المطابقة لتشغيل جلب ومطابقة الحوالات جماعياً</p>
					<div class="row">
						<div class="col-md-6">
							<label>من تاريخ:</label>
							<input type="date" id="rec-from-date" class="form-control">
						</div>
						<div class="col-md-6">
							<label>إلى تاريخ:</label>
							<input type="date" id="rec-to-date" class="form-control">
						</div>
					</div>
					<button class="btn btn-success btn-lg btn-block margin-top" id="btn-run-reconcile"><i class="fa fa-play"></i> تشغيل المطابقة الآلية الجماعية</button>
					<a class="btn btn-default btn-block margin-top" href="/app/bir-transaction"><i class="fa fa-list"></i> الانتقال لجدول المعاملات كاملة</a>
				</div>
			</div>
		</div>

		<!-- SECTION: BANK STATEMENT QUICK ENTRY BY PROJECTS -->
		<div class="row margin-top">
			<div class="col-md-12">
				<div class="bir-card">
					<h4><i class="fa fa-bank"></i> شاشة "تضمين المصرف" وتصفية المعاملات حسب المشاريع</h4>
					<p class="text-muted">حدد الدفعة، ثم المصرف، ثم اختبر مشروعاً أو أكثر لتجميع التبرعات وتحديث حالة المطابقة فورياً</p>

					<div class="row">
						<div class="col-md-4">
							<label>1. اختر دفعة الاستيراد (Batch):</label>
							<div id="ctrl-batch"></div>
						</div>
						<div class="col-md-4">
							<label>2. اختر المصرف (Bank):</label>
							<div id="ctrl-bank"></div>
						</div>
						<div class="col-md-4">
							<label>3. اختر المشاريع المرادة (Multi-Select Projects):</label>
							<div id="ctrl-projects"></div>
						</div>
					</div>

					<div class="margin-top text-right">
						<button class="btn btn-primary" id="btn-load-grouped-table"><i class="fa fa-search"></i> عرض وتصفية المعاملات</button>
						<button class="btn btn-success" id="btn-export-grouped-excel" style="display:none;"><i class="fa fa-file-excel-o"></i> تصدير كشف حساب المصرف (Excel)</button>
					</div>

					<div id="grouped-projects-container" class="margin-top"></div>
				</div>
			</div>
		</div>

		<!-- Modal for Progress Bar -->
		<div class="modal fade" id="bir-progress-modal" tabindex="-1" role="dialog" data-backdrop="static">
			<div class="modal-dialog modal-dialog-centered" role="document">
				<div class="modal-content" style="border-radius: 12px;">
					<div class="modal-header" style="background-color: #0A4D2E; color: #fff; border-top-left-radius: 12px; border-top-right-radius: 12px;">
						<h5 class="modal-title" id="bir-progress-title"><i class="fa fa-spinner fa-spin"></i> جاري المعالجة والمطابقة...</h5>
					</div>
					<div class="modal-body text-center" style="padding: 30px;">
						<p id="bir-progress-msg" style="font-size: 16px; font-weight: bold; color: #333;">جاري المعالجة...</p>
						<div class="progress" style="height: 25px; border-radius: 12px; background-color: #e9ecef;">
							<div id="bir-progress-bar" class="progress-bar progress-bar-striped progress-bar-animated bg-success" role="progressbar" style="width: 0%; font-size: 14px; font-weight: bold; line-height: 25px;">0%</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	`);

	function format_cur(amount) {
		if (!amount) return '0.00 د.ل';
		return parseFloat(amount).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' د.ل';
	}

	function load_stats() {
		frappe.call({
			method: 'bir_waqf.api.get_dashboard_stats',
			callback: function(r) {
				if(r.message) {
					$('#st-total').text(r.message.total_transactions);
					$('#st-amount').text(format_cur(r.message.total_donations));
					$('#st-basket').text(r.message.basket_count);
					$('#st-batches').text(r.message.batches_count);
				}
			}
		});
	}

	load_stats();

	// Initialize Controls: Batch, Bank, Projects (MultiSelect)
	var field_batch = frappe.ui.form.make_control({
		df: {
			fieldtype: 'Link',
			options: 'Bir Import Batch',
			fieldname: 'batch_filter',
			placeholder: 'اختر الدفعة...'
		},
		parent: $('#ctrl-batch'),
		only_input: true
	});
	field_batch.make();

	var field_bank = frappe.ui.form.make_control({
		df: {
			fieldtype: 'Link',
			options: 'Bank',
			fieldname: 'bank_filter',
			placeholder: 'اختر المصرف...'
		},
		parent: $('#ctrl-bank'),
		only_input: true
	});
	field_bank.make();

	var field_projects = frappe.ui.form.make_control({
		df: {
			fieldtype: 'MultiSelect',
			options: 'Project',
			fieldname: 'projects_filter',
			placeholder: 'اختر مشروعات...'
		},
		parent: $('#ctrl-projects'),
		only_input: true
	});
	field_projects.make();

	function show_progress(title, msg, start_percent) {
		$('#bir-progress-title').html('<i class="fa fa-spinner fa-spin"></i> ' + title);
		$('#bir-progress-msg').text(msg);
		$('#bir-progress-bar').css('width', start_percent + '%').text(start_percent + '%');
		$('#bir-progress-modal').modal('show');
	}

	function update_progress(percent, msg) {
		$('#bir-progress-bar').css('width', percent + '%').text(percent + '%');
		if(msg) $('#bir-progress-msg').text(msg);
	}

	function hide_progress() {
		setTimeout(function() {
			$('#bir-progress-modal').modal('hide');
		}, 600);
	}

	$('#btn-upload-file').on('click', function() {
		new frappe.ui.FileUploader({
			make_attachments_public: 1,
			on_success: function(file_doc) {
				show_progress('جاري معالجة واستجلاب الملف', 'جاري تفكيك ملف الإكسل وتجميع السلات بالـ ID وربط المشاريع...', 15);
				
				var p_timer = setInterval(function() {
					var cur = parseInt($('#bir-progress-bar').text());
					if(cur < 85) update_progress(cur + 15, 'جاري حفظ المعاملات وإنشاء الدفعة...');
				}, 400);

				frappe.call({
					method: 'bir_waqf.api.process_uploaded_file',
					args: { file_url: file_doc.file_url },
					callback: function(r) {
						clearInterval(p_timer);
						update_progress(100, 'تمت المعالجة بنجاح!');
						hide_progress();
						if(r.message) {
							$('#upload-result').html(`
								<div class="alert alert-success margin-top">
									<strong>تمت المعالجة وإنشاء الدفعة وربط المشاريع بنجاح!</strong><br>
									رقم الدفعة المعرّف (ID): <a href="/app/bir-import-batch/${r.message.batch_id}"><b>${r.message.batch_id}</b></a><br>
									تم إدخال <b>${r.message.total_transactions}</b> معاملة (منها <b>${r.message.basket_transactions}</b> معاملة سلة).<br>
									إجمالي التبرعات: <b>${format_cur(r.message.total_donations)}</b>
								</div>
							`);
							load_stats();
						}
					}
				});
			}
		});
	});

	$('#btn-run-reconcile').on('click', function() {
		var f_date = $('#rec-from-date').val();
		var t_date = $('#rec-to-date').val();

		show_progress('جاري المطابقة المصرفية الجماعية', 'جاري مطابقة أرقام الحوالات والمبالغ مع كشف الحساب المصرفي...', 20);

		var r_timer = setInterval(function() {
			var cur = parseInt($('#bir-progress-bar').text());
			if(cur < 85) update_progress(cur + 20, 'جاري البحث وتحديث المعاملات المطابقة...');
		}, 300);

		frappe.call({
			method: 'bir_waqf.api.run_auto_reconciliation',
			args: { from_date: f_date, to_date: t_date },
			callback: function(r) {
				clearInterval(r_timer);
				update_progress(100, 'تمت المطابقة المصرفية بنجاح!');
				hide_progress();
				if(r.message) {
					frappe.msgprint(__('تمت عملية المطابقة الجماعية: تم مطابقة {0} معاملة جديدة بقيمة إجمالية {1}.', [r.message.matched_count, format_cur(r.message.matched_amount)]));
					load_stats();
				}
			}
		});
	});

	// Load Grouped Transactions by Project
	$('#btn-load-grouped-table').on('click', function() {
		var batch_val = field_batch.get_value();
		var bank_val = field_bank.get_value();
		var projects_val = field_projects.get_value();

		if (!projects_val) {
			frappe.msgprint(__('يرجى اختيار مشروع واحد على الأقل للتصفية والتجميع.'));
			return;
		}

		frappe.show_alert({message: __('جاري تجميع التبرعات حسب المشاريع...'), indicator: 'blue'});

		frappe.call({
			method: 'bir_waqf.api.get_grouped_transactions_by_projects',
			args: {
				import_batch: batch_val,
				bank: bank_val,
				projects: projects_val
			},
			callback: function(r) {
				if (r.message) {
					render_grouped_projects_table(r.message);
					$('#btn-export-grouped-excel').show();
				}
			}
		});
	});

	function render_grouped_projects_table(groups) {
		var $c = $('#grouped-projects-container').empty();

		if (!groups || groups.length === 0) {
			$c.html('<div class="alert alert-warning text-center">لا توجد معاملات تبرع مقترنة بالمشاريع المختارة.</div>');
			return;
		}

		groups.forEach(function(g) {
			var html = `
				<div class="proj-group-card">
					<div class="proj-group-header">
						<span>📌 مشروع: ${g.project_name}</span>
						<span class="badge badge-success" style="font-size:12px;">عدد التبرعات: ${g.donations.length}</span>
					</div>
					<table class="table table-bordered table-hover" style="margin-bottom:0;font-size:13px;">
						<thead style="background:#1E293B;color:#fff;">
							<tr>
								<th style="width:40px;text-align:center;">#</th>
								<th>رقم المعاملة</th>
								<th>رقم الحوالة / الصك</th>
								<th>المستخدم / المتبرع</th>
								<th>مبلغ التبرع</th>
								<th style="text-align:center;">تاريخ المعاملة</th>
								<th style="width:110px;text-align:center;">تمت المطابقة</th>
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
							<td style="font-weight:bold;color:#0A4D2E;">${format_cur(d.amount)}</td>
							<td style="text-align:center;">${d.transaction_date}</td>
							<td style="text-align:center;">
								<input type="checkbox" class="rec-checkbox" data-tx-name="${d.name}" ${chk}>
							</td>
						</tr>
					`;
				});
			}

			html += `
						</tbody>
						<tfoot>
							<tr class="proj-subtotal-row">
								<td colspan="4" class="text-left">إجمالي تبرعات مشروع (${g.project_name}):</td>
								<td style="font-weight:bold;font-size:14px;color:#92400E;">${format_cur(g.subtotal)}</td>
								<td colspan="2"></td>
							</tr>
						</tfoot>
					</table>
				</div>
			`;

			$c.append(html);
		});

		// Bind Checkbox click to toggle_transaction_reconciliation API
		$c.find('.rec-checkbox').on('change', function() {
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
	}

	// Export Grouped Bank Statement Excel
	$('#btn-export-grouped-excel').on('click', function() {
		var batch_val = field_batch.get_value();
		var bank_val = field_bank.get_value();
		var projects_val = field_projects.get_value();

		frappe.show_alert({message: __('جاري إنشاء وتوليد كشف حساب المصرف Excel...'), indicator: 'blue'});

		frappe.call({
			method: 'bir_waqf.api.export_grouped_bank_statement_excel',
			args: {
				import_batch: batch_val,
				bank: bank_val,
				projects: projects_val
			},
			callback: function(r) {
				if (r.message && r.message.file_url) {
					window.open(r.message.file_url, '_blank');
				}
			}
		});
	});
};
