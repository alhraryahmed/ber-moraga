import frappe

def setup_custom_block():
    block_name = "Bir Waqf Dashboard Block"
    if not frappe.db.exists("Custom HTML Block", block_name):
        block_doc = frappe.new_doc("Custom HTML Block")
        block_doc.name = block_name
        block_doc.private = 0
    else:
        block_doc = frappe.get_doc("Custom HTML Block", block_name)

    html_content = """<!-- لوحة منصة البر الوقفية — v16 تصميم مودرن عالمي نظيف وبدون أي أيقونات رسومية مع شعار بارز ومكبر جداً -->
<div class="bir-wc-dashboard" dir="rtl" lang="ar">
  
  <!-- 1. الهيدر الفاخر مع شعار مكبر وواضح جداً -->
  <header class="bir-wc-header">
    <div class="bir-wc-brand">
      <div class="bir-wc-logo-box">
        <img src="/files/Screenshot 2026-07-23 013547.png" alt="شعار منصة البر الوقفية" class="bir-wc-logo-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
        <div class="bir-wc-logo-fallback" style="display:none;">
          <svg viewBox="0 0 24 24" width="48" height="48" fill="#0a5c36"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
        </div>
      </div>
      <div class="bir-wc-titles">
        <h1 class="bir-wc-main-title">منصة البِرّ الوقفية — مركز المعالجة والمطابقة المصرفية</h1>
        <p class="bir-wc-sub-title">الهيئة العامة للأوقاف والشؤون الإسلامية | المنظومة الذكية للتبرعات والمطابقة المصرفية</p>
      </div>
    </div>

    <div class="bir-wc-meta">
      <div class="bir-wc-status-pill">
        <span class="bir-wc-dot"></span>
        <span>النظام متصل ونشط</span>
      </div>
      <div class="bir-wc-clock-box">
        <span class="bir-v8-clock bir-hu-clock">--:--:--</span>
      </div>
    </div>
  </header>

  <!-- 2. شبكة الكروت الإحصائية (تصميم مودرن عالمي نظيف بدون أيقونات رسومية) -->
  <section class="bir-wc-kpi-grid">
    
    <!-- 1. إجمالي التبرعات والمساهمات -->
    <div class="bir-wc-card" onclick="openBirFilteredList('Bir Transaction', {}, 'جميع التبرعات والمساهمات', 'creation', 'desc');" title="انقر لفتح واستعراض جميع المعاملات">
      <div class="bir-wc-card-title">إجمالي التبرعات والمساهمات</div>
      <div class="bir-wc-card-value val-total-amount">0.00 <small>د.ل</small></div>
      <div class="bir-wc-card-caption val-total-count">0 معاملة مدخلة</div>
    </div>

    <!-- 2. المعاملات المطابقة مصرفياً -->
    <div class="bir-wc-card gold-border" onclick="openBirFilteredList('Bir Transaction', {reconciliation_status: ['in', ['مطابق آليًا', 'مطابق يدويًا']]}, 'المعاملات المطابقة مصرفياً', 'creation', 'desc');" title="تصفية المعاملات المطابقة">
      <div class="bir-wc-card-title">المعاملات المطابقة مصرفياً</div>
      <div class="bir-wc-card-value gold val-matched-count">0</div>
      <div class="bir-wc-card-caption val-matched-pct">0% نسبة المطابقة</div>
    </div>

    <!-- 3. المعاملات المدخلة بالنظام -->
    <div class="bir-wc-card" onclick="openBirFilteredList('Bir Transaction', {}, 'المعاملات المدخلة بالنظام', 'creation', 'desc');" title="عرض المعاملات المدخلة">
      <div class="bir-wc-card-title">المعاملات المدخلة بالنظام</div>
      <div class="bir-wc-card-value val-transactions-input">0</div>
      <div class="bir-wc-card-caption">إجمالي قيود المنظومة</div>
    </div>

    <!-- 4. معاملات الاستثناء -->
    <div class="bir-wc-card red-border" onclick="openBirFilteredList('Bir Transaction', {has_exception: 1}, 'معاملات الاستثناء', 'creation', 'desc');" title="عرض معاملات الاستثناء">
      <div class="bir-wc-card-title">معاملات الاستثناء</div>
      <div class="bir-wc-card-value red val-exceptions-count">0</div>
      <div class="bir-wc-card-caption red">تتطلب تدقيق ومراجعة</div>
    </div>

    <!-- 5. أعلى قيمة لمساهمة واحدة -->
    <div class="bir-wc-card gold-border" onclick="openBirFilteredList('Bir Transaction', {is_basket: 0}, 'أعلى قيمة لمساهمة واحدة', 'total_amount', 'desc');" title="ترتيب المساهمات الفردية">
      <div class="bir-wc-card-title">أعلى قيمة لمساهمة واحدة</div>
      <div class="bir-wc-card-value gold val-max-single">0.00 <small>د.ل</small></div>
      <div class="bir-wc-card-caption">مساهمة فردية قياسية</div>
    </div>

    <!-- 6. أعلى قيمة لمساهمة السلة -->
    <div class="bir-wc-card" onclick="openBirFilteredList('Bir Transaction', {is_basket: 1}, 'أعلى قيمة لمساهمة السلة', 'total_amount', 'desc');" title="ترتيب مساهمات السلة">
      <div class="bir-wc-card-title">أعلى قيمة لمساهمة السلة</div>
      <div class="bir-wc-card-value val-max-basket">0.00 <small>د.ل</small></div>
      <div class="bir-wc-card-caption val-basket-count-sub">معاملات سلة المشاريع</div>
    </div>

  </section>

  <!-- 3. أقسام وإجراءات الوصول السريع بتصميم احترافي عالمي -->
  <div class="bir-wc-section-header">أقسام المنظومة والوصول السريع</div>

  <div class="bir-wc-panels-grid">
    
    <!-- اللوحة 1: مركز المعالجة والقيود -->
    <div class="bir-wc-panel">
      <div class="bir-wc-panel-head">مركز المعالجة والقيود</div>
      <div class="bir-wc-btn-list">
        
        <button class="bir-wc-btn btn-hero" onclick="frappe.set_route('bir_data_processor');">
          <div class="bir-wc-btn-text">
            <strong>مركز معالجة البيانات والمطابقة</strong>
            <small>رفع ومعالجة كشوف المنصة والبنك</small>
          </div>
          <span class="bir-wc-tag white">الرئيسي</span>
        </button>

        <button class="bir-wc-btn" onclick="openBirFilteredList('Bir Transaction', {}, 'جدول المعاملات', 'creation', 'desc');">
          <div class="bir-wc-btn-text">
            <strong>جدول المعاملات وتضمين المصرف</strong>
            <small>استعراض القيود وتحديث المصارف</small>
          </div>
          <span class="bir-wc-arrow">➔</span>
        </button>

        <button class="bir-wc-btn" onclick="openBirFilteredList('Bir Import Batch', {}, 'دفعات استيراد البيانات', 'creation', 'desc');">
          <div class="bir-wc-btn-text">
            <strong>دفعات استيراد البيانات المستوردة</strong>
            <small>أرشيف وسجل الاستيراد</small>
          </div>
          <span class="bir-wc-arrow">➔</span>
        </button>

      </div>
    </div>

    <!-- اللوحة 2: كشوف الحساب والمصارف -->
    <div class="bir-wc-panel">
      <div class="bir-wc-panel-head">كشوف الحساب والمصارف</div>
      <div class="bir-wc-btn-list">
        
        <button class="bir-wc-btn" onclick="openBirFilteredList('Bir Bank Statement', {}, 'كشوف الحسابات المصرفية', 'creation', 'desc');">
          <div class="bir-wc-btn-text">
            <strong>كشوف الحسابات المصرفية</strong>
            <small>متابعة وتدقيق كشوف البنوك</small>
          </div>
          <span class="bir-wc-tag soft-green">الكشوف</span>
        </button>

        <button class="bir-wc-btn" onclick="openBirFilteredList('Bir Bank Statement Entry', {}, 'بنود كشوف الحساب المصرفي', 'creation', 'desc');">
          <div class="bir-wc-btn-text">
            <strong>بنود كشوف الحساب المصرفي</strong>
            <small>عرض قيود كشف الحساب والعمليات</small>
          </div>
          <span class="bir-wc-tag soft-blue">البنود</span>
        </button>

        <button class="bir-wc-btn" onclick="openBirFilteredList('Bank', {}, 'دليل المصارف المعتمدة');">
          <div class="bir-wc-btn-text">
            <strong>دليل المصارف المعتمدة (البنوك)</strong>
            <small>قائمة البنوك المعتمدة</small>
          </div>
          <span class="bir-wc-arrow">➔</span>
        </button>

      </div>
    </div>

    <!-- اللوحة 3: أعلى المشاريع الوقفية -->
    <div class="bir-wc-panel">
      <div class="bir-wc-panel-head">أعلى المشاريع الوقفية</div>
      <div class="bir-v8-projects-list bir-wc-projects-list">
        <div class="bir-wc-loading">جاري جلب إحصائيات المشاريع...</div>
      </div>
    </div>

  </div>

</div>
"""

    style_content = """/* ---------------------------------------------------
 * v16 تصميم مودرن عالمي نظيف ومريح للعين 100% — منصة البر الوقفية
 * - شعار مكبر جداً وواضح بأبعاد وافية (130px x 75px)
 * - خالي تماماً من الأيقونات الرسومية والرموز الرمزية
 * - خطوط وتنسيقات عالمية فائقة الجودة والنقاء
 * --------------------------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Tajawal:wght@400;500;700;800&display=swap');

.bir-wc-dashboard {
  direction: rtl;
  font-family: "Cairo", "Tajawal", "Inter", -apple-system, sans-serif;
  color: #1e293b;
  background: #ffffff;
  border: 1px solid #eaecf0;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
}

/* 1. Header (شعار بارز ومكبر جداً) */
.bir-wc-header {
  background: #ffffff;
  border: 1px solid #eaecf0;
  border-top: 4px solid #0a5c36;
  border-radius: 12px;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

.bir-wc-brand {
  display: flex;
  align-items: center;
  gap: 18px;
}

/* تكبير كارت الشعار جداً ليظهر بوضوح تام */
.bir-wc-logo-box {
  width: 130px;
  height: 75px;
  border-radius: 10px;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px;
  border: 1.5px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  flex-shrink: 0;
}

.bir-wc-logo-img {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
}

.bir-wc-titles {
  display: flex;
  flex-direction: column;
}

.bir-wc-main-title {
  font-size: 16.5px;
  font-weight: 800;
  color: #0a5c36;
  margin: 0;
  line-height: 1.3;
}

.bir-wc-sub-title {
  font-size: 12px;
  color: #64748b;
  margin: 3px 0 0 0;
}

.bir-wc-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.bir-wc-status-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #e6f4ea;
  color: #137333;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
}

.bir-wc-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #137333;
}

.bir-wc-clock-box {
  font-size: 12px;
  font-weight: 700;
  color: #0a5c36;
  background: #f8fafc;
  padding: 4px 12px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

/* 2. World-Class Clean KPI Grid (كروت مصغرة ونظيفة بدون أيقونات رسومية) */
.bir-wc-kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(165px, 1fr));
  gap: 12px;
  margin-bottom: 22px;
}

.bir-wc-card {
  background: #ffffff;
  border: 1px solid #eaecf0;
  border-top: 3.5px solid #0a5c36;
  border-radius: 10px;
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 78px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
}

.bir-wc-card:hover {
  transform: translateY(-2px);
  border-color: #0a5c36;
  box-shadow: 0 4px 12px rgba(10, 92, 54, 0.08);
}

.bir-wc-card.gold-border {
  border-top-color: #d4af37;
}

.bir-wc-card.red-border {
  border-top-color: #dc2626;
}

.bir-wc-card-title {
  font-size: 11.5px;
  color: #475569;
  font-weight: 700;
  margin-bottom: 4px;
  line-height: 1.25;
}

.bir-wc-card-value {
  font-size: 1.35rem;
  font-weight: 800;
  color: #0a5c36;
  line-height: 1.2;
}

.bir-wc-card-value.gold {
  color: #b8901f;
}

.bir-wc-card-value.red {
  color: #dc2626;
}

.bir-wc-card-value small {
  font-size: 0.75rem;
  font-weight: 700;
  color: #b8901f;
}

.bir-wc-card-caption {
  font-size: 10.5px;
  color: #94a3b8;
  font-weight: 600;
  margin-top: 4px;
}

.bir-wc-card-caption.red {
  color: #dc2626;
}

/* 3. Section Title */
.bir-wc-section-header {
  font-size: 13.5px;
  font-weight: 800;
  color: #334155;
  margin-bottom: 12px;
  text-align: right;
}

/* 4. Panels & Action Buttons (تصميم مودرن عالمي نظيف بدون أيقونات رسومية) */
.bir-wc-panels-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

@media (max-width: 992px) {
  .bir-wc-panels-grid {
    grid-template-columns: 1fr;
  }
}

.bir-wc-panel {
  background: #ffffff;
  border: 1px solid #eaecf0;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
}

.bir-wc-panel-head {
  font-size: 13px;
  font-weight: 800;
  color: #0f172a;
  padding-bottom: 10px;
  margin-bottom: 12px;
  border-bottom: 1px solid #f1f5f9;
  text-align: right;
}

.bir-wc-btn-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* أزرار مودرن راقية نظيفة */
.bir-wc-btn {
  background: #ffffff;
  border: 1px solid #eaecf0;
  border-radius: 8px;
  padding: 10px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  text-align: right;
  transition: all 0.2s ease;
  color: #334155;
  width: 100%;
}

.bir-wc-btn:hover {
  background: #f8fafc;
  border-color: #0a5c36;
  transform: translateX(-3px);
  box-shadow: 0 2px 8px rgba(10, 92, 54, 0.05);
}

.bir-wc-btn.btn-hero {
  background: #0a5c36;
  border-color: #0a5c36;
  color: #ffffff;
}

.bir-wc-btn.btn-hero:hover {
  background: #084c2d;
  border-color: #084c2d;
  box-shadow: 0 4px 12px rgba(10, 92, 54, 0.18);
}

.bir-wc-btn-text {
  display: flex;
  flex-direction: column;
}

.bir-wc-btn-text strong {
  font-size: 12px;
  font-weight: 700;
  line-height: 1.25;
}

.bir-wc-btn-text small {
  font-size: 10.5px;
  color: #64748b;
  margin-top: 1px;
}

.btn-hero .bir-wc-btn-text small {
  color: #d1fae5;
}

.bir-wc-tag {
  font-size: 10px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
  flex-shrink: 0;
}

.bir-wc-tag.white {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

.bir-wc-tag.soft-green {
  background: #e6f4ea;
  color: #137333;
}

.bir-wc-tag.soft-blue {
  background: #e0f2fe;
  color: #0369a1;
}

.bir-wc-arrow {
  font-size: 11px;
  color: #94a3b8;
  flex-shrink: 0;
}

/* Projects List */
.bir-wc-projects-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bir-v8-proj-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background: #f8fafc;
  border-radius: 6px;
  border: 1px solid #eaecf0;
}

.bir-v8-proj-info {
  display: flex;
  align-items: center;
  gap: 6px;
}

.bir-v8-rank {
  background: #e2e8f0;
  color: #334155;
  font-size: 10px;
  font-weight: 800;
  padding: 1px 5px;
  border-radius: 4px;
}

.bir-v8-proj-title {
  font-size: 11.5px;
  font-weight: 700;
  color: #1e293b;
}

.bir-v8-proj-amount {
  font-size: 12.5px;
  font-weight: 800;
  color: #0a5c36;
}

.bir-v8-proj-amount small {
  font-size: 10px;
  color: #64748b;
}

.bir-wc-loading {
  text-align: center;
  padding: 15px;
  color: #94a3b8;
  font-size: 11.5px;
}
"""

    script_content = """// World-Class Clean Script for Bir Waqf Dashboard Block v16
window.openBirFilteredList = function(doctype, filters, filterName, sort_field, sort_order) {
    if (typeof frappe === 'undefined') return;

    frappe.route_options = Object.assign({}, filters || {});

    function applyFiltersToListView(listview) {
        if (!listview || !listview.filter_area) return;
        
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
		var clock = wrapper.querySelector('.bir-hu-clock');
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
						mbVal.innerHTML = mbVal + ' <small>د.ل</small>';
					}

					var bskSubEl = wrapper.querySelector('.val-basket-count-sub');
					if (bskSubEl) {
						bskSubEl.innerText = (stats.basket_count || 0).toLocaleString('ar-LY') + ' معاملة سلة بالمشاريع';
					}

					// 8. Top Projects List
					var projContainer = wrapper.querySelector('.bir-wc-projects-list');
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
							projContainer.innerHTML = '<div class="bir-v8-empty" style="text-align:center;padding:12px;color:#94a3b8;font-size:11.5px;">لا توجد بيانات مشاريع سلة حالياً</div>';
						}
					}
				}
			}
		});
	}

	setTimeout(fetchStats, 100);
})(typeof root_element !== 'undefined' ? root_element : document);
"""

    block_doc.html = html_content
    block_doc.style = style_content
    block_doc.script = script_content
    block_doc.flags.ignore_permissions = True
    block_doc.save()
    frappe.db.commit()
    return block_doc.name
