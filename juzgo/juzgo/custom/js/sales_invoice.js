frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        if(frm.doc.docstatus == 1) {
			frm.add_custom_button(__('Customer Statement'), function() {
				frappe.call({
                    method: 'juzgo.juzgo.custom.py.sales_invoice.customer_statement',
                    args: {
                        doc:frm.doc
                    },
                    callback(r){
                        if(r.message){
                            window.open(r.message);
                        }
                    }
                })
			});
		}
    }
});
