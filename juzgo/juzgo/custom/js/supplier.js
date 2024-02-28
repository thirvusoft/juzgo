frappe.ui.form.on('Supplier', {
    refresh: function(frm){
        setTimeout(()=>{
            cur_frm.remove_custom_button('Get Supplier Group Details', 'Actions')
            cur_frm.remove_custom_button('Bank Account', 'Create')
            cur_frm.remove_custom_button('Pricing Rule', 'Create')
        },300)
    }
})