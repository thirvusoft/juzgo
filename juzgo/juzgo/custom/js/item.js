frappe.ui.form.on('Item', {
    refresh: function(frm){
        setTimeout(()=>{
            cur_frm.remove_custom_button('Publish in Website', 'Actions')
            cur_frm.remove_custom_button('Add / Edit Prices', 'Actions')
        },300)
    }
})
