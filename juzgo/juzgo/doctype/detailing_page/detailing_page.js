// Copyright (c) 2024, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Detailing Page', {
    validate: function(frm) {
        if(frm.doc.ca_form){
            frappe.call({
                method: "juzgo.juzgo.doctype.detailing_page.detailing_page.ca_form_details",
                args: {ca_form:frm.doc.ca_form},
                callback: function(r){
                    let child_count = r.message[0].no_of_childrens +r.message[0].child_without_bed
                    setTimeout(() => {
                        frm.set_value("no_of_child" , child_count );
                    }, 300)
                    
                }
            })
        }
    }
});

frappe.ui.form.on('Visa Supplier Table', {
    destination: function(frm, cdt, cdn){
        if(frm.doc.ca_form){
            frappe.call({
                method: "juzgo.juzgo.doctype.detailing_page.detailing_page.ca_form_details",
                args: {ca_form:frm.doc.ca_form},
                callback: function(r){
                    let child_count = r.message[0].no_of_childrens +r.message[0].child_without_bed
                    setTimeout(() => {
                        frappe.model.set_value(cdt,cdn, "travel_from_dates" , r.message[0].travel_start_date );
                        frappe.model.set_value(cdt,cdn, "travel_to_dates" , r.message[0].travel_end_date );
                        frappe.model.set_value(cdt,cdn, "no_of_adults" , r.message[0].no_of_adult );
                        frappe.model.set_value(cdt,cdn, "no_of_child" , child_count );
                    }, 300)
                    
                }
            })
        }
    },
    supplier: function(frm, cdt, cdn){
        if(frm.doc.ca_form){
            frappe.call({
                method: "juzgo.juzgo.doctype.detailing_page.detailing_page.ca_form_details",
                args: {ca_form:frm.doc.ca_form},
                callback: function(r){
                    let child_count = r.message[0].no_of_childrens +r.message[0].child_without_bed
                    setTimeout(() => {
                        frappe.model.set_value(cdt,cdn, "travel_from_dates" , r.message[0].travel_start_date );
                        frappe.model.set_value(cdt,cdn, "travel_to_dates" , r.message[0].travel_end_date );
                        frappe.model.set_value(cdt,cdn, "no_of_adults" , r.message[0].no_of_adult );
                        frappe.model.set_value(cdt,cdn, "no_of_child" , child_count );
                    }, 300)
                    
                }
            })
        }
    }
})