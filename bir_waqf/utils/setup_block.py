import frappe, json

def setup_custom_block():
	block_name = "Bir Waqf Dashboard Block"
	
	html_content = """<div class="bir-dashboard-container">
  <div class="bir-banner">
    <div class="bir-banner-brand">
      <img src="/files/Screenshot 2026-07-23 013547.png" alt="الشعار" class="bir-logo-img" onerror="this.style.display='none'">
      <div>
        <h1 class="bir-banner-title">منصة البر الوقفية — مركز التحليل والمطابقة المصرفية</h1>
        <p class="bir-banner-sub">الهيئة العامة للأوقاف والشؤون الإسلامية — لوحة الإدارة والمراجعة الفورية</p>
      </div>
    </div>
    <div class="bir-banner-right">
      <span class="bir-live-badge"><i class="fa fa-circle"></i> النظام نشط وتفاعلي</span>
      <div id="bir-clock" class="bir-clock">--:--:--</div>
    </div>
  </div>

  <div class="bir-kpi-grid">
    <div class="bir-kpi-card emerald" id="kpi-total">
      <div class="bir-kpi-icon"><i class="fa fa-money"></i></div>
      <div class="bir-kpi-info">
        <div class="bir-kpi-label">إجمالي التبرعات والمساهمات</div>
        <div class="bir-kpi-val" id="val-total-amount">0.00 <small>ل.د</small></div>
        <div class="bir-kpi-sub" id="val-total-count">0 معاملة مسجلة</div>
      </div>
    </div>

    <div class="bir-kpi-card gold" id="kpi-matched">
      <div class="bir-kpi-icon"><i class="fa fa-check-circle"></i></div>
      <div class="bir-kpi-info">
        <div class="bir-kpi-label">المعاملات المطابقة مصرفياً</div>
        <div class="bir-kpi-val" id="val-matched-count">0</div>
        <div class="bir-progress-bar"><div class="bir-progress-fill" id="val-matched-progress" style="width: 0%;"></div></div>
        <div class="bir-kpi-sub" id="val-matched-pct">0% نسبة المطابقة الآلية</div>
      </div>
    </div>

    <div class="bir-kpi-card crimson" id="kpi-exceptions">
      <div class="bir-kpi-icon"><i class="fa fa-exclamation-triangle"></i></div>
      <div class="bir-kpi-info">
        <div class="bir-kpi-label">حالات تحتاج مراجعة / استثناءات</div>
        <div class="bir-kpi-val" id="val-exceptions-count">0</div>
        <div class="bir-kpi-sub">تتطلب تدقيق يدوي</div>
      </div>
    </div>

    <div class="bir-kpi-card blue" id="kpi-basket">
      <div class="bir-kpi-icon"><i class="fa fa-shopping-basket"></i></div>
      <div class="bir-kpi-info">
        <div class="bir-kpi-label">معاملات السلة متعددة المشاريع</div>
        <div class="bir-kpi-val" id="val-basket-count">0</div>
        <div class="bir-kpi-sub">موزعة على المشاريع الفرعية</div>
      </div>
    </div>
  </div>

  <div class="bir-actions-section">
    <div class="bir-section-title"><i class="fa fa-bolt"></i> إجراءات واختصارات سريعة</div>
    <div class="bir-actions-grid">
      <button class="bir-btn-action" onclick="frappe.set_route('page', 'bir_data_processor')">
        <div class="bir-btn-icon"><i class="fa fa-cloud-upload"></i></div>
        <div class="bir-btn-text">
          <strong>مركز معالجة الملفات</strong>
          <span>رفع كشوف المنصة والبنك</span>
        </div>
      </button>

      <button class="bir-btn-action" onclick="frappe.set_route('List', 'Bir Bank Statement')">
        <div class="bir-btn-icon"><i class="fa fa-university"></i></div>
        <div class="bir-btn-text">
          <strong>كشوف الحساب المصرفية</strong>
          <span>استجلاب كشوفات البنوك</span>
        </div>
      </button>

      <button class="bir-btn-action" onclick="frappe.set_route('List', 'Bir Transaction')">
        <div class="bir-btn-icon"><i class="fa fa-list-alt"></i></div>
        <div class="bir-btn-text">
          <strong>جميع المعاملات</strong>
          <span>طباعة واستعراض الجدول</span>
        </div>
      </button>

      <button class="bir-btn-action" onclick="frappe.set_route('List', 'Bir Import Batch')">
        <div class="bir-btn-icon"><i class="fa fa-folder-open"></i></div>
        <div class="bir-btn-text">
          <strong>دفعات الاستيراد</strong>
          <span>سجل الدفعات المستوردة</span>
        </div>
      </button>
    </div>
  </div>

  <div class="bir-projects-section">
    <div class="bir-section-title"><i class="fa fa-trophy"></i> أعلى المشاريع الوقفيّة استقبالاً للتبرعات</div>
    <div id="bir-top-projects-container" class="bir-projects-list">
      <div class="bir-loading-text">جاري تحميل البيانات...</div>
    </div>
  </div>
</div>"""

	style_content = """@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@700&family=Tajawal:wght@400;500;700;800&display=swap');

.bir-dashboard-container {
  direction: rtl;
  font-family: 'Tajawal', sans-serif;
  color: #1C2B24;
  background: linear-gradient(135deg, #FAF7F0 0%, #F4EFE6 100%);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(11, 61, 46, 0.05);
  margin-bottom: 24px;
}

.bir-banner {
  background: linear-gradient(135deg, #0B3D2E 0%, #145C43 60%, #1C2B24 100%);
  border-radius: 14px;
  padding: 20px 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #fff;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(11, 61, 46, 0.25);
  border: 1px solid rgba(198, 161, 91, 0.4);
}

.bir-banner-brand {
  display: flex;
  align-items: center;
  gap: 18px;
}
.bir-logo-img {
  max-height: 58px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  background: #fff;
  padding: 4px;
}
.bir-banner-title {
  font-family: 'Amiri', serif;
  font-size: 22px;
  font-weight: 700;
  margin: 0;
  color: #fff;
}
.bir-banner-sub {
  font-size: 12.5px;
  color: #E8D5A3;
  margin-top: 4px;
}

.bir-banner-right {
  text-align: left;
}
.bir-live-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.25);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  color: #8CF0B3;
}
.bir-clock {
  font-size: 16px;
  font-weight: 700;
  color: #C6A15B;
  margin-top: 6px;
  font-family: 'Tajawal', sans-serif;
}

.bir-kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-top: 20px;
}

.bir-kpi-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 18px 20px;
  display: flex;
  align-items: flex-start;
  gap: 14px;
  border: 1px solid #EAE3D2;
  box-shadow: 0 4px 14px rgba(0,0,0,0.03);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.bir-kpi-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(11, 61, 46, 0.1);
  border-color: #C6A15B;
}

.bir-kpi-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}
.bir-kpi-card.emerald .bir-kpi-icon { background: #EAF2EE; color: #0B3D2E; }
.bir-kpi-card.gold .bir-kpi-icon { background: #FAF3E3; color: #C6A15B; }
.bir-kpi-card.crimson .bir-kpi-icon { background: #FDECEC; color: #A03A3A; }
.bir-kpi-card.blue .bir-kpi-icon { background: #EBF4FC; color: #1B60A5; }

.bir-kpi-label { font-size: 11.5px; color: #5C6B63; font-weight: 500; }
.bir-kpi-val { font-size: 22px; font-weight: 800; color: #0B3D2E; font-family: 'Amiri', serif; margin-top: 3px; }
.bir-kpi-val small { font-size: 12px; font-family: 'Tajawal', sans-serif; color: #C6A15B; font-weight: 700; }
.bir-kpi-sub { font-size: 11px; color: #889990; margin-top: 4px; }

.bir-progress-bar {
  height: 6px;
  background: #EAE3D2;
  border-radius: 3px;
  margin-top: 8px;
  overflow: hidden;
}
.bir-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #C6A15B 0%, #0B3D2E 100%);
  border-radius: 3px;
  transition: width 0.8s ease-in-out;
}

.bir-actions-section, .bir-projects-section {
  margin-top: 24px;
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #EAE3D2;
  box-shadow: 0 4px 14px rgba(0,0,0,0.02);
}

.bir-section-title {
  font-size: 14px;
  font-weight: 700;
  color: #0B3D2E;
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.bir-section-title i { color: #C6A15B; }

.bir-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.bir-btn-action {
  background: #FAF7F0;
  border: 1px solid #E6DEC9;
  border-radius: 10px;
  padding: 14px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  text-align: right;
  transition: all 0.2s ease;
}
.bir-btn-action:hover {
  background: #0B3D2E;
  color: #fff;
  border-color: #0B3D2E;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(11,61,46,0.15);
}
.bir-btn-action:hover .bir-btn-icon { background: rgba(255,255,255,0.15); color: #E8D5A3; }
.bir-btn-action:hover .bir-btn-text strong { color: #fff; }
.bir-btn-action:hover .bir-btn-text span { color: #D1E3DB; }

.bir-btn-icon {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  background: #EAF2EE;
  color: #0B3D2E;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
  transition: all 0.2s ease;
}
.bir-btn-text { display: flex; flex-direction: column; }
.bir-btn-text strong { font-size: 12.5px; color: #1C2B24; }
.bir-btn-text span { font-size: 10.5px; color: #708078; margin-top: 2px; }

.bir-projects-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.bir-project-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: #FAF7F0;
  border-radius: 8px;
  border: 1px solid #EAE3D2;
}
.bir-project-name { font-size: 12.5px; font-weight: 700; color: #0B3D2E; }
.bir-project-val { font-size: 14px; font-weight: 700; color: #C6A15B; font-family: 'Amiri', serif; }
"""

	script_content = """// Live Dashboard Script
setInterval(function() {
	var now = new Date();
	var clock = document.getElementById('bir-clock');
	if (clock) {
		clock.innerText = now.toLocaleTimeString('ar-LY');
	}
}, 1000);

frappe.call({
	method: 'bir_waqf.api.get_dashboard_stats',
	callback: function(r) {
		if (r.message) {
			var stats = r.message;
			var amtEl = document.getElementById('val-total-amount');
			if (amtEl) amtEl.innerHTML = stats.total_donations.toLocaleString('ar-LY', {minimumFractionDigits:2}) + ' <small>ل.د</small>';
			
			var cntEl = document.getElementById('val-total-count');
			if (cntEl) cntEl.innerText = stats.total_transactions + ' معاملة مسجلة';
			
			var matchEl = document.getElementById('val-matched-count');
			if (matchEl) matchEl.innerText = stats.matched_transactions;
			
			var pct = stats.total_transactions > 0 ? Math.round((stats.matched_transactions / stats.total_transactions) * 100) : 0;
			var pctEl = document.getElementById('val-matched-pct');
			if (pctEl) pctEl.innerText = pct + '% نسبة المطابقة الآلية';
			
			var prgEl = document.getElementById('val-matched-progress');
			if (prgEl) prgEl.style.width = pct + '%';
			
			var excEl = document.getElementById('val-exceptions-count');
			if (excEl) excEl.innerText = stats.exceptions_count;
			
			var bskEl = document.getElementById('val-basket-count');
			if (bskEl) bskEl.innerText = stats.basket_count;
			
			var projContainer = document.getElementById('bir-top-projects-container');
			if (projContainer && stats.top_projects && stats.top_projects.length > 0) {
				var projHtml = '';
				stats.top_projects.forEach(function(p) {
					projHtml += '<div class="bir-project-item">' +
						'<div class="bir-project-name"><i class="fa fa-bookmark" style="color:#C6A15B; margin-left:6px;"></i> ' + p.project_name + '</div>' +
						'<div class="bir-project-val">ل.د ' + p.total.toLocaleString('ar-LY', {minimumFractionDigits:2}) + '</div>' +
					'</div>';
				});
				projContainer.innerHTML = projHtml;
			} else if (projContainer) {
				projContainer.innerHTML = '<div style="font-size:12px; color:#888;">لا توجد إحصائيات مشاريع حالية.</div>';
			}
		}
	}
});
"""

	if frappe.db.exists("Custom HTML Block", block_name):
		block_doc = frappe.get_doc("Custom HTML Block", block_name)
	else:
		block_doc = frappe.new_doc("Custom HTML Block")
		block_doc.name = block_name
		block_doc.private = 0

	block_doc.html = html_content
	block_doc.style = style_content
	block_doc.script = script_content
	block_doc.flags.ignore_permissions = True
	block_doc.save()
	frappe.db.commit()
	return block_doc.name
