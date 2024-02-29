frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        setTimeout(()=>{
            cur_frm.remove_custom_button('Quality Inspection(s)', 'Create')
            cur_frm.remove_custom_button('Delivery', 'Create')
            cur_frm.remove_custom_button('Payment Request', 'Create')
            cur_frm.remove_custom_button('Invoice Discounting', 'Create')
            cur_frm.remove_custom_button('Maintenance Schedule', 'Create')
            cur_frm.remove_custom_button('Subscription', 'Create')
            cur_frm.remove_custom_button('Sales Order', 'Get Items From')
            cur_frm.remove_custom_button('Delivery Note', 'Get Items From')
            cur_frm.remove_custom_button('Fetch Timesheet')
        }, 500)
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
