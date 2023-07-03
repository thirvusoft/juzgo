// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hotel Details', {
	refresh: function(frm) {
		frm.set_query("nearby_places_table", function () {
			return { filters:{destination: frm.doc.destination }};
		});
		frm.set_query("nearby_indian_restaurants", function () {
			return { filters:{type: "India" }};
		});
	},
	open_website: function(frm){
        if(!frm.doc.website_link){
            cur_frm.scroll_to_field('website_link')
            frappe.throw('Enter WebSite Link')
        }
        else{
        window.open(frm.doc.website_link, '_blank')
        }
    },
	open_pin_location: function(frm){
        if(!frm.doc.pin_location){
            cur_frm.scroll_to_field('pin_location')
            frappe.throw('Enter Pin Location')
        }
        else{
        window.open(frm.doc.pin_location, '_blank')
        }
    },
});
