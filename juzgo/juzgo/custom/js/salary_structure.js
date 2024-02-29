frappe.ui.form.on('Salary Structure', {
    refresh: function(frm){
        setTimeout(()=>{
            cur_frm.remove_custom_button('Preview Salary Slip', 'Actions')
        },300)
    }
})