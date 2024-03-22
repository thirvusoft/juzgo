var branch = "" // initiating the branch value

frappe.ui.form.on('Purchase Invoice', {

    branch: function(frm) {
        branch = frm.doc.branch  // setting the branch variable value
        
    },
    refresh: function(frm){
        setTimeout(()=>{
            cur_frm.remove_custom_button('Quality Inspection(s)', 'Create')
            cur_frm.remove_custom_button('Purchase Receipt', 'Create')
            cur_frm.remove_custom_button('Block Invoice', 'Create')
            cur_frm.remove_custom_button('Subscription', 'Create')
            cur_frm.remove_custom_button('Payment Request', 'Create')
            cur_frm.remove_custom_button('Purchase Order', 'Get Items From')
            cur_frm.remove_custom_button('Purchase Receipt', 'Get Items From')
        }, 1000)
    }
})


frappe.ui.form.on('Purchase Invoice Item', {
    item_code(frm, cdt, cdn) {
            frappe.model.set_value(cdt , cdn, "branch", branch); // set the branch value to the child table field
    }
});