frappe.ui.form.on('Salary Slip', {
    refresh: function(frm) {
        frappe.call({
            method: 'juzgo.juzgo.custom.py.salary_slip.get_last_from_date',
            args: {
                'employee': frm.doc.employee,
                'salary_structure': frm.doc.salary_structure,
                'posting_date': frm.doc.posting_date
            },
            callback: function(response) {
                if (response && response.message) {
                    var lastRecord = response.message;
                    frm.set_value('salary_amount', lastRecord.base);
                }
            }
        });
    }
});
