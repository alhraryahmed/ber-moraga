import frappe

def run():
    block_name = "Bir Waqf Dashboard Block"
    if not frappe.db.exists("Custom HTML Block", block_name):
        doc = frappe.new_doc("Custom HTML Block")
        doc.name = block_name
    else:
        doc = frappe.get_doc("Custom HTML Block", block_name)

    doc.html = """<!-- لوحة منصة البر الوقفية — v7 مع كروت ومداخل البيانات الاحصائية المفلترة المباشرة -->
<div class="bir-v7-dashboard" dir="rtl" lang="ar">
  
  <!-- الشريط العلوي الفخم بشعار كبير مبرز -->
  <header class="bir-v7-header">
    <div class="bir-v7-brand">
      
      <!-- إبراز الصورة وحجم الشعار الكبير -->
      <div class="bir-v7-logo-card">
        <img src="/files/Screenshot 2026-07-23 013547.png" alt="شعار منصة البر الوقفية" class="bir-v7-logo-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
        <div class="bir-v7-logo-fallback" style="display:none;">
          <svg viewBox="0 0 24 24" width="48" height="48" fill="currentColor"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
        </div>
      </div>

      <div class="bir-v7-titles">
        <div class="bir-v7-org-tag">
          <svg viewBox="0 0 24 24" width="13" height="13" fill="currentColor"><path d="M12 2L3 7v10l9 5 9-5V7l-9-5zm0 2.2L19 8v8l-7 3.9L5 16V8l7-3.8z"/></svg>
          <span>الهيئة العامة للأوقاف والشؤون الإسلامية</span>
        </div>
        <h1 class="bir-v7-main-title">منصة البِرّ الوقفية <span class="bir-v7-gold-txt">| مركز المعالجة والمطابقة المصرفية</span></h1>
        <p class="bir-v7-sub-title">منظومة الإدارة الذكية للتبرعات ومساهمات السلة والمطابقة الآلية لكشوف الحسابات</p>
      </div>
    </div>

    <div class="bir-v7-meta">
      <div class="bir-v7-live-chip">
        <span class="bir-v7-pulse"></span>
        <span>النظام متصل ونشط</span>
      </div>
      <div class="bir-v7-clock-box">
        <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        <span class="bir-v7-clock">--:--:--</span>
      </div>
    </div>
  </header>

  <!-- شريط تنبيه المدخل المباشر للبيانات المفلترة -->
  <div class="bir-v7-action-banner">
    <div class="bir-v7-banner-info">
      <span class="bir-v7-banner-icon">⚡</span>
      <div>
        <strong>مداخل البيانات المباشرة والإحصائيات المفلترة:</strong>
        <span>انقر على أي كارت إحصائي لفتح القائمة المفلترة الخاصة بتلك الإحصائية مباشرة</span>
      </div>
    </div>
    <div class="bir-v7-banner-hint">تصفية فورية 100%</div>
  </div>

  <!-- شبكة بطاقات KPI تفاعلية قابلة للنقر (تفتح مباشرة قائمة المعاملات المفلترة حسب الإحصائية) -->
  <section class="bir-v7-kpi-grid">
    
    <!-- 1. إجمالي التبرعات والمساهمات -->
    <div class="bir-v7-card c-emerald clickable" onclick="openBirFilteredList('Bir Transaction', {}, 'جميع التبرعات والمساهمات');" title="انقر لفتح قائمة جميع التبرعات والمساهمات">
      <div class="bir-v7-icon">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12V7H3v10h11"/><path d="M18 15t3 3m0 0l-3 3m3-3h-6"/></svg>
      </div>
      <div class="bir-v7-card-body">
        <div class="bir-v7-card-top">
          <span class="bir-v7-label">إجمالي التبرعات والمساهمات</span>
          <span class="bir-v7-badge badge-emerald">مدخل البيانات <i class="fa fa-arrow-left"></i></span>
        </div>
        <div class="bir-v7-value val-total-amount">0.00 <small>د.ل</small></div>
        <div class="bir-v7-sub val-total-count">0 معاملة مدخلة بالنظام</div>
        <div class="bir-v7-entry-hint">انقر لفتح السجل الكامل للمعاملات ➔</div>
      </div>
    </div>

    <!-- 2. المعاملات المطابقة مصرفياً -->
    <div class="bir-v7-card c-gold clickable" onclick="openBirFilteredList('Bir Transaction', {reconciliation_status: ['in', ['مطابق آليًا', 'مطابق يدويًا']]}, 'المعاملات المطابقة مصرفياً');" title="انقر لعرض المعاملات المطابقة مصرفياً فقط">
      <div class="bir-v7-icon">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
      </div>
      <div class="bir-v7-card-body">
        <div class="bir-v7-card-top">
          <span class="bir-v7-label">المعاملات المطابقة مصرفياً</span>
          <span class="bir-v7-badge badge-gold val-matched-pct">0% مطابقة <i class="fa fa-arrow-left"></i></span>
        </div>
        <div class="bir-v7-value val-matched-count">0</div>
        <div class="bir-v7-progress-track"><div class="bir-v7-progress-bar val-matched-progress" style="width: 0%;"></div></div>
        <div class="bir-v7-sub">انقر للتصفية حسب المعاملات المطابقة</div>
        <div class="bir-v7-entry-hint">فتح قائمة المعاملات المطابقة ➔</div>
      </div>
    </div>

    <!-- 3. المعاملات المدخلة بالنظام -->
    <div class="bir-v7-card c-blue clickable" onclick="openBirFilteredList('Bir Transaction', {}, 'المعاملات المدخلة بالنظام');" title="انقر لعرض المعاملات المدخلة">
      <div class="bir-v7-icon">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>
      </div>
      <div class="bir-v7-card-body">
        <div class="bir-v7-card-top">
          <span class="bir-v7-label">المعاملات المدخلة بالنظام</span>
          <span class="bir-v7-badge badge-blue">إجمالي المدخلات <i class="fa fa-arrow-left"></i></span>
        </div>
        <div class="bir-v7-value val-transactions-input">0</div>
        <div class="bir-v7-sub">انقر للتصفية والاستعراض الكامل</div>
        <div class="bir-v7-entry-hint">فتح سجل جميع المدخلات ➔</div>
      </div>
    </div>

    <!-- 4. معاملات الاستثناء -->
    <div class="bir-v7-card c-amber clickable" onclick="openBirFilteredList('Bir Transaction', {has_exception: 1}, 'معاملات الاستثناء');" title="انقر لعرض معاملات الاستثناء التي تتطلب مراجعة">
      <div class="bir-v7-icon">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
      </div>
      <div class="bir-v7-card-body">
        <div class="bir-v7-card-top">
          <span class="bir-v7-label">معاملات الاستثناء</span>
          <span class="bir-v7-badge badge-amber">تتطلب مراجعة ⚡</span>
        </div>
        <div class="bir-v7-value val-exceptions-count">0</div>
        <div class="bir-v7-sub">انقر للتصفية وعرض المعاملات المستثناة</div>
        <div class="bir-v7-entry-hint">فتح المعاملات المستثناة فقط ➔</div>
      </div>
    </div>

    <!-- 5. أعلى قيمة لمساهمة واحدة -->
    <div class="bir-v7-card c-purple clickable" onclick="openBirFilteredList('Bir Transaction', {is_basket: 0}, 'المساهمات الفردية');" title="انقر لعرض المساهمات الفردية مرتبة حسب القيمة الأكبر">
      <div class="bir-v7-icon">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2z"/></svg>
      </div>
      <div class="bir-v7-card-body">
        <div class="bir-v7-card-top">
          <span class="bir-v7-label">أعلى قيمة لمساهمة واحدة</span>
          <span class="bir-v7-badge badge-purple">مساهمات فردية <i class="fa fa-arrow-left"></i></span>
        </div>
        <div class="bir-v7-value val-max-single">0.00 <small>د.ل</small></div>
        <div class="bir-v7-sub">انقر لفتح قائمة المعاملات الفردية</div>
        <div class="bir-v7-entry-hint">فتح تصفية المساهمات الفردية ➔</div>
      </div>
    </div>

    <!-- 6. أعلى قيمة لمساهمة السلة -->
    <div class="bir-v7-card c-teal clickable" onclick="openBirFilteredList('Bir Transaction', {is_basket: 1}, 'معاملات سلة المشاريع');" title="انقر لعرض معاملات سلة المشاريع">
      <div class="bir-v7-icon">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
      </div>
      <div class="bir-v7-card-body">
        <div class="bir-v7-card-top">
          <span class="bir-v7-label">أعلى قيمة لمساهمة السلة</span>
          <span class="bir-v7-badge badge-teal">سلات المشاريع <i class="fa fa-arrow-left"></i></span>
        </div>
        <div class="bir-v7-value val-max-basket">0.00 <small>د.ل</small></div>
        <div class="bir-v7-sub val-basket-count-sub">انقر لعرض معاملات السلة فقط</div>
        <div class="bir-v7-entry-hint">فتح تصفية سلات المشاريع ➔</div>
      </div>
    </div>

  </section>

  <!-- التخطيط الرئيسي السفلي -->
  <div class="bir-v7-layout">
    
    <!-- قسم المداخل المباشرة والخدمات لدوكتايبات المنظومة -->
    <section class="bir-v7-panel">
      <div class="bir-v7-panel-header">
        <div>
          <h3 class="bir-v7-panel-title">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#C5A059" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            <span>مداخل البيانات المباشرة ودوكتايبات النظام</span>
          </h3>
          <small class="bir-v7-panel-sub">انتقال مباشر ومضمون لقوائم وسجلات المنظومة</small>
        </div>
        <span class="bir-v7-portal-tag">بوابات الدخول السريع</span>
      </div>

      <div class="bir-v7-btn-grid">
        
        <!-- رابط مركز معالجة البيانات -->
        <button class="bir-v7-btn highlight" onclick="frappe.set_route('bir_data_processor');" title="مدخل تشغيلي مباشر لمركز رفع ومعالجة الكشوف والمطابقة">
          <div class="bir-v7-btn-icon icon-emerald"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/><path d="M12 13v6m-3-3l3-3 3 3"/></svg></div>
          <div class="bir-v7-btn-txt">
            <div class="bir-v7-btn-head">
              <strong>مركز معالجة البيانات والمطابقة</strong>
              <span class="bir-v7-chip chip-emerald">مركز عمل ⚡</span>
            </div>
            <span>رفع ومعالجة كشوف المنصة والبنك</span>
          </div>
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" class="bir-v7-btn-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

        <!-- رابط جدول المعاملات وتضمين المصرف -->
        <button class="bir-v7-btn" onclick="openBirFilteredList('Bir Transaction', {}, 'جدول جميع المعاملات');" title="مدخل مباشر لسجل معاملات التبرعات والمساهمات">
          <div class="bir-v7-btn-icon icon-gold"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg></div>
          <div class="bir-v7-btn-txt">
            <div class="bir-v7-btn-head">
              <strong>جدول المعاملات وتضمين المصرف</strong>
              <span class="bir-v7-chip chip-gold">سجل عام ➔</span>
            </div>
            <span>استعراض المعاملات وتحديث المصارف</span>
          </div>
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" class="bir-v7-btn-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

        <!-- رابط كشوف الحساب المصرفية -->
        <button class="bir-v7-btn" onclick="openBirFilteredList('Bir Bank Statement', {}, 'كشوف الحسابات المصرفية');" title="مدخل مباشر لدوكتايب كشوف الحسابات المصرفية">
          <div class="bir-v7-btn-icon icon-blue"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M3 10h18M5 6l7-3 7 3M4 10v11M20 10v11M8 14v3M12 14v3M16 14v3"/></svg></div>
          <div class="bir-v7-btn-txt">
            <div class="bir-v7-btn-head">
              <strong>كشوف الحسابات المصرفية</strong>
              <span class="bir-v7-chip chip-blue">سجل الكشوف ➔</span>
            </div>
            <span>متابعة كشوف الحسابات والبنود</span>
          </div>
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" class="bir-v7-btn-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

        <!-- رابط بنود كشوف الحساب المصرفي -->
        <button class="bir-v7-btn" onclick="openBirFilteredList('Bir Bank Statement Entry', {}, 'بنود كشوف الحساب المصرفي');" title="مدخل مباشر لدوكتايب قيود وبنود الكشوف المصرفية">
          <div class="bir-v7-btn-icon icon-purple"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div>
          <div class="bir-v7-btn-txt">
            <div class="bir-v7-btn-head">
              <strong>بنود كشوف الحساب المصرفي</strong>
              <span class="bir-v7-chip chip-purple">تفاصيل القيود ➔</span>
            </div>
            <span>عرض قيود كشف الحساب والعمليات</span>
          </div>
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" class="bir-v7-btn-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

        <!-- رابط المصارف المعتمدة -->
        <button class="bir-v7-btn" onclick="openBirFilteredList('Bank', {}, 'دليل المصارف المعتمدة');" title="مدخل مباشر لدوكتايب دليل البنوك المعتمدة">
          <div class="bir-v7-btn-icon icon-teal"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg></div>
          <div class="bir-v7-btn-txt">
            <div class="bir-v7-btn-head">
              <strong>المصارف المعتمدة</strong>
              <span class="bir-v7-chip chip-teal">دليل المصارف ➔</span>
            </div>
            <span>دليل البنوك (مصرف الجمهورية،...)</span>
          </div>
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" class="bir-v7-btn-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

        <!-- رابط دفعات استيراد البيانات -->
        <button class="bir-v7-btn" onclick="openBirFilteredList('Bir Import Batch', {}, 'دفعات استيراد البيانات');" title="مدخل مباشر لدوكتايب أرشيف ودفعات الاستيراد">
          <div class="bir-v7-btn-icon icon-amber"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg></div>
          <div class="bir-v7-btn-txt">
            <div class="bir-v7-btn-head">
              <strong>دفعات استيراد البيانات</strong>
              <span class="bir-v7-chip chip-amber">أرشيف الدفعات ➔</span>
            </div>
            <span>أرشيف وسجل الدفعات المستوردة</span>
          </div>
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" class="bir-v7-btn-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

      </div>
    </section>

    <!-- قسم أعلى المشاريع الوقفية -->
    <section class="bir-v7-panel">
      <div class="bir-v7-panel-header">
        <div>
          <h3 class="bir-v7-panel-title">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#C5A059" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
            <span>أعلى المشاريع الوقفية</span>
          </h3>
          <small class="bir-v7-panel-sub">ترتيب آلي حسب حجم المساهمات</small>
        </div>
      </div>

      <div class="bir-v7-projects-list">
        <div class="bir-v7-loading">
          <div class="bir-v7-spinner"></div>
          <span>جاري جلب إحصائيات المشاريع...</span>
        </div>
      </div>
    </section>

  </div>

</div>
"""

    doc.script = """// Robust Script for Bir Waqf Dashboard Block v7 with Filtered List Openers
window.openBirFilteredList = function(doctype, filters, filterName) {
    if (typeof frappe !== 'undefined') {
        frappe.route_options = filters || {};
        frappe.set_route('List', doctype);
        if (filterName && frappe.show_alert) {
            frappe.show_alert({
                message: __('تم فتح قائمة ') + (doctype === 'Bir Transaction' ? __('المعاملات') : doctype) + __(' المفلترة حسب: ') + filterName,
                indicator: 'green'
            }, 4);
        }
    }
};

(function(wrapper) {
	if (!wrapper) wrapper = document;

	function renderClock() {
		var now = new Date();
		var clock = wrapper.querySelector('.bir-v7-clock');
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
						cntEl.innerText = (stats.total_transactions || 0).toLocaleString('ar-LY') + ' معاملة مدخلة بالنظام';
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
						pctEl.innerHTML = pct + '% مطابقة <i class="fa fa-arrow-left"></i>';
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
					var projContainer = wrapper.querySelector('.bir-v7-projects-list');
					if (projContainer) {
						if (stats.top_projects && stats.top_projects.length > 0) {
							var projHtml = '';
							stats.top_projects.forEach(function(p, idx) {
								var rankBadge = '<span class="bir-v7-rank">#' + (idx + 1) + '</span>';
								var pVal = (p.total || 0).toLocaleString('ar-LY', {minimumFractionDigits:2, maximumFractionDigits:2});
								projHtml += '<div class="bir-v7-proj-row">' +
									'<div class="bir-v7-proj-info">' + rankBadge + '<span class="bir-v7-proj-title">' + (p.project_name || 'مشروع وقفي') + '</span></div>' +
									'<div class="bir-v7-proj-amount">' + pVal + ' <small>د.ل</small></div>' +
								'</div>';
							});
							projContainer.innerHTML = projHtml;
						} else {
							projContainer.innerHTML = '<div class="bir-v7-empty">لا توجد بيانات مشاريع سلة حالياً</div>';
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
 * الهوية البصرية الفخمة والعصرية v7 — منصة البر الوقفية
 * Deep Green (#0B3D2E) | Gold (#C5A059) | Action Portal Buttons & Filtered Cards
 * --------------------------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@700&family=Tajawal:wght@400;500;600;700;800&display=swap');

.bir-v7-dashboard {
  direction: rtl;
  font-family: 'Tajawal', sans-serif;
  color: #1F2D26;
  background: #F4F7F5;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 10px 36px rgba(11, 61, 46, 0.03);
  margin-bottom: 24px;
}

/* Header Banner المطور */
.bir-v7-header {
  background: linear-gradient(135deg, #0B3D2E 0%, #145C43 50%, #06301E 100%);
  border-radius: 18px;
  padding: 24px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #ffffff;
  position: relative;
  overflow: hidden;
  box-shadow: 0 14px 32px rgba(11, 61, 46, 0.22);
  border: 1px solid rgba(197, 160, 89, 0.4);
  margin-bottom: 16px;
  min-height: 120px;
}
.bir-v7-header::before {
  content: '';
  position: absolute;
  top: -40%;
  right: -10%;
  width: 320px;
  height: 320px;
  background: radial-gradient(circle, rgba(197, 160, 89, 0.14) 0%, transparent 70%);
  pointer-events: none;
}

.bir-v7-brand {
  display: flex;
  align-items: center;
  gap: 22px;
  z-index: 2;
}

.bir-v7-logo-card {
  width: 120px;
  height: 90px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  padding: 8px 12px;
  border: 2px solid #C5A059;
  flex-shrink: 0;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.bir-v7-logo-card:hover {
  transform: scale(1.04);
  box-shadow: 0 12px 30px rgba(197, 160, 89, 0.35);
}

.bir-v7-logo-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
.bir-v7-logo-fallback {
  color: #0B3D2E;
}

.bir-v7-org-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11.5px;
  font-weight: 600;
  color: #E2C485;
  background: rgba(197, 160, 89, 0.16);
  padding: 4px 12px;
  border-radius: 14px;
  border: 1px solid rgba(197, 160, 89, 0.35);
  margin-bottom: 8px;
}

.bir-v7-main-title {
  font-family: 'Amiri', serif;
  font-size: 26px;
  font-weight: 700;
  margin: 0;
  color: #ffffff;
  line-height: 1.2;
}
.bir-v7-gold-txt {
  color: #E2C485;
  font-family: 'Tajawal', sans-serif;
  font-size: 18px;
  font-weight: 600;
}
.bir-v7-sub-title {
  font-size: 13px;
  color: #D1E3DB;
  margin: 5px 0 0 0;
}

.bir-v7-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
  z-index: 2;
}

.bir-v7-live-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.22);
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 12px;
  color: #92F7B6;
  font-weight: 600;
}

.bir-v7-pulse {
  width: 8px;
  height: 8px;
  background: #2ECC71;
  border-radius: 50%;
  box-shadow: 0 0 8px #2ECC71;
  animation: birPulse 1.8s infinite;
}
@keyframes birPulse {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(46, 204, 113, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); }
}

.bir-v7-clock-box {
  font-size: 14.5px;
  font-weight: 700;
  color: #E2C485;
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(0,0,0,0.25);
  padding: 5px 14px;
  border-radius: 10px;
  border: 1px solid rgba(197, 160, 89, 0.3);
}

/* Action Banner */
.bir-v7-action-banner {
  background: linear-gradient(90deg, #FAF5E8 0%, #F0E6CE 100%);
  border: 1.5px dashed #C5A059;
  border-radius: 12px;
  padding: 10px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.bir-v7-banner-info {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: #0B3D2E;
}
.bir-v7-banner-icon {
  font-size: 18px;
}
.bir-v7-banner-info strong {
  font-weight: 700;
  margin-left: 6px;
}
.bir-v7-banner-info span {
  color: #4A5B52;
}
.bir-v7-banner-hint {
  font-size: 11px;
  font-weight: 700;
  background: #0B3D2E;
  color: #E2C485;
  padding: 3px 10px;
  border-radius: 12px;
}

/* KPI Grid */
.bir-v7-kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

@media (max-width: 1024px) {
  .bir-v7-kpi-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .bir-v7-kpi-grid { grid-template-columns: 1fr; }
}

.bir-v7-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: flex-start;
  gap: 14px;
  border: 1.5px solid #E2E8E4;
  box-shadow: 0 4px 14px rgba(0,0,0,0.025);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}
.bir-v7-card.clickable {
  cursor: pointer !important;
}
.bir-v7-card::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 5px;
  height: 100%;
  transition: width 0.2s ease;
}
.bir-v7-card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 16px 32px rgba(11, 61, 46, 0.15);
  border-color: #C5A059;
}
.bir-v7-card:hover::before { width: 10px; }
.bir-v7-card:hover .bir-v7-entry-hint {
  color: #0B3D2E;
  font-weight: 700;
  transform: translateX(-4px);
}

.c-emerald::before { background: #0B3D2E; }
.c-gold::before { background: #C5A059; }
.c-blue::before { background: #2980B9; }
.c-amber::before { background: #D35400; }
.c-purple::before { background: #8E44AD; }
.c-teal::before { background: #16A085; }

.bir-v7-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 10px rgba(0,0,0,0.04);
}
.c-emerald .bir-v7-icon { background: #EAF3EE; color: #0B3D2E; }
.c-gold .bir-v7-icon { background: #FAF5E8; color: #B58D28; }
.c-blue .bir-v7-icon { background: #EBF4FA; color: #2980B9; }
.c-amber .bir-v7-icon { background: #FDF3E9; color: #D35400; }
.c-purple .bir-v7-icon { background: #F4ECF7; color: #8E44AD; }
.c-teal .bir-v7-icon { background: #E8F8F5; color: #16A085; }

.bir-v7-card-body { flex: 1; }

.bir-v7-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}
.bir-v7-label {
  font-size: 12.5px;
  font-weight: 700;
  color: #35473E;
}

.bir-v7-badge {
  font-size: 10px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 4px;
  border: 1px solid transparent;
}
.badge-emerald { background: #EAF3EE; color: #0B3D2E; border-color: rgba(11,61,46,0.2); }
.badge-gold { background: #FAF5E8; color: #B58D28; border-color: rgba(197,160,89,0.3); }
.badge-blue { background: #EBF4FA; color: #2980B9; border-color: rgba(41,128,185,0.2); }
.badge-amber { background: #FDF3E9; color: #D35400; border-color: rgba(211,84,0,0.2); }
.badge-purple { background: #F4ECF7; color: #8E44AD; border-color: rgba(142,68,173,0.2); }
.badge-teal { background: #E8F8F5; color: #16A085; border-color: rgba(22,160,133,0.2); }

.bir-v7-value {
  font-family: 'Amiri', serif;
  font-size: 26px;
  font-weight: 700;
  color: #0B3D2E;
  line-height: 1.1;
  margin: 4px 0;
}
.bir-v7-value small {
  font-family: 'Tajawal', sans-serif;
  font-size: 12px;
  color: #C5A059;
  font-weight: 700;
}

.bir-v7-progress-track {
  height: 6px;
  background: #EAEFEB;
  border-radius: 3px;
  overflow: hidden;
  margin: 6px 0;
}
.bir-v7-progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #C5A059 0%, #0B3D2E 100%);
  border-radius: 3px;
  transition: width 0.7s ease;
}

.bir-v7-sub {
  font-size: 11px;
  color: #7A8C83;
}

.bir-v7-entry-hint {
  font-size: 10.5px;
  color: #A0B2A9;
  margin-top: 8px;
  padding-top: 6px;
  border-top: 1px dashed #E5EBE7;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
}

/* Layout */
.bir-v7-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 18px;
}
@media (max-width: 992px) {
  .bir-v7-layout { grid-template-columns: 1fr; }
}

.bir-v7-panel {
  background: #ffffff;
  border-radius: 16px;
  padding: 22px;
  border: 1px solid #E2E8E4;
  box-shadow: 0 4px 16px rgba(0,0,0,0.02);
}

.bir-v7-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
  padding-bottom: 12px;
  border-bottom: 2px solid #F0F4F2;
}
.bir-v7-panel-title {
  font-size: 15px;
  font-weight: 700;
  color: #0B3D2E;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}
.bir-v7-panel-sub {
  font-size: 11.5px;
  color: #7A8C83;
  margin-top: 2px;
  display: block;
}
.bir-v7-portal-tag {
  font-size: 10.5px;
  font-weight: 700;
  color: #C5A059;
  background: #FAF5E8;
  padding: 4px 12px;
  border-radius: 12px;
  border: 1px solid rgba(197,160,89,0.3);
}

/* Actions Grid - Direct Entry Portal Buttons */
.bir-v7-btn-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
}

.bir-v7-btn {
  background: #F9FBF8;
  border: 1.5px solid #E0E7E2;
  border-radius: 14px;
  padding: 14px 16px;
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  text-align: right;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}
.bir-v7-btn.highlight {
  background: linear-gradient(135deg, #FAF5E8 0%, #F4E7CB 100%);
  border-color: #E2D1A6;
}
.bir-v7-btn:hover {
  background: #0B3D2E;
  color: #ffffff;
  border-color: #C5A059;
  transform: translateY(-3px);
  box-shadow: 0 8px 22px rgba(11, 61, 46, 0.2);
}
.bir-v7-btn:hover .bir-v7-btn-icon {
  background: rgba(255,255,255,0.18);
  color: #E2C485;
}
.bir-v7-btn:hover .bir-v7-btn-txt strong { color: #ffffff; }
.bir-v7-btn:hover .bir-v7-btn-txt span { color: #D1E3DB; }
.bir-v7-btn:hover .bir-v7-chip {
  background: rgba(197,160,89,0.25);
  color: #E2C485;
  border-color: #C5A059;
}
.bir-v7-btn:hover .bir-v7-btn-arrow { color: #C5A059; transform: translateX(-4px); }

.bir-v7-btn-icon {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.22s ease;
}
.icon-emerald { background: #EAF3EE; color: #0B3D2E; }
.icon-gold { background: #FAF5E8; color: #B58D28; }
.icon-blue { background: #EBF4FA; color: #2980B9; }
.icon-purple { background: #F4ECF7; color: #8E44AD; }
.icon-teal { background: #E8F8F5; color: #16A085; }
.icon-amber { background: #FDF3E9; color: #D35400; }

.bir-v7-btn-txt {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.bir-v7-btn-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
  margin-bottom: 3px;
}
.bir-v7-btn-txt strong {
  font-size: 13px;
  color: #1F2D26;
  font-weight: 700;
}
.bir-v7-btn-txt span {
  font-size: 11px;
  color: #7A8C83;
}

.bir-v7-chip {
  font-size: 9.5px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 8px;
  border: 1px solid transparent;
  white-space: nowrap;
  transition: all 0.2s ease;
}
.chip-emerald { background: #EAF3EE; color: #0B3D2E; }
.chip-gold { background: #FAF5E8; color: #B58D28; }
.chip-blue { background: #EBF4FA; color: #2980B9; }
.chip-purple { background: #F4ECF7; color: #8E44AD; }
.chip-teal { background: #E8F8F5; color: #16A085; }
.chip-amber { background: #FDF3E9; color: #D35400; }

.bir-v7-btn-arrow {
  color: #A0B2A9;
  transition: all 0.22s ease;
}

/* Projects List */
.bir-v7-projects-list {
  display: flex;
  flex-direction: column;
  gap: 9.5px;
}
.bir-v7-proj-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 11px 14px;
  background: #F8FAF6;
  border-radius: 12px;
  border: 1px solid #E5EBE7;
  transition: all 0.2s ease;
}
.bir-v7-proj-row:hover {
  background: #FAF5E8;
  border-color: #C5A059;
  transform: translateX(-2px);
}
.bir-v7-proj-info {
  display: flex;
  align-items: center;
  gap: 10px;
}
.bir-v7-rank {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #0B3D2E;
  color: #C5A059;
  font-size: 11px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
}
.bir-v7-proj-title {
  font-size: 12.5px;
  font-weight: 600;
  color: #1F2D26;
}
.bir-v7-proj-amount {
  font-family: 'Amiri', serif;
  font-size: 15px;
  font-weight: 700;
  color: #0B3D2E;
}
.bir-v7-proj-amount small {
  font-family: 'Tajawal', sans-serif;
  font-size: 11px;
  color: #C5A059;
}

.bir-v7-loading, .bir-v7-empty {
  text-align: center;
  padding: 20px;
  color: #7A8C83;
  font-size: 12.5px;
}
.bir-v7-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #E2E8E4;
  border-top-color: #0B3D2E;
  border-radius: 50%;
  animation: birSpin 0.8s linear infinite;
  margin: 0 auto 8px auto;
}
@keyframes birSpin {
  to { transform: rotate(360deg); }
}
"""

    doc.flags.ignore_permissions = True
    doc.save()
    frappe.db.commit()
    print("SUCCESS: Updated Bir Waqf Dashboard Block v7 with filtered statistical cards and direct entry portals!")

if __name__ == "__main__":
    run()
