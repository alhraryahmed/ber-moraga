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
			<div class="col-md-3"><div class="bir-card"><small>إجمالي التبرعات (د.ل)</small><div class="bir-stat-num" id="st-amount" style="color:#D4AF37;">-</div></div></div>
			<div class="col-md-3"><div class="bir-card"><small>معاملات سلة</small><div class="bir-stat-num" id="st-basket" style="color:#2b6cb0;">-</div></div></div>
			<div class="col-md-3"><div class="bir-card"><small>استثناءات تحتاج مراجعة</small><div class="bir-stat-num" id="st-exceptions" style="color:#c53030;">-</div></div></div>
		</div>

		<div class="row margin-top">
			<div class="col-md-6">
				<div class="bir-card">
					<h4><i class="fa fa-upload"></i> رفع ومعالجة ملف منصة البر (Excel / CSV)</h4>
					<p class="text-muted">اختر ملف المعاملات المصدّر لمعالجته وتجميع السلات تلقائياً</p>
					<div id="file-upload-area" style="padding: 20px; border: 2px dashed #0A4D2E; text-align: center; border-radius: 8px;">
						<button class="btn bir-btn-primary" id="btn-upload-file"><i class="fa fa-folder-open"></i> اختيار الملف</button>
					</div>
					<div id="upload-result" class="margin-top"></div>
				</div>
			</div>
			<div class="col-md-6">
				<div class="bir-card">
					<h4><i class="fa fa-check-circle"></i> المطابقة المصرفية الآلية واليدوية</h4>
					<p class="text-muted">تشغيل محرك المطابقة بين الحوالات وكشوفات المصرف</p>
					<button class="btn btn-success btn-lg btn-block" id="btn-run-reconcile"><i class="fa fa-play"></i> تشغيل المطابقة الآلية الآن</button>
					<a class="btn btn-default btn-block margin-top" href="/app/bir-transaction"><i class="fa fa-list"></i> الانتقال لجدول المعاملات كاملة</a>
				</div>
			</div>
		</div>
	`);

	function load_stats() {
		frappe.call({
			method: 'bir_waqf.api.get_dashboard_stats',
			callback: function(r) {
				if(r.message) {
					$('#st-total').text(r.message.total_transactions);
					$('#st-amount').text(frappe.format(r.message.total_donations, {fieldtype: 'Currency'}));
					$('#st-basket').text(r.message.basket_count);
					$('#st-exceptions').text(r.message.exceptions_count);
				}
			}
		});
	}

	load_stats();

	$('#btn-upload-file').on('click', function() {
		new frappe.ui.FileUploader({
			method: 'upload_file',
			make_attachments_public: 1,
			on_success: function(file_doc) {
				frappe.show_alert({message: __('جاري معالجة الملف...'), indicator: 'blue'});
				frappe.call({
					method: 'bir_waqf.api.process_uploaded_file',
					args: { file_url: file_doc.file_url },
					callback: function(r) {
						if(r.message) {
							$('#upload-result').html(`
								<div class="alert alert-success">
									<strong>تمت المعالجة بنجاح!</strong><br>
									تم إدخال <b>${r.message.total_transactions}</b> معاملة (منها <b>${r.message.basket_transactions}</b> معاملة سلة).<br>
									عدد الاستثناءات: <b>${r.message.exceptions_count}</b>
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
		frappe.msgprint('جاري تنفيذ المطابقة بين السجلات وكشوف الحساب...');
	});
};
