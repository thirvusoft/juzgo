// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Restaurant', {
	open_url: function(frm){
        if(!frm.doc.pin_location){
            cur_frm.scroll_to_field('pin_location')
            frappe.throw('Enter Pin Location')
        }
        else{
        window.open(frm.doc.pin_location, '_blank')
        }
    },
});
