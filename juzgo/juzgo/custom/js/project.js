frappe.ui.form.on('Project', {
    onload:function (frm) {
        setTimeout(() => {
            $("[data-doctype='Expense Claim']").hide();
        }, 10);
    },
    project_name:function(frm){
        frappe.call({
            
            method: "juzgo.juzgo.custom.py.project.get_project_abbr",
            args:{
                project_name:frm.doc.project_name,
            },
            callback: function(r) {
				frm.set_value("abbr",r.message)
				

        }
        })    
    },
    no_of_days: function(frm){
        frm.set_value("no_of_nights",frm.doc.no_of_days-1)
        auto_end_date(frm)
    },
    no_of_nights: function(frm){
        frm.set_value("no_of_days",frm.doc.no_of_nights+1)
        auto_end_date(frm)
    },
    travel_start_date: function(frm){
        auto_end_date(frm)
    },
    multi_customer: function(frm){
        let custom_list = []
        for(var i=0;i<frm.doc.multi_customer.length;i++){
            custom_list.push(frm.doc.multi_customer[i].customer)
        }
        if(custom_list){
            frappe.call({
                method: "juzgo.juzgo.custom.py.project.get_family_member_details_list",
                args:{
                    family_member_details :frm.doc.family_member_details,
                    custom_list : custom_list
                },
                callback: function(r) {
                    frm.doc.family_member_details = []
                    r.message.forEach(row => {
                        let child = cur_frm.add_child("family_member_details")
                        frappe.model.set_value(child.doctype, child.name, "members_name", row.members_name)
                        frappe.model.set_value(child.doctype, child.name, "date_of_birth", row.date_of_birth)
                        frappe.model.set_value(child.doctype, child.name, "gender", row.gender)
                        frappe.model.set_value(child.doctype, child.name, "age", row.age)
                        frappe.model.set_value(child.doctype, child.name, "relationship", row.relationship)
                        frappe.model.set_value(child.doctype, child.name, "member_row_id", row.member_row_id)
                        frappe.model.set_value(child.doctype, child.name, "customer_id", row.customer_id)
                    });
                    refresh_field("family_member_details");
                }
            }) 
            frappe.call({
                method: "juzgo.juzgo.custom.py.project.get_family_member_attachment",
                args:{
                    family_members_attachment :frm.doc.family_members_attachment,
                    custom_list : custom_list
                },
                callback: function(r) {
                    frm.doc.family_members_attachment = []
                    r.message.forEach(row => {
                        let child = cur_frm.add_child("family_members_attachment")
                        frappe.model.set_value(child.doctype, child.name, "members_name", row.members_name)
                        frappe.model.set_value(child.doctype, child.name, "file_type", row.file_type)
                        frappe.model.set_value(child.doctype, child.name, "file", row.file)
                        frappe.model.set_value(child.doctype, child.name, "next_remainder_or_expiry_on", row.next_remainder_or_expiry_on)
                        frappe.model.set_value(child.doctype, child.name, "description", row.description)
                        frappe.model.set_value(child.doctype, child.name, "attached_by", row.attached_by)
                        frappe.model.set_value(child.doctype, child.name, "family_members_documents_name", row.family_members_documents_name)
                        frappe.model.set_value(child.doctype, child.name, "customer_id", row.customer_id)
                    });
                    refresh_field("family_members_attachment");
                    frm.save()
                }
            })
        }
    },
    destination: function(frm){
        add_destination_details(frm)
    }
})

frappe.ui.form.on('Quotation Copy', {
    quotation_copy_items_add:function (frm,cdt,cdn) {
        frappe.model.set_value(cdt,cdn,"attached_by",frappe.session.user)
    }
})
frappe.ui.form.on('Supplier Final Copies', {
    supplier_final_copies_add:function (frm,cdt,cdn) {
        frappe.model.set_value(cdt,cdn,"attached_by",frappe.session.user)
    }
})

function auto_end_date(frm){
    if(frm.doc.travel_start_date && frm.doc.no_of_nights){
        frm.set_value("travel_end_date",frappe.datetime.add_days(frm.doc.travel_start_date, frm.doc.no_of_nights))
    } else {
        frm.set_value("travel_end_date","")
    }
    
}

function add_destination_details(frm){
        let destination_list = []
        for(var i=0;i<frm.doc.destination.length;i++){
            destination_list.push(frm.doc.destination[i].destination)
        }
        frappe.call({
            method:'juzgo.juzgo.custom.py.project.add_destination_details',
            args:{
                name:frm.doc.name,
                destination:destination_list
            },
            callback(r1){
                if(r1.message){
                    frm.doc.destination_check_list = []
                    r1.message.forEach(row => {
                        let child = cur_frm.add_child("destination_check_list")
                        frappe.model.set_value(child.doctype, child.name, "members_name", row.members_name)
                        frappe.model.set_value(child.doctype, child.name, "age", row.age)
                        frappe.model.set_value(child.doctype, child.name, "gender", row.gender)
                        frappe.model.set_value(child.doctype, child.name, "check_list_name", row.check_list_name)
                        frappe.model.set_value(child.doctype, child.name, "family_member_details_name", row.family_member_details_name)
                        frappe.model.set_value(child.doctype, child.name, "check", row.check)
                        frappe.model.set_value(child.doctype, child.name, "destination", row.destination)
                        frappe.model.set_value(child.doctype, child.name, "customer_id", row.customer_id)
                    });
                    refresh_field("destination_check_list");
                    frm.save()
                }
            }
        })
}