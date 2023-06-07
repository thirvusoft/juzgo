frappe.ui.form.on('Project', {
    onload:function (frm) {
        setTimeout(() => {
            $("[data-doctype='Expense Claim']").hide();
            // $("[class='col-md-4']").hide();
        }, 10);
    }
})