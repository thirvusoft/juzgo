var form
var form_destination_details = {}
var form_destination
frappe.ui.form.on('Project', {
    refresh:function (frm,cdt,cdn) {
        console.log(frm.doc.family_members_attachment)
        if(frm.doc.family_members_attachment.length > 0){
            let fields=[
                {
                    fieldtype: 'Read Only',
                    fieldname: 'members_name',
                    label: __('Members Name'),
                }, 
                {
                    fieldtype: 'Read Only',
                    fieldname: 'file_type',
                    label: __('File Type'),
                    in_list_view: 1,
                    columns:2
                },
                {
                    fieldtype: 'Attach',
                    fieldname: 'file',
                    label: __('File'),
                    in_list_view: 1,
                    columns:2,
                },
                {
                    fieldtype: 'Check',
                    fieldname: 'checkfile',
                    label: __('Attached'),
                    in_list_view: 1,
                    columns:1,
                    onchange: function(event) {
                        let table = event.target.closest('[data-fieldtype="Table"]').getAttribute('data-fieldname');
                        let index = parseInt(event.target.closest('.grid-row').getAttribute('data-idx'))-1
                        let htmlrow = form.get_field(table).get_value()[index]
                        frm.doc.family_members_attachment.forEach((el) => {
                            if(htmlrow.parent_name1 == el.name){
                                frappe.model.set_value(el.doctype, el.name, 'attached_by', frappe.session.user)
                                frappe.model.set_value(el.doctype, el.name, 'file', htmlrow.file)
                            }
                        });
                    }
                },
                {
                    fieldtype: 'Date',
                    fieldname: 'next_remainder_or_expiry_on',
                    label: __('Next remainder or expiry on'),
                    in_list_view: 1,
                    columns:2,
                    onchange: function(event) {
                        let table = event.target.closest('[data-fieldtype="Table"]').getAttribute('data-fieldname');
                        let index = parseInt(event.target.closest('.grid-row').getAttribute('data-idx'))-1
                        let htmlrow = form.get_field(table).get_value()[index]
                        frm.doc.family_members_attachment.forEach((el) => {
                            if(htmlrow.parent_name1 == el.name){
                                frappe.model.set_value(el.doctype, el.name, 'next_remainder_or_expiry_on', htmlrow.next_remainder_or_expiry_on)
                            }
                            
                        });
                    }
                },
                {
                    fieldtype: 'Small Text',
                    fieldname: 'description',
                    label: __('Description'),
                    in_list_view: 1,
                    columns:2,
                    onchange: function(event) {
                        let table = event.target.closest('[data-fieldtype="Table"]').getAttribute('data-fieldname');
                        let index = parseInt(event.target.closest('.grid-row').getAttribute('data-idx'))-1
                        let htmlrow = form.get_field(table).get_value()[index]
                        frm.doc.family_members_attachment.forEach((el) => {
                            if(htmlrow.parent_name1 == el.name){
                                frappe.model.set_value(el.doctype, el.name, 'description', event.target.value)
                            }
                        });
                    }
                },
                {
                    fieldtype: 'Read Only',
                    fieldname: 'parent_name1',
                    label: __('Parent Name'),
                    hidden:1
                },
            ]
    
            
            let check_list = {}
            let file_table ={}
            let desti_attach_table ={}
            for(let i=0;i<frm.doc.family_member_details.length;i++){
                check_list[frm.doc.family_member_details[i].members_name]=[]
                file_table[frm.doc.family_member_details[i].members_name]=[]
                desti_attach_table[frm.doc.family_member_details[i].members_name]=[]
            }
            for(let i=0;i<frm.doc.family_members_attachment.length;i++){  
                file_table[frm.doc.family_members_attachment[i].members_name ].push(
                    {
                        members_name:frm.doc.family_members_attachment[i].members_name,
                        file_type:frm.doc.family_members_attachment[i].file_type,
                        file:frm.doc.family_members_attachment[i].file,
                        next_remainder_or_expiry_on:frm.doc.family_members_attachment[i].next_remainder_or_expiry_on,
                        description:frm.doc.family_members_attachment[i].description,
                        parent_name1:frm.doc.family_members_attachment[i].name,
                        checkfile:frm.doc.family_members_attachment[i].file?1:0
                    }
                )
            }
            for(let i=0;i<frm.doc.family_members_destination_attachment.length;i++){  
                desti_attach_table[frm.doc.family_members_destination_attachment[i].members_name ].push(
                    {
                        members_name:frm.doc.family_members_destination_attachment[i].members_name,
                        file_type:frm.doc.family_members_destination_attachment[i].file_type,
                        file:frm.doc.family_members_destination_attachment[i].file,
                        next_remainder_or_expiry_on:frm.doc.family_members_destination_attachment[i].next_remainder_or_expiry_on,
                        description:frm.doc.family_members_destination_attachment[i].description,
                        parent_name1:frm.doc.family_members_destination_attachment[i].name,
                        checkfile:frm.doc.family_members_destination_attachment[i].file?1:0
                    }
                )
            }
            let p=[]
            let keys=Object.keys(file_table);
            for(let i=0;i<keys.length;i++){
                var desti_table_field=[
                    {
                        fieldtype: 'Read Only',
                        fieldname: 'members_name',
                        label: __('Members Name'),
                    }, 
                    {
                        fieldtype: 'Read Only',
                        fieldname: 'file_type',
                        label: __('File Type'),
                        in_list_view: 1,
                        columns:2
                    },
                    {
                        fieldtype: 'Attach',
                        fieldname: 'file',
                        label: __('File'),
                        in_list_view: 1,
                        columns:2,
                    },
                    {
                        fieldtype: 'Check',
                        fieldname: 'checkfile',
                        label: __('Attached'),
                        in_list_view: 1,
                        columns:1,
                        onchange: function(event) {
                            let table = event.target.closest('[data-fieldtype="Table"]').getAttribute('data-fieldname');
                            let index = parseInt(event.target.closest('.grid-row').getAttribute('data-idx'))-1
                            let htmlrow = form_destination_details[table].get_field(table).get_value()[index]
                            frm.doc.family_members_destination_attachment.forEach((el) => {
                                if(htmlrow.parent_name1 == el.name){
                                    frappe.model.set_value(el.doctype, el.name, 'attached_by', frappe.session.user)
                                    frappe.model.set_value(el.doctype, el.name, 'file', htmlrow.file)
                                }
                            });
                        }
                    },
                    {
                        fieldtype: 'Date',
                        fieldname: 'next_remainder_or_expiry_on',
                        label: __('Next remainder or expiry on'),
                        in_list_view: 1,
                        columns:2,
                        onchange: function(event) {
                            let table = event.target.closest('[data-fieldtype="Table"]').getAttribute('data-fieldname');
                            let index = parseInt(event.target.closest('.grid-row').getAttribute('data-idx'))-1
                            let htmlrow = form_destination_details[table].get_field(table).get_value()[index]
                            frm.doc.family_members_destination_attachment.forEach((el) => {
                                if(htmlrow.parent_name1 == el.name){
                                    frappe.model.set_value(el.doctype, el.name, 'next_remainder_or_expiry_on', htmlrow.next_remainder_or_expiry_on)
                                }
                                
                            });
                        }
                    },
                    {
                        fieldtype: 'Small Text',
                        fieldname: 'description',
                        label: __('Description'),
                        in_list_view: 1,
                        columns:2,
                        onchange: function(event) {
                            let table = event.target.closest('[data-fieldtype="Table"]').getAttribute('data-fieldname');
                            let index = parseInt(event.target.closest('.grid-row').getAttribute('data-idx'))-1
                            let htmlrow = form_destination_details[table].get_field(table).get_value()[index]
                            frm.doc.family_members_destination_attachment.forEach((el) => {
                                if(htmlrow.parent_name1 == el.name){
                                    frappe.model.set_value(el.doctype, el.name, 'description', event.target.value)
                                }
                            });
                        }
                    },
                    {
                        fieldtype: 'Read Only',
                        fieldname: 'parent_name1',
                        label: __('Parent Name'),
                        hidden:1
                    },
                ]
    
    
                p.push({
                    fieldtype: 'Section Break',
                    fieldname:keys[i],
                    label:keys[i],
                    collapsible:1
                })
               
                if(file_table[keys[i]].length != 0){
                    p.push({
                        fieldname: 'table'+keys[i],
                        fieldtype: 'Table',
                        label: keys[i]+" Basic Attachment Table",
                        cannot_add_rows: true,
                        in_editable_grid: true,
                        cannot_delete_rows:true,
                        fields: fields,
                        data: file_table[keys[i]]
                    })
                }
                p.push({
                    fieldtype: 'HTML',
                    fieldname: keys[i]+'_destination_html',
                })
                
            }
            
            let attr_html = frm.$wrapper.find('div[data-fieldname="family_member_html"]')[0]
            attr_html.innerHTML=''
            form = new frappe.ui.FieldGroup({
                fields: p,
                body: attr_html
            });
            form.make()
            for(let i=0;i<frm.doc.destination_check_list.length;i++){
                
                check_list[frm.doc.destination_check_list[i].members_name ].push(
                    {
                        fieldtype: 'Check',
                        fieldname:frm.doc.destination_check_list[i].members_name+frm.doc.destination_check_list[i].check_list_name,
                        label:frm.doc.destination_check_list[i].check_list_name,
                        default:frm.doc.destination_check_list[i].check,
                        onchange: function(event) {
                            let row = frm.doc.destination_check_list[i]
                            frappe.model.set_value(row.doctype, row.name, 'check', event.target.checked)
                        }
                    }
                )
            }
            for(let user=0;user<keys.length;user++){
                let desti = []
                
                desti.push({
                    fieldtype: 'Section Break',
                    fieldname:keys[user],
                    label:keys[user]+" Destination Check List",
                })
                for(let j=0;j<check_list[keys[user]].length;j++){
                    desti.push(check_list[keys[user]][j])
                }
                if(desti_attach_table[keys[user]].length != 0){
                    desti.push({
                        fieldname: 'destination_table'+keys[user],
                        fieldtype: 'Table',
                        label: keys[user]+" Destination Attachment Table",
                        cannot_add_rows: true,
                        cannot_delete_rows:true,
                        in_editable_grid: true,
                        fields: desti_table_field,
                        data: desti_attach_table[keys[user]]
                    })
                }
                
                let desti_html = form.get_field(`${keys[user]}_destination_html`).wrapper
                desti_html.innerHTML=''
                form_destination = new frappe.ui.FieldGroup({
                    fields: desti,
                    body: desti_html
                });
                form_destination_details['destination_table'+keys[user]]=form_destination
                console.log(form_destination_details)
                form_destination.make()
            }
        }
        
    },
    onload:function (frm) {
        setTimeout(() => {
            $("[data-doctype='Expense Claim']").hide();
        }, 10);
        add_destination_details(frm)
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
        for(let i=0;i<frm.doc.multi_customer.length;i++){
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
                }
            })
        }
        frappe.call({
            method: "juzgo.juzgo.custom.py.project.remove_function",
            args:{
                table_field :frm.doc.family_members_destination_attachment,
                custom_list : custom_list
            },
            callback: function(r) {
                frm.set_value('family_members_destination_attachment',r.message)
                refresh_field("family_members_destination_attachment");
            }
        }) 
        frappe.call({
            method: "juzgo.juzgo.custom.py.project.remove_function",
            args:{
                table_field :frm.doc.destination_check_list,
                custom_list : custom_list
            },
            callback: function(r) {
                frm.set_value('destination_check_list',r.message)
                refresh_field("destination_check_list");
            }
        })
        // frm.save()
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
        for(let i=0;i<frm.doc.destination.length;i++){
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

frappe.ui.form.on('Customer Destination Check List', {
    check:function (frm,cdt,cdn) {
        let row = locals[cdt][cdn]
        let c = 1
        if(row.check == 1){
            if (frm.doc.family_members_destination_attachment.length == 0){
                c = 0
            }
            for(let i=0; i<frm.doc.family_members_destination_attachment.length; i++){
                if((frm.doc.family_members_destination_attachment[i].family_members_documents_name == row.family_member_details_name)&&(frm.doc.family_members_destination_attachment[i].file_type == row.check_list_name) ){
                    c = 1
                    break
                }else{
                    c =0
                }
            }
        } else {
            for(let i=0; i<frm.doc.family_members_destination_attachment.length; i++){
                if((frm.doc.family_members_destination_attachment[i].family_members_documents_name == row.family_member_details_name)&&(frm.doc.family_members_destination_attachment[i].file_type == row.check_list_name) ){
                    frm.doc.family_members_destination_attachment.splice(i, 1);
                    refresh_field("family_members_destination_attachment");
                    frm.save()
                }
            }
        }
        if(c == 0){
            let child = cur_frm.add_child("family_members_destination_attachment")
            frappe.model.set_value(child.doctype, child.name, "file_type", row.check_list_name)
            frappe.model.set_value(child.doctype, child.name, "members_name", row.members_name)
            frappe.model.set_value(child.doctype, child.name, "family_members_documents_name", row.family_member_details_name)
            frappe.model.set_value(child.doctype, child.name, "customer_id", row.customer_id)
            frappe.model.set_value(child.doctype, child.name, "destination", row.destination)
            refresh_field("family_members_destination_attachment");
            frm.save()
        }

    }
})