frappe.ui.form.on('Project', {
    onload:function (frm) {
        setTimeout(() => {
            $("[data-doctype='Expense Claim']").hide();
        }, 10);
    }
})
frappe.ui.form.on('Quotation Copy', {
    quotation_copy_items_add:function (frm,cdt,cdn) {
        frappe.model.set_value(cdt,cdn,"attached_by",frappe.session.user)
    }
})
frappe.ui.form.on('Supplier Final Copies', {
    supplier_final_copies_add:function (frm,cdt,cdn) {
        frappe.model.set_value(cdt,cdn,"attached_by",frappe.session.user)
    }
})