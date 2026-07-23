frappe.pages['bir_data_processor'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'مركز معالجة ومطابقة البر الوقفية',
		single_column: true
	});

	$(wrapper).find('.layout-main-section').html(`
		<div class="bir-waqf-header">
			<h2 class="bir-waqf-title"><i class="fa fa-university"></i> نظام البر الوقفية — معالجة البيانات والمطابقة المصرفية</h2>
			<p>رفع وتصفية ملفات التبرعات والسلات والمطابقة الآلية مع كشف الحساب المصرفي</p>
		</div>

		<div class="row" id="bir-stats-row">
			<div class="col-md-3"><div class="bir-card"><small>إجمالي المعاملات</small><div class="bir-stat-num" id="st-total">-</div></div></div>
			<div class="col-md-3"><div class="bir-card"><small>إجمالي التبرعات</small><div class="bir-stat-num" id="st-amount" style="color:#D4AF37;">-</div></div></div>
			<div class="col-md-3"><div class="bir-card"><small>معاملات سلة</small><div class="bir-stat-num" id="st-basket" style="color:#2b6cb0;">-</div></div></div>
			<div class="col-md-3"><div class="bir-card"><small>دفعات الاستيراد</small><div class="bir-stat-num" id="st-batches" style="color:#805ad5;">-</div></div></div>
		</div>

		<div class="row margin-top">
			<div class="col-md-6">
				<div class="bir-card">
					<h4><i class="fa fa-upload"></i> رفع ملف واستجلاب دفعة جديدة (Excel / CSV)</h4>
					<p class="text-muted">اختر ملف المعاملات المصدّر لمعالجته وإنشاء دفعة استيراد رقمية لها ID فريد</p>
					<div id="file-upload-area" style="padding: 20px; border: 2px dashed #0A4D2E; text-align: center; border-radius: 8px;">
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

		<!-- Modal for Progress Bar -->
		<div class="modal fade" id="bir-progress-modal" tabindex="-1" role="dialog" data-backdrop="static">
			<div class="modal-dialog modal-dialog-centered" role="document">
				<div class="modal-content" style="border-radius: 12px;">
					<div class="modal-header" style="background-color: #0A4D2E; color: #fff; border-top-left-radius: 12px; border-top-right-radius: 12px;">
						<h5 class="modal-title" id="bir-progress-title"><i class="fa fa-spinner fa-spin"></i> جاري المعالجة والمطابقة...</h5>
					</div>
					<div class="modal-body text-center" style="padding: 30px;">
						<p id="bir-progress-msg" style="font-size: 16px; font-weight: bold; color: #333;">جاري قراءة الملف وتفكيك السلات...</p>
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
				show_progress('جاري معالجة واستجلاب الملف', 'جاري تفكيك ملف الإكسل وتجميع السلات بالـ ID...', 15);
				
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
									<strong>تمت المعالجة وإنشاء الدفعة بنجاح!</strong><br>
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
};
