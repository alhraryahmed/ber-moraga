frappe.provide("bir_waqf");

$(document).ready(function() {
    // Monitor modal dialogs opening in Frappe Desk
    const observer = new MutationObserver(function() {
        const $modal = $('.modal.show, .modal.in, .modal-dialog');
        if ($modal.length) {
            $modal.each(function() {
                const $m = $(this);
                const title = $m.find('.modal-title').text() || '';
                if (title.indexOf('جلب المعاملات') !== -1) {
                    const $proj_field = $m.find('[data-fieldname="projects"]');
                    if ($proj_field.length && !$proj_field.find('#btn-fetch-all-linked-projects-dialog').length) {
                        const btn_html = `
                            <div style="margin-top: 10px; margin-bottom: 6px;" id="wrapper-btn-fetch-projects">
                                <button type="button" class="btn btn-sm btn-dark" id="btn-fetch-all-linked-projects-dialog" style="background-color: #000000 !important; color: #ffffff !important; font-weight: bold; border-radius: 6px; padding: 7px 18px; border: none; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 2px 6px rgba(0,0,0,0.25); font-size: 13px;">
                                    <span>جلب جميع المشاريع المرتبطة</span>
                                </button>
                            </div>
                            <div style="font-size: 11px; color: #64748b; margin-top: 4px;">اختر مشروعاً أو أكثر لجلب معاملاتها، أو اتركه فارغاً لجلب كافة المعاملات</div>
                        `;
                        
                        const $help = $proj_field.find('.help-box');
                        if ($help.length) {
                            $help.html(btn_html);
                        } else {
                            $proj_field.append(btn_html);
                        }
                    }
                }
            });
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });

    // Handle button click event globally
    $(document).off('click.global_fetch_projs').on('click.global_fetch_projs', '#btn-fetch-all-linked-projects-dialog', function(e) {
        e.preventDefault();
        e.stopPropagation();

        var batch = '';
        var bank = '';

        if (window.cur_dialog) {
            batch = cur_dialog.get_value('import_batch') || '';
            bank = cur_dialog.get_value('bank') || '';
        }

        if (!batch) {
            const $batch_input = $('[data-fieldname="import_batch"] input');
            if ($batch_input.length) batch = $batch_input.val();
        }

        if (!bank) {
            const $bank_input = $('[data-fieldname="bank"] input');
            if ($bank_input.length) bank = $bank_input.val();
        }

        if (!batch) {
            frappe.msgprint(__('يرجى اختيار دفعة الاستيراد (Import Batch) أولاً.'));
            return;
        }

        frappe.show_alert({message: __('جاري البحث عن جميع المشاريع المرتبطة بالدفعة والمصرف...'), indicator: 'blue'});

        frappe.call({
            method: 'bir_waqf.api.get_all_linked_projects',
            args: { import_batch: batch, bank: bank },
            callback: function(r) {
                if (r.message && r.message.length > 0) {
                    var proj_str = r.message.join(', ');
                    if (window.cur_dialog) {
                        cur_dialog.set_value('projects', proj_str);
                    } else {
                        const $proj_input = $('[data-fieldname="projects"] input');
                        if ($proj_input.length) {
                            $proj_input.val(proj_str).trigger('change');
                        }
                    }
                    frappe.show_alert({
                        message: __('تم جلب وتحديد {0} مشروع مرتبط بالدفعة والمصرف بنجاح.', [r.message.length]),
                        indicator: 'green'
                    });
                } else {
                    frappe.msgprint(__('لم يتم العثور على أي مشاريع مرتبطة بالدفعة والمصرف المحددين.'));
                }
            }
        });
    });
});
