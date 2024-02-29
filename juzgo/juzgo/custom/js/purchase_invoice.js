frappe.ui.form.on('Purchase Invoice', {
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