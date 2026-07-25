import frappe

def run():
    block_name = "Bir Waqf Dashboard Block"
    if not frappe.db.exists("Custom HTML Block", block_name):
        doc = frappe.new_doc("Custom HTML Block")
        doc.name = block_name
        doc.private = 0
    else:
        doc = frappe.get_doc("Custom HTML Block", block_name)

    doc.html = """<!-- لوحة منصة البر الوقفية — تصميم الهوية البصرية لخدمات الحج والعمرة (الأخضر والذهبي) -->
<div class="bir-hu-dashboard" dir="rtl" lang="ar">
  
  <!-- الهيدر الرئيسي بهوية الأخضر والذهبي -->
  <header class="bir-hu-header">
    <div class="bir-hu-brand">
      <div class="bir-hu-logo-box">
        <img src="/files/Screenshot 2026-07-23 013547.png" alt="شعار منصة البر الوقفية" class="bir-hu-logo-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
        <div class="bir-hu-logo-fallback" style="display:none;">
          <svg viewBox="0 0 24 24" width="38" height="38" fill="currentColor"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
        </div>
      </div>

      <div class="bir-hu-titles">
        <div class="bir-hu-org-badge">
          <svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><path d="M12 2L3 7v10l9 5 9-5V7l-9-5zm0 2.2L19 8v8l-7 3.9L5 16V8l7-3.8z"/></svg>
          <span>الهيئة العامة للأوقاف والشؤون الإسلامية</span>
        </div>
        <h1 class="bir-hu-main-title">منصة البِرّ الوقفية <span class="bir-hu-gold-tag">| مركز المعالجة والمطابقة المصرفية</span></h1>
        <p class="bir-hu-sub-title">منظومة الإدارة الذكية للتبرعات ومساهمات السلة والمطابقة الآلية لكشوف الحسابات</p>
      </div>
    </div>

    <div class="bir-hu-meta">
      <div class="bir-hu-live-badge">
        <span class="bir-hu-pulse"></span>
        <span>النظام متصل ونشط</span>
      </div>
      <div class="bir-hu-clock-box">
        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 16 14"/></svg>
        <span class="bir-v8-clock bir-hu-clock">--:--:--</span>
      </div>
    </div>
  </header>

  <!-- شبكة الكروت الإحصائية بتصميم كروت الحج والعمرة (Green & Gold KPI Cards) -->
  <section class="bir-hu-kpi-grid">
    
    <!-- 1. إجمالي التبرعات والمساهمات -->
    <div class="hu-kpi-card" onclick="openBirFilteredList('Bir Transaction', {}, 'جميع التبرعات والمساهمات', 'creation', 'desc');" title="انقر لفتح واستعراض جميع المعاملات">
      <div class="hu-kpi-title">إجمالي التبرعات والمساهمات</div>
      <div class="hu-kpi-value val-total-amount">0.00 <small>د.ل</small></div>
      <div class="bir-hu-card-footer">
        <span class="val-total-count">0 معاملة مدخلة</span>
        <span class="bir-hu-action-link">استعراض السجل ➔</span>
      </div>
    </div>

    <!-- 2. المعاملات المطابقة مصرفياً -->
    <div class="hu-kpi-card gold-accent" onclick="openBirFilteredList('Bir Transaction', {reconciliation_status: ['in', ['مطابق آليًا', 'مطابق يدويًا']]}, 'المعاملات المطابقة مصرفياً', 'creation', 'desc');" title="انقر لعرض المعاملات المطابقة مصرفياً فقط">
      <div class="hu-kpi-title">المعاملات المطابقة مصرفياً</div>
      <div class="hu-kpi-value gold val-matched-count">0</div>
      <div class="bir-hu-progress-bar"><div class="bir-hu-progress-fill val-matched-progress" style="width: 0%;"></div></div>
      <div class="bir-hu-card-footer">
        <span class="val-matched-pct">0% نسبة المطابقة</span>
        <span class="bir-hu-action-link gold">تصفية المطابق ➔</span>
      </div>
    </div>

    <!-- 3. المعاملات المدخلة بالنظام -->
    <div class="hu-kpi-card" onclick="openBirFilteredList('Bir Transaction', {}, 'المعاملات المدخلة بالنظام', 'creation', 'desc');" title="انقر لعرض المعاملات المدخلة">
      <div class="hu-kpi-title">المعاملات المدخلة بالنظام</div>
      <div class="hu-kpi-value val-transactions-input">0</div>
      <div class="bir-hu-card-footer">
        <span>إجمالي القيود بالمنظومة</span>
        <span class="bir-hu-action-link">تصفية المدخلات ➔</span>
      </div>
    </div>

    <!-- 4. معاملات الاستثناء -->
    <div class="hu-kpi-card alert-accent" onclick="openBirFilteredList('Bir Transaction', {has_exception: 1}, 'معاملات الاستثناء', 'creation', 'desc');" title="انقر لعرض معاملات الاستثناء التي تتطلب مراجعة">
      <div class="hu-kpi-title">معاملات الاستثناء</div>
      <div class="hu-kpi-value alert val-exceptions-count">0</div>
      <div class="bir-hu-card-footer">
        <span style="color:#dc2626;font-weight:600;">تتطلب مراجعة تدقيقية</span>
        <span class="bir-hu-action-link alert">تصفية الاستثناءات ➔</span>
      </div>
    </div>

    <!-- 5. أعلى قيمة لمساهمة واحدة -->
    <div class="hu-kpi-card gold-accent" onclick="openBirFilteredList('Bir Transaction', {is_basket: 0}, 'أعلى قيمة لمساهمة واحدة', 'total_amount', 'desc');" title="انقر لعرض المساهمات الفردية مرتبة من الأكبر إلى الأصغر">
      <div class="hu-kpi-title">أعلى قيمة لمساهمة واحدة</div>
      <div class="hu-kpi-value gold val-max-single">0.00 <small>د.ل</small></div>
      <div class="bir-hu-card-footer">
        <span>مساهمة فردية قياسية</span>
        <span class="bir-hu-action-link gold">ترتيب حسب القيمة ➔</span>
      </div>
    </div>

    <!-- 6. أعلى قيمة لمساهمة السلة -->
    <div class="hu-kpi-card" onclick="openBirFilteredList('Bir Transaction', {is_basket: 1}, 'أعلى قيمة لمساهمة السلة', 'total_amount', 'desc');" title="انقر لعرض معاملات سلة المشاريع مرتبة من الأكبر إلى الأصغر">
      <div class="hu-kpi-title">أعلى قيمة لمساهمة السلة</div>
      <div class="hu-kpi-value val-max-basket">0.00 <small>د.ل</small></div>
      <div class="bir-hu-card-footer">
        <span class="val-basket-count-sub">معاملات سلة المشاريع</span>
        <span class="bir-hu-action-link">ترتيب حسب القيمة ➔</span>
      </div>
    </div>

  </section>

  <!-- التخطيط السفلي بتصميم مستوحى من الهوية البصرية للحج والعمرة -->
  <div class="bir-hu-layout">
    
    <!-- مداخل دوكتايبات المنظومة -->
    <section class="bir-hu-panel">
      <div class="bir-hu-panel-header">
        <h3 class="bir-hu-panel-title">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#d4af37" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          <span>مداخل سجلات ودوكتايبات المنظومة</span>
        </h3>
        <span class="bir-hu-sub-tag">وصول مباشر ونظيف</span>
      </div>

      <div class="bir-hu-nav-grid">
        
        <button class="bir-hu-nav-item primary" onclick="frappe.set_route('bir_data_processor');">
          <div class="bir-hu-nav-icon"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/><path d="M12 13v6m-3-3l3-3 3 3"/></svg></div>
          <div class="bir-hu-nav-content">
            <strong>مركز معالجة البيانات والمطابقة</strong>
            <span>رفع ومعالجة كشوف المنصة والبنك</span>
          </div>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" class="bir-hu-nav-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

        <button class="bir-hu-nav-item" onclick="openBirFilteredList('Bir Transaction', {}, 'جدول المعاملات', 'creation', 'desc');">
          <div class="bir-hu-nav-icon"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg></div>
          <div class="bir-hu-nav-content">
            <strong>جدول المعاملات وتضمين المصرف</strong>
            <span>استعراض المعاملات وتحديث المصارف</span>
          </div>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" class="bir-hu-nav-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

        <button class="bir-hu-nav-item" onclick="openBirFilteredList('Bir Bank Statement', {}, 'كشوف الحسابات المصرفية', 'creation', 'desc');">
          <div class="bir-hu-nav-icon"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M3 10h18M5 6l7-3 7 3M4 10v11M20 10v11M8 14v3M12 14v3M16 14v3"/></svg></div>
          <div class="bir-hu-nav-content">
            <strong>كشوف الحسابات المصرفية</strong>
            <span>متابعة كشوف الحسابات والبنود</span>
          </div>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" class="bir-hu-nav-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

        <button class="bir-hu-nav-item" onclick="openBirFilteredList('Bir Bank Statement Entry', {}, 'بنود كشوف الحساب المصرفي', 'creation', 'desc');">
          <div class="bir-hu-nav-icon"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div>
          <div class="bir-hu-nav-content">
            <strong>بنود كشوف الحساب المصرفي</strong>
            <span>عرض قيود كشف الحساب والعمليات</span>
          </div>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" class="bir-hu-nav-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

        <button class="bir-hu-nav-item" onclick="openBirFilteredList('Bank', {}, 'دليل المصارف المعتمدة');">
          <div class="bir-hu-nav-icon"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg></div>
          <div class="bir-hu-nav-content">
            <strong>المصارف المعتمدة</strong>
            <span>دليل البنوك (مصرف الجمهورية،...)</span>
          </div>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" class="bir-hu-nav-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

        <button class="bir-hu-nav-item" onclick="openBirFilteredList('Bir Import Batch', {}, 'دفعات استيراد البيانات', 'creation', 'desc');">
          <div class="bir-hu-nav-icon"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg></div>
          <div class="bir-hu-nav-content">
            <strong>دفعات استيراد البيانات</strong>
            <span>أرشيف وسجل الدفعات المستوردة</span>
          </div>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" class="bir-hu-nav-arrow"><polyline points="15 18 9 12 15 6"/></svg>
        </button>

      </div>
    </section>

    <!-- قسم أعلى المشاريع الوقفية -->
    <section class="bir-hu-panel">
      <div class="bir-hu-panel-header">
        <h3 class="bir-hu-panel-title">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#d4af37" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
          <span>أعلى المشاريع الوقفية</span>
        </h3>
        <span class="bir-hu-sub-tag">حسب القيمة</span>
      </div>

      <div class="bir-v8-projects-list bir-hu-projects-list">
        <div class="bir-hu-loading">
          <div class="bir-hu-spinner"></div>
          <span>جاري جلب إحصائيات المشاريع...</span>
        </div>
      </div>
    </section>

  </div>

</div>
"""

    doc.style = """/* ---------------------------------------------------
 * الهوية البصرية لخدمات الحج والعمرة (Green & Gold Theme)
 * تطبيق التصميم الأنيق مع إبراز الأخضر الشريف (#0a5c36) والذهبي الملكي (#d4af37)
 * --------------------------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Tajawal:wght@400;500;700;800&display=swap');

.bir-hu-dashboard {
  direction: rtl;
  font-family: "Cairo", "Tajawal", "Inter", sans-serif;
  color: #1F2D26;
  background: #f8faf9;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
}

/* Header Banner - هوية الأخضر والذهبي */
.bir-hu-header {
  background: linear-gradient(135deg, #0a5c36 0%, #0e7344 60%, #063821 100%);
  border-radius: 14px;
  padding: 20px 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #ffffff;
  box-shadow: 0 6px 20px rgba(10, 92, 54, 0.18);
  border-bottom: 4px solid #d4af37;
  border-top: 1px solid rgba(212, 175, 55, 0.4);
  margin-bottom: 22px;
}

.bir-hu-brand {
  display: flex;
  align-items: center;
  gap: 18px;
}

.bir-hu-logo-box {
  width: 90px;
  height: 70px;
  border-radius: 12px;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px 10px;
  border: 2px solid #d4af37;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  flex-shrink: 0;
}

.bir-hu-logo-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.bir-hu-logo-fallback {
  color: #0a5c36;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bir-hu-titles {
  display: flex;
  flex-direction: column;
}

.bir-hu-org-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11.5px;
  color: #f3e5ab;
  font-weight: 600;
  margin-bottom: 4px;
}

.bir-hu-main-title {
  font-size: 21px;
  font-weight: 800;
  color: #ffffff;
  margin: 0;
  line-height: 1.3;
}

.bir-hu-gold-tag {
  color: #f3e5ab;
  font-weight: 700;
}

.bir-hu-sub-title {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.85);
  margin: 4px 0 0 0;
}

.bir-hu-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.bir-hu-live-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.15);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  color: #84f1b5;
  border: 1px solid rgba(255, 255, 255, 0.25);
}

.bir-hu-pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #84f1b5;
  box-shadow: 0 0 8px #84f1b5;
}

.bir-hu-clock-box {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #f3e5ab;
  font-size: 14px;
  font-weight: 700;
  background: rgba(0, 0, 0, 0.2);
  padding: 4px 12px;
  border-radius: 8px;
  border: 1px solid rgba(212, 175, 55, 0.3);
}

/* KPI Grid — أسلوب كروت الحج والعمرة .hu-kpi-card */
.bir-hu-kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.hu-kpi-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  border-top: 4px solid #0a5c36;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.hu-kpi-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(10, 92, 54, 0.12);
}

.hu-kpi-card.gold-accent {
  border-top-color: #d4af37;
}

.hu-kpi-card.alert-accent {
  border-top-color: #dc2626;
}

.hu-kpi-title {
  font-size: 0.88rem;
  font-weight: 700;
  color: #526058;
  margin-bottom: 8px;
}

.hu-kpi-value {
  font-size: 1.65rem;
  font-weight: 800;
  color: #0a5c36;
  line-height: 1.2;
}

.hu-kpi-value.gold {
  color: #b8901f;
}

.hu-kpi-value.alert {
  color: #dc2626;
}

.hu-kpi-value small {
  font-size: 0.85rem;
  font-weight: 700;
  color: #b8901f;
}

.bir-hu-progress-bar {
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  margin: 10px 0 6px 0;
  overflow: hidden;
}

.bir-hu-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #d4af37 0%, #0a5c36 100%);
  border-radius: 3px;
  transition: width 0.8s ease-in-out;
}

.bir-hu-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 11.5px;
  color: #718096;
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px solid #f0f4f2;
}

.bir-hu-action-link {
  color: #0a5c36;
  font-weight: 700;
  transition: color 0.2s;
}

.bir-hu-action-link.gold {
  color: #b8901f;
}

.bir-hu-action-link.alert {
  color: #dc2626;
}

.hu-kpi-card:hover .bir-hu-action-link {
  text-decoration: underline;
}

/* Layout Panels */
.bir-hu-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

@media (max-width: 992px) {
  .bir-hu-layout {
    grid-template-columns: 1fr;
  }
}

.bir-hu-panel {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  border-top: 3px solid #0a5c36;
}

.bir-hu-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid #edf2f0;
}

.bir-hu-panel-title {
  font-size: 15px;
  font-weight: 800;
  color: #0a5c36;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.bir-hu-sub-tag {
  font-size: 11px;
  color: #b8901f;
  background: #fdfbf7;
  border: 1px solid #f3e5ab;
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 600;
}

/* Navigation Items */
.bir-hu-nav-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
}

.bir-hu-nav-item {
  background: #fbfdfc;
  border: 1px solid #e1e9e5;
  border-right: 4px solid #0a5c36;
  border-radius: 10px;
  padding: 14px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  text-align: right;
  transition: all 0.25s ease;
}

.bir-hu-nav-item:hover {
  background: #0a5c36;
  color: #ffffff;
  border-color: #0a5c36;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(10, 92, 54, 0.2);
}

.bir-hu-nav-item.primary {
  border-right-color: #d4af37;
}

.bir-hu-nav-icon {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  background: #eef6f2;
  color: #0a5c36;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.25s ease;
}

.bir-hu-nav-item:hover .bir-hu-nav-icon {
  background: rgba(255, 255, 255, 0.2);
  color: #f3e5ab;
}

.bir-hu-nav-content {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.bir-hu-nav-content strong {
  font-size: 13px;
  color: #1a2e24;
  font-weight: 700;
}

.bir-hu-nav-content span {
  font-size: 11px;
  color: #64748b;
  margin-top: 2px;
}

.bir-hu-nav-item:hover .bir-hu-nav-content strong {
  color: #ffffff;
}

.bir-hu-nav-item:hover .bir-hu-nav-content span {
  color: #e2e8f0;
}

.bir-hu-nav-arrow {
  color: #94a3b8;
  transition: transform 0.25s ease, color 0.25s ease;
}

.bir-hu-nav-item:hover .bir-hu-nav-arrow {
  color: #f3e5ab;
  transform: translateX(-4px);
}

/* Projects List */
.bir-hu-projects-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.bir-v8-proj-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: #fbfdfc;
  border-radius: 8px;
  border: 1px solid #e1e9e5;
  border-right: 3px solid #d4af37;
  transition: background 0.2s;
}

.bir-v8-proj-row:hover {
  background: #f4f8f6;
}

.bir-v8-proj-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.bir-v8-rank {
  background: #0a5c36;
  color: #ffffff;
  font-size: 10.5px;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 6px;
}

.bir-v8-proj-title {
  font-size: 12.5px;
  font-weight: 700;
  color: #0a5c36;
}

.bir-v8-proj-amount {
  font-size: 13.5px;
  font-weight: 800;
  color: #b8901f;
}

.bir-v8-proj-amount small {
  font-size: 10px;
  color: #64748b;
}

.bir-hu-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 20px;
  color: #64748b;
  font-size: 12px;
}

.bir-hu-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid #e2e8f0;
  border-top-color: #0a5c36;
  border-radius: 50%;
  animation: birHuSpin 0.8s linear infinite;
}

@keyframes birHuSpin {
  to { transform: rotate(360deg); }
}
"""

    doc.script = """// Robust Filtered List Opener Script for Bir Waqf Dashboard Block - Hajj & Umrah Theme
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
						mbVal.innerHTML = mbVal + ' <small>د.ل</small>';
					}

					var bskSubEl = wrapper.querySelector('.val-basket-count-sub');
					if (bskSubEl) {
						bskSubEl.innerText = (stats.basket_count || 0).toLocaleString('ar-LY') + ' معاملة سلة بالمشاريع';
					}

					// 8. Top Projects List
					var projContainer = wrapper.querySelector('.bir-hu-projects-list');
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
							projContainer.innerHTML = '<div class="bir-v8-empty" style="text-align:center;padding:15px;color:#94a3b8;font-size:12px;">لا توجد بيانات مشاريع سلة حالياً</div>';
						}
					}
				}
			}
		});
	}

	setTimeout(fetchStats, 100);
})(typeof root_element !== 'undefined' ? root_element : document);
"""

    doc.flags.ignore_permissions = True
    doc.save()
    frappe.db.commit()
    print("SUCCESSFULLY UPDATED BIR WAQF DASHBOARD BLOCK WITH HAJJ & UMRAH GREEN & GOLD THEME!")

if __name__ == "__main__":
    run()
