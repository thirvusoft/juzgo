frappe.ui.form.on('Lead', {
    refresh(frm){
        setTimeout(()=>{
            cur_frm.remove_custom_button('Opportunity', 'Create')
            cur_frm.remove_custom_button('Prospect', 'Create')
            cur_frm.remove_custom_button('Quotation', 'Create')
            frm.add_custom_button(__('CA Form'), function() {
				frappe.model.open_mapped_doc({
                    method: "juzgo.juzgo.custom.py.lead.make_ca_form",
                    frm: cur_frm
                })
			}, "Create");
        },300)
    }
})