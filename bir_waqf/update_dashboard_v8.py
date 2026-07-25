import frappe

def run():
    block_name = "Bir Waqf Dashboard Block"
    if not frappe.db.exists("Custom HTML Block", block_name):
        doc = frappe.new_doc("Custom HTML Block")
        doc.name = block_name
    else:
        doc = frappe.get_doc("Custom HTML Block", block_name)

    doc.html = """<!-- لوحة منصة البر الوقفية — v8 تصميم مودرن كلاسيك نظيف ومريح للعين مع تصفية فورية حقيقية -->
<div class="bir-v8-dashboard" dir="rtl" lang="ar">
  
  <!-- الشريط العلوي الهادئ الكلاسيكي بشعار فخم -->
  <header class="bir-v8-header">
    <div class="bir-v8-brand">
      <div class="bir-v8-logo-card">
        <img src="/files/Screenshot 2026-07-23 013547.png" alt="شعار منصة البر الوقفية" class="bir-v8-logo-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
        <div class="bir-v8-logo-fallback" style="display:none;">
          <svg viewBox="0 0 24 24" width="42" height="42" fill="currentColor"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
        </div>
      </div>

      <div class="bir-v8-titles">
        <div class="bir-v8-org-tag">
          <svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><path d="M12 2L3 7v10l9 5 9-5V7l-9-5zm0 2.2L19 8v8l-7 3.9L5 16V8l7-3.8z"/></svg>
          <span>الهيئة العامة للأوقاف والشؤون الإسلامية</span>
        </div>
        <h1 class="bir-v8-main-title">منصة البِرّ الوقفية <span class="bir-v8-gold-txt">| مركز المعالجة والمطابقة المصرفية</span></h1>
        <p class="bir-v8-sub-title">منظومة الإدارة الذكية للتبرعات ومساهمات السلة والمطابقة الآلية لكشوف الحسابات</p>
      </div>
    </div>

    <div class="bir-v8-meta">
      <div class="bir-v8-live-chip">
        <span class="bir-v8-pulse"></span>
        <span>النظام متصل ونشط</span>
      </div>
      <div class="bir-v8-clock-box">
        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        <span class="bir-v8-clock">--:--:--</span>
      </div>
    </div>
  </header>

  <!-- شبكة الكروت الأحصائية الكلاسيكية المودرن (تصفية فورية للقائمة المعروضة عند النقر) -->
  <section class="bir-v8-kpi-grid">
    
    <!-- 1. إجمالي التبرعات والمساهمات -->
    <div class="bir-v8-card" onclick="openBirFilteredList('Bir Transaction', {}, 'جميع التبرعات والمساهمات', 'creation', 'desc');" title="انقر لفتح واستعراض جميع المعاملات">
      <div class="bir-v8-card-head">
        <span class="bir-v8-card-title">إجمالي التبرعات والمساهمات</span>
        <div class="bir-v8-card-icon icon-emerald">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12V7H3v10h11"/><path d="M18 15t3 3m0 0l-3 3m3-3h-6"/></svg>
        </div>
      </div>
      <div class="bir-v8-value val-total-amount">0.00 <small>د.ل</small></div>
      <div class="bir-v8-card-footer">
        <span class="val-total-count">0 معاملة مدخلة</span>
        <span class="bir-v8-filter-action">استعراض السجل ➔</span>
      </div>
    </div>

    <!-- 2. المعاملات المطابقة مصرفياً -->
    <div class="bir-v8-card" onclick="openBirFilteredList('Bir Transaction', {reconciliation_status: ['in', ['مطابق آليًا', 'مطابق يدويًا']]}, 'المعاملات المطابقة مصرفياً', 'creation', 'desc');" title="انقر لعرض المعاملات المطابقة مصرفياً فقط">
      <div class="bir-v8-card-head">
        <span class="bir-v8-card-title">المعاملات المطابقة مصرفياً</span>
        <div class="bir-v8-card-icon icon-gold">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        </div>
      </div>
      <div class="bir-v8-value val-matched-count">0</div>
      <div class="bir-v8-progress-bar"><div class="bir-v8-progress-fill val-matched-progress" style="width: 0%;"></div></div>
      <div class="bir-v8-card-footer">
        <span class="val-matched-pct">0% نسبة المطابقة</span>
        <span class="bir-v8-filter-action">تصفية المطابق ➔</span>
      </div>
    </div>

    <!-- 3. المعاملات المدخلة بالنظام -->
    <div class="bir-v8-card" onclick="openBirFilteredList('Bir Transaction', {}, 'المعاملات المدخلة بالنظام', 'creation', 'desc');" title="انقر لعرض المعاملات المدخلة">
      <div class="bir-v8-card-head">
        <span class="bir-v8-card-title">المعاملات المدخلة بالنظام</span>
        <div class="bir-v8-card-icon icon-blue">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>
        </div>
      </div>
      <div class="bir-v8-value val-transactions-input">0</div>
      <div class="bir-v8-card-footer">
        <span>إجمالي القيود بالمنظومة</span>
        <span class="bir-v8-filter-action">تصفية المدخلات ➔</span>
      </div>
    </div>

    <!-- 4. معاملات الاستثناء -->
    <div class="bir-v8-card" onclick="openBirFilteredList('Bir Transaction', {has_exception: 1}, 'معاملات الاستثناء', 'creation', 'desc');" title="انقر لعرض معاملات الاستثناء التي تتطلب مراجعة">
      <div class="bir-v8-card-head">
        <span class="bir-v8-card-title">معاملات الاستثناء</span>
        <div class="bir-v8-card-icon icon-amber">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        </div>
      </div>
      <div class="bir-v8-value val-exceptions-count">0</div>
      <div class="bir-v8-card-footer">
        <span style="color:#D35400;font-weight:600;">تتطلب مراجعة تدقيقية</span>
        <span class="bir-v8-filter-action" style="color:#D35400;">تصفية الاستثناءات ➔</span>
      </div>
    </div>

    <!-- 5. أعلى قيمة لمساهمة واحدة -->
    <div class="bir-v8-card" onclick="openBirFilteredList('Bir Transaction', {is_basket: 0}, 'أعلى قيمة لمساهمة واحدة', 'total_amount', 'desc');" title="انقر لعرض المساهمات الفردية مرتبة من الأكبر إلى الأصغر">
      <div class="bir-v8-card-head">
        <span class="bir-v8-card-title">أعلى قيمة لمساهمة واحدة</span>
        <div class="bir-v8-card-icon icon-purple">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2z"/></svg>
        </div>
      </div>
      <div class="bir-v8-value val-max-single">0.00 <small>د.ل</small></div>
      <div class="bir-v8-card-footer">
        <span>مساهمة فردية قياسية</span>
        <span class="bir-v8-filter-action">ترتيب حسب القيمة ➔</span>
      </div>
    </div>

    <!-- 6. أعلى قيمة لمساهمة السلة -->
    <div class="bir-v8-card" onclick="openBirFilteredList('Bir Transaction', {is_basket: 1}, 'أعلى قيمة لمساهمة السلة', 'total_amount', 'desc');" title="انقر لعرض معاملات سلة المشاريع مرتبة من الأكبر إلى الأصغر">
      <div class="bir-v8-card-head">
        <span class="bir-v8-card-title">أعلى قيمة لمساهمة السلة</span>
        <div class="bir-v8-card-icon icon-teal">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
        </div>
      </div>
      <div class="bir-v8-value val-max-basket">0.00 <small>د.ل</small></div>
      <div class="bir-v8-card-footer">
        <span class="val-basket-count-sub">معاملات سلة المشاريع</span>
        <span class="bir-v8-filter-action">ترتيب حسب القيمة ➔</span>
      </div>
    </div>

  </section>

  <!-- التخطيط السفلي المريح -->
  <div class="bir-v8-layout">
    
    <!-- مداخل دوكتايبات المنظومة -->
    <section class="bir-v8-panel">
      <div class="bir-v8-panel-header">
        <h3 class="bir-v8-panel-title">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#C5A059" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          <span>مداخل سجلات ودوكتايبات المنظومة</span>
        </h3>
        <span class="bir-v8-sub-tag">وصول مباشر ونظيف</span>
      </div>

      <div class="bir-v8-nav-grid">
        
        <button class="bir-v8-nav-item primary" onclick="frappe.set_route('bir_data_processor');">
          <div class="bir-v8-nav-icon"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/><path d="M12 13v6m-3-3l3-3 3 3"/></svg></div>
          <div class="bir-v8-nav-content">
            <strong>مركز معالجة البيانات والمطابقة</strong>
            <span>رفع ومعالجة كشوف المنصة والبنك</span>
          </div>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" class="bir-v8-nav-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

        <button class="bir-v8-nav-item" onclick="openBirFilteredList('Bir Transaction', {}, 'جدول المعاملات', 'creation', 'desc');">
          <div class="bir-v8-nav-icon"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg></div>
          <div class="bir-v8-nav-content">
            <strong>جدول المعاملات وتضمين المصرف</strong>
            <span>استعراض المعاملات وتحديث المصارف</span>
          </div>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" class="bir-v8-nav-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

        <button class="bir-v8-nav-item" onclick="openBirFilteredList('Bir Bank Statement', {}, 'كشوف الحسابات المصرفية', 'creation', 'desc');">
          <div class="bir-v8-nav-icon"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M3 10h18M5 6l7-3 7 3M4 10v11M20 10v11M8 14v3M12 14v3M16 14v3"/></svg></div>
          <div class="bir-v8-nav-content">
            <strong>كشوف الحسابات المصرفية</strong>
            <span>متابعة كشوف الحسابات والبنود</span>
          </div>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" class="bir-v8-nav-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

        <button class="bir-v8-nav-item" onclick="openBirFilteredList('Bir Bank Statement Entry', {}, 'بنود كشوف الحساب المصرفي', 'creation', 'desc');">
          <div class="bir-v8-nav-icon"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div>
          <div class="bir-v8-nav-content">
            <strong>بنود كشوف الحساب المصرفي</strong>
            <span>عرض قيود كشف الحساب والعمليات</span>
          </div>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" class="bir-v8-nav-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

        <button class="bir-v8-nav-item" onclick="openBirFilteredList('Bank', {}, 'دليل المصارف المعتمدة');">
          <div class="bir-v8-nav-icon"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg></div>
          <div class="bir-v8-nav-content">
            <strong>المصارف المعتمدة</strong>
            <span>دليل البنوك (مصرف الجمهورية،...)</span>
          </div>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" class="bir-v8-nav-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

        <button class="bir-v8-nav-item" onclick="openBirFilteredList('Bir Import Batch', {}, 'دفعات استيراد البيانات', 'creation', 'desc');">
          <div class="bir-v8-nav-icon"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg></div>
          <div class="bir-v8-nav-content">
            <strong>دفعات استيراد البيانات</strong>
            <span>أرشيف وسجل الدفعات المستوردة</span>
          </div>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" class="bir-v8-nav-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

      </div>
    </section>

    <!-- قسم أعلى المشاريع الوقفية -->
    <section class="bir-v8-panel">
      <div class="bir-v8-panel-header">
        <h3 class="bir-v8-panel-title">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#C5A059" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
          <span>أعلى المشاريع الوقفية</span>
        </h3>
        <span class="bir-v8-sub-tag">حسب القيمة</span>
      </div>

      <div class="bir-v8-projects-list">
        <div class="bir-v8-loading">
          <div class="bir-v8-spinner"></div>
          <span>جاري جلب إحصائيات المشاريع...</span>
        </div>
      </div>
    </section>

  </div>

</div>
"""

    doc.script = """// Robust Filtered List Opener Script for Bir Waqf Dashboard Block v8
window.openBirFilteredList = function(doctype, filters, filterName, sort_field, sort_order) {
    if (typeof frappe === 'undefined') return;

    // Set route options for global navigation
    frappe.route_options = Object.assign({}, filters || {});

    function applyFiltersToListView(listview) {
        if (!listview || !listview.filter_area) return;
        
        // Clear all existing filters in listview
        listview.filter_area.clear().then(function() {
            if (filters && Object.keys(filters).length > 0) {
                for (var key in filters) {
                    var val = filters[key];
                    if (Array.isArray(val) && val[0] === 'in') {
                        listview.filter_area.add(doctype, key, 'in', val[1]);
                    } else {
                        listview.filter_area.add(doctype, key, '=', val);
                    }
                }
            }
            if (sort_field) {
                listview.sort_by = sort_field;
                listview.sort_order = sort_order || 'desc';
            }
            listview.refresh();
        });
    }

    var route = frappe.get_route();
    if (route && route[0] === 'List' && route[1] === doctype) {
        var listview = frappe.views.listview_instances[doctype];
        if (listview) {
            applyFiltersToListView(listview);
            if (filterName && frappe.show_alert) {
                frappe.show_alert({
                    message: __('تم تصفية القائمة المعروضة حسب: ') + filterName,
                    indicator: 'green'
                }, 4);
            }
            return;
        }
    }

    frappe.set_route('List', doctype).then(function() {
        setTimeout(function() {
            var listview = frappe.views.listview_instances[doctype];
            if (listview) {
                applyFiltersToListView(listview);
            }
        }, 400);
    });

    if (filterName && frappe.show_alert) {
        frappe.show_alert({
            message: __('جاري فتح القائمة المفلترة: ') + filterName,
            indicator: 'green'
        }, 4);
    }
};

(function(wrapper) {
	if (!wrapper) wrapper = document;

	function renderClock() {
		var now = new Date();
		var clock = wrapper.querySelector('.bir-v8-clock');
		if (clock) {
			clock.innerText = now.toLocaleTimeString('ar-LY', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
		}
	}
	setInterval(renderClock, 1000);
	renderClock();

	function fetchStats() {
		frappe.call({
			method: 'bir_waqf.api.get_dashboard_stats',
			callback: function(r) {
				if (r && r.message) {
					var stats = r.message;

					// 1. Total Amount
					var amtEl = wrapper.querySelector('.val-total-amount');
					if (amtEl) {
						var val = (stats.total_donations || 0).toLocaleString('ar-LY', {minimumFractionDigits:2, maximumFractionDigits:2});
						amtEl.innerHTML = val + ' <small>د.ل</small>';
					}

					// 2. Total Count
					var cntEl = wrapper.querySelector('.val-total-count');
					if (cntEl) {
						cntEl.innerText = (stats.total_transactions || 0).toLocaleString('ar-LY') + ' معاملة مدخلة';
					}

					// 3. Transactions Input
					var inputEl = wrapper.querySelector('.val-transactions-input');
					if (inputEl) {
						inputEl.innerText = (stats.total_transactions || 0).toLocaleString('ar-LY');
					}

					// 4. Matched Count & Pct
					var matchEl = wrapper.querySelector('.val-matched-count');
					if (matchEl) {
						matchEl.innerText = (stats.matched_transactions || 0).toLocaleString('ar-LY');
					}
					var pct = stats.total_transactions > 0 ? Math.round((stats.matched_transactions / stats.total_transactions) * 100) : 0;
					var pctEl = wrapper.querySelector('.val-matched-pct');
					if (pctEl) {
						pctEl.innerText = pct + '% نسبة المطابقة';
					}
					var prgEl = wrapper.querySelector('.val-matched-progress');
					if (prgEl) {
						prgEl.style.width = pct + '%';
					}

					// 5. Exceptions
					var excEl = wrapper.querySelector('.val-exceptions-count');
					if (excEl) {
						excEl.innerText = (stats.exceptions_count || 0).toLocaleString('ar-LY');
					}

					// 6. Max Single
					var maxSingleEl = wrapper.querySelector('.val-max-single');
					if (maxSingleEl) {
						var msVal = (stats.max_single || 0).toLocaleString('ar-LY', {minimumFractionDigits:2, maximumFractionDigits:2});
						maxSingleEl.innerHTML = msVal + ' <small>د.ل</small>';
					}

					// 7. Max Basket
					var maxBasketEl = wrapper.querySelector('.val-max-basket');
					if (maxBasketEl) {
						var mbVal = (stats.max_basket || 0).toLocaleString('ar-LY', {minimumFractionDigits:2, maximumFractionDigits:2});
						maxBasketEl.innerHTML = mbVal + ' <small>د.ل</small>';
					}

					var bskSubEl = wrapper.querySelector('.val-basket-count-sub');
					if (bskSubEl) {
						bskSubEl.innerText = (stats.basket_count || 0).toLocaleString('ar-LY') + ' معاملة سلة بالمشاريع';
					}

					// 8. Top Projects List
					var projContainer = wrapper.querySelector('.bir-v8-projects-list');
					if (projContainer) {
						if (stats.top_projects && stats.top_projects.length > 0) {
							var projHtml = '';
							stats.top_projects.forEach(function(p, idx) {
								var rankBadge = '<span class="bir-v8-rank">#' + (idx + 1) + '</span>';
								var pVal = (p.total || 0).toLocaleString('ar-LY', {minimumFractionDigits:2, maximumFractionDigits:2});
								projHtml += '<div class="bir-v8-proj-row">' +
									'<div class="bir-v8-proj-info">' + rankBadge + '<span class="bir-v8-proj-title">' + (p.project_name || 'مشروع وقفي') + '</span></div>' +
									'<div class="bir-v8-proj-amount">' + pVal + ' <small>د.ل</small></div>' +
								'</div>';
							});
							projContainer.innerHTML = projHtml;
						} else {
							projContainer.innerHTML = '<div class="bir-v8-empty">لا توجد بيانات مشاريع سلة حالياً</div>';
						}
					}
				}
			}
		});
	}

	setTimeout(fetchStats, 100);
})(typeof root_element !== 'undefined' ? root_element : document);
"""

    doc.style = """/* ---------------------------------------------------
 * تصميم مودرن كلاسيك نظيف ومريح للعين v8 — منصة البر الوقفية
 * Clean Classic & Restful Aesthetic | Emerald (#09382B) & Warm Gold (#C5A059)
 * --------------------------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@700&family=Tajawal:wght@400;500;600;700;800&display=swap');

.bir-v8-dashboard {
  direction: rtl;
  font-family: 'Tajawal', -apple-system, BlinkMacSystemFont, sans-serif;
  color: #1F2D26;
  background: #F6F8F6;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
}

/* Header Banner — مودرن كلاسيك راقي */
.bir-v8-header {
  background: linear-gradient(135deg, #09382B 0%, #114F3D 100%);
  border-radius: 14px;
  padding: 20px 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #ffffff;
  box-shadow: 0 4px 18px rgba(9, 56, 43, 0.12);
  border: 1px solid rgba(197, 160, 89, 0.35);
  margin-bottom: 20px;
}

.bir-v8-brand {
  display: flex;
  align-items: center;
  gap: 18px;
}

.bir-v8-logo-card {
  width: 100px;
  height: 75px;
  border-radius: 12px;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px 10px;
  border: 1.5px solid #C5A059;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.bir-v8-logo-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.bir-v8-org-tag {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 600;
  color: #E2C485;
  background: rgba(197, 160, 89, 0.15);
  padding: 3px 10px;
  border-radius: 10px;
  border: 1px solid rgba(197, 160, 89, 0.3);
  margin-bottom: 6px;
}

.bir-v8-main-title {
  font-family: 'Amiri', serif;
  font-size: 24px;
  font-weight: 700;
  margin: 0;
  color: #ffffff;
}
.bir-v8-gold-txt {
  color: #E2C485;
  font-family: 'Tajawal', sans-serif;
  font-size: 16.5px;
  font-weight: 600;
}
.bir-v8-sub-title {
  font-size: 12.5px;
  color: #D1E3DB;
  margin: 4px 0 0 0;
}

.bir-v8-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.bir-v8-live-chip {
  display: flex;
  align-items: center;
  gap: 7px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.18);
  padding: 5px 14px;
  border-radius: 16px;
  font-size: 11.5px;
  color: #92F7B6;
  font-weight: 600;
}

.bir-v8-pulse {
  width: 7px;
  height: 7px;
  background: #2ECC71;
  border-radius: 50%;
  box-shadow: 0 0 6px #2ECC71;
}

.bir-v8-clock-box {
  font-size: 13.5px;
  font-weight: 700;
  color: #E2C485;
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(0,0,0,0.2);
  padding: 4px 12px;
  border-radius: 8px;
  border: 1px solid rgba(197, 160, 89, 0.25);
}

/* KPI Grid — كروت أنيقة ومريحة للعين */
.bir-v8-kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

@media (max-width: 1024px) {
  .bir-v8-kpi-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .bir-v8-kpi-grid { grid-template-columns: 1fr; }
}

.bir-v8-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 18px 20px;
  border: 1px solid #E2E8E4;
  box-shadow: 0 2px 8px rgba(0,0,0,0.025);
  cursor: pointer;
  transition: all 0.22s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.bir-v8-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(9, 56, 43, 0.08);
  border-color: #C5A059;
}

.bir-v8-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}
.bir-v8-card-title {
  font-size: 13px;
  font-weight: 700;
  color: #2D3E36;
}

.bir-v8-card-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.icon-emerald { background: #EBF4EF; color: #09382B; }
.icon-gold { background: #FAF5E8; color: #B58D28; }
.icon-blue { background: #EDF5FA; color: #2980B9; }
.icon-amber { background: #FDF4EB; color: #D35400; }
.icon-purple { background: #F5EEF8; color: #8E44AD; }
.icon-teal { background: #EBF7F5; color: #16A085; }

.bir-v8-value {
  font-family: 'Amiri', serif;
  font-size: 25px;
  font-weight: 700;
  color: #09382B;
  margin: 2px 0 8px 0;
  line-height: 1;
}
.bir-v8-value small {
  font-family: 'Tajawal', sans-serif;
  font-size: 12px;
  color: #C5A059;
  font-weight: 700;
}

.bir-v8-progress-bar {
  height: 4px;
  background: #EAEFEB;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 8px;
}
.bir-v8-progress-fill {
  height: 100%;
  background: #C5A059;
  border-radius: 2px;
  transition: width 0.5s ease;
}

.bir-v8-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 11px;
  color: #6B7C73;
  padding-top: 8px;
  border-top: 1px solid #F0F4F2;
}

.bir-v8-filter-action {
  font-weight: 700;
  color: #09382B;
  transition: transform 0.2s ease;
}
.bir-v8-card:hover .bir-v8-filter-action {
  transform: translateX(-3px);
  color: #C5A059;
}

/* Layout */
.bir-v8-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 16px;
}
@media (max-width: 992px) {
  .bir-v8-layout { grid-template-columns: 1fr; }
}

.bir-v8-panel {
  background: #ffffff;
  border-radius: 14px;
  padding: 18px 20px;
  border: 1px solid #E2E8E4;
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
}

.bir-v8-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1.5px solid #F0F4F2;
}
.bir-v8-panel-title {
  font-size: 14px;
  font-weight: 700;
  color: #09382B;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}
.bir-v8-sub-tag {
  font-size: 10.5px;
  font-weight: 600;
  color: #C5A059;
  background: #FAF5E8;
  padding: 3px 10px;
  border-radius: 8px;
}

/* Navigation Grid */
.bir-v8-nav-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 12px;
}

.bir-v8-nav-item {
  background: #F9FAF8;
  border: 1px solid #E2E8E4;
  border-radius: 10px;
  padding: 12px 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  text-align: right;
  transition: all 0.2s ease;
}
.bir-v8-nav-item.primary {
  background: #FAF6ED;
  border-color: #E6D4B2;
}
.bir-v8-nav-item:hover {
  background: #09382B;
  color: #ffffff;
  border-color: #09382B;
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(9, 56, 43, 0.12);
}
.bir-v8-nav-item:hover .bir-v8-nav-icon {
  background: rgba(255,255,255,0.15);
  color: #E2C485;
}
.bir-v8-nav-item:hover .bir-v8-nav-content strong { color: #ffffff; }
.bir-v8-nav-item:hover .bir-v8-nav-content span { color: #D1E3DB; }
.bir-v8-nav-item:hover .bir-v8-nav-arrow { color: #C5A059; transform: translateX(-3px); }

.bir-v8-nav-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #EBF4EF;
  color: #09382B;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s ease;
}
.bir-v8-nav-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.bir-v8-nav-content strong {
  font-size: 12.5px;
  color: #1F2D26;
  font-weight: 700;
}
.bir-v8-nav-content span {
  font-size: 10.5px;
  color: #7A8C83;
  margin-top: 1px;
}
.bir-v8-nav-arrow {
  color: #A0B2A9;
  transition: all 0.2s ease;
}

/* Projects List */
.bir-v8-projects-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.bir-v8-proj-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 9px 12px;
  background: #F9FAF8;
  border-radius: 8px;
  border: 1px solid #E8EEEA;
  transition: all 0.18s ease;
}
.bir-v8-proj-row:hover {
  background: #FAF5E8;
  border-color: #C5A059;
}
.bir-v8-proj-info {
  display: flex;
  align-items: center;
  gap: 8px;
}
.bir-v8-rank {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #09382B;
  color: #C5A059;
  font-size: 10px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
}
.bir-v8-proj-title {
  font-size: 12px;
  font-weight: 600;
  color: #1F2D26;
}
.bir-v8-proj-amount {
  font-family: 'Amiri', serif;
  font-size: 14px;
  font-weight: 700;
  color: #09382B;
}
.bir-v8-proj-amount small {
  font-family: 'Tajawal', sans-serif;
  font-size: 10.5px;
  color: #C5A059;
}

.bir-v8-loading, .bir-v8-empty {
  text-align: center;
  padding: 16px;
  color: #7A8C83;
  font-size: 12px;
}
.bir-v8-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #E2E8E4;
  border-top-color: #09382B;
  border-radius: 50%;
  animation: birSpin 0.8s linear infinite;
  margin: 0 auto 6px auto;
}
@keyframes birSpin {
  to { transform: rotate(360deg); }
}
"""

    doc.flags.ignore_permissions = True
    doc.save()
    frappe.db.commit()
    print("SUCCESS: Updated Bir Waqf Dashboard Block v8 with clean modern classic design and robust filtering!")

if __name__ == "__main__":
    run()
