var form
var form_destination_details = {}
var form_destination
var remainder_group
var remainder_group_details = {}
frappe.ui.form.on('Project', {
    refresh:function (frm,cdt,cdn) {
        if(!frm.is_new()){
            check_list(frm)
            frappe.call({
                method:'juzgo.juzgo.custom.py.project.family_member_details_seprate',
                args:{
                    table:frm.doc.family_member_details,
                },
                callback(r1){
                frm.set_df_property("family_member_details_html","options",r1.message)
                }
            })
        }
        frm.set_query("task_name","attachments", function () {
            return {
                filters: {
                    project: frm.doc.name,
                    assigned_to: frappe.session.user
                },
            };
        });
    },
    phone_number:function(frm){
        if(frm.doc.phone_number){
            var phoneno = /^\d{10,12}$/;
            if(!frm.doc.phone_number.match(phoneno)){
                frm.set_df_property("phone_number",'description',"<b style='color:red'>"+frm.doc.phone_number.length+"</b> no. Entered."+"<span style='color:red'>Enter Correct Phone No.</span>")
            }
            else{
                frm.set_df_property("phone_number",'description',"")
                if(frm.doc.phone_number.length > 10){
                    frm.set_df_property("phone_number",'description',"<b style='color:Orange'>"+frm.doc.phone_number.length+"</b> no. Entered.")
                }
            }
        }
    },
    update_data:function (frm) {
        multi_customer(frm)
        frm.save()
    },
    onload:function (frm) {
        setTimeout(() => {
            $("[data-doctype='Expense Claim']").hide();
            $("[data-doctype='Material Request']").hide();
            $("[data-doctype='BOM']").hide();
            $("[data-doctype='Stock Entry']").hide();
            $("[data-doctype='Sales Order']").hide();
            $("[data-doctype='Delivery Note']").hide();
            $("[data-doctype='Purchase Order']").hide();
            $("[data-doctype='Purchase Receipt']").hide();
            $("[data-doctype='Project Update']").hide();
            $("[data-doclabel='Material']").hide();
            $("[data-doclabel='Claims']").hide();
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
        if (frm.doc.project_name.length >= 3){
            frappe.call({
                method: "juzgo.juzgo.custom.py.project.project_exist_list",
                args: {
                    "project_name": frm.doc.project_name
                },
                callback: function (r) {
                    if (r && r.message) {
                        frm.set_df_property(
                            "project_name",
                            "description",
                            ('This Project Name already exists: {0}', [r.message.map(function (d) {
                                return repl('<a href="/app/project/%(name)s">%(or_name)s</a>', { name: d['name'], or_name: d['project_name'] })
                            }).join(', ')]));
                    }
                },
            })
        } else {
            frm.set_df_property(
                "project_name",
                "description",
                "");
        }
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
        multi_customer(frm)
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

function add_destination_details(frm,event=''){
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
                        frappe.model.set_value(child.doctype, child.name, "receive_or_send", row.receive_or_send)
                    });
                    refresh_field("destination_check_list");
                    // frm.save()
                }
            }
        })
        check_list(frm)
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
                if((frm.doc.family_members_destination_attachment[i].family_members_documents_name == row.family_member_details_name)&&(frm.doc.family_members_destination_attachment[i].file_type == row.check_list_name) &&(frm.doc.family_members_destination_attachment[i].destination == row.destination) ){
                    c = 1
                    break
                }else{
                    c =0
                }
            }
        } else {
            for(let i=0; i<frm.doc.family_members_destination_attachment.length; i++){
                if((frm.doc.family_members_destination_attachment[i].family_members_documents_name == row.family_member_details_name)&&(frm.doc.family_members_destination_attachment[i].file_type == row.check_list_name) &&(frm.doc.family_members_destination_attachment[i].destination == row.destination)){
                    frm.doc.family_members_destination_attachment.splice(i, 1);
                    refresh_field("family_members_destination_attachment");
                    check_list(frm)
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
            frappe.model.set_value(child.doctype, child.name, "receive_or_send", row.receive_or_send)
            refresh_field("family_members_destination_attachment");
            check_list(frm)
        }

    }
})

function multi_customer(frm,event=''){
    if(frm.is_new()){
        frappe.throw("First Kindly Save This Project.")
    }
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
                    r.message[0].forEach(row => {
                        let child = cur_frm.add_child("family_members_attachment")
                        frappe.model.set_value(child.doctype, child.name, "members_name", row.members_name)
                        frappe.model.set_value(child.doctype, child.name, "file_type", row.file_type)
                        frappe.model.set_value(child.doctype, child.name, "file", row.file)
                        frappe.model.set_value(child.doctype, child.name, "next_remainder_or_expiry_on", row.next_remainder_or_expiry_on)
                        frappe.model.set_value(child.doctype, child.name, "description", row.description)
                        frappe.model.set_value(child.doctype, child.name, "attached_by", row.attached_by)
                        frappe.model.set_value(child.doctype, child.name, "family_members_documents_name", row.family_members_documents_name)
                        frappe.model.set_value(child.doctype, child.name, "customer_id", row.customer_id)
                        frappe.model.set_value(child.doctype, child.name, "receive_or_send", row.receive_or_send)
                    });
                    refresh_field("family_members_attachment");
                    frm.doc.project_members_check_list = []
                    r.message[1].forEach(row => {
                        let child = cur_frm.add_child("project_members_check_list")
                        frappe.model.set_value(child.doctype, child.name, "members_name", row.members_name)
                        frappe.model.set_value(child.doctype, child.name, "check_list_name", row.check_list_name)
                        frappe.model.set_value(child.doctype, child.name, "check", row.check)
                        frappe.model.set_value(child.doctype, child.name, "receive_or_send", row.receive_or_send)
                        frappe.model.set_value(child.doctype, child.name, "file", row.file)
                        frappe.model.set_value(child.doctype, child.name, "next_remainder_or_expiry_on", row.next_remainder_or_expiry_on)
                        frappe.model.set_value(child.doctype, child.name, "description", row.description)
                    });
                    refresh_field("project_members_check_list");
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
        add_destination_details(frm,event)
}

function check_list(frm){
    let attr_html = frm.$wrapper.find('div[data-fieldname="family_member_html"]')[0]
    attr_html.innerHTML=''
    let remainder_html = frm.$wrapper.find('div[data-fieldname="check_list_remainder_html"]')[0]
    remainder_html.innerHTML=''
    if(frm.doc.project_members_check_list.length > 0){
        let check=[
            {
                fieldtype: 'Data',
                fieldname: 'check_list_name',
                label: __('Check List Name'),
                in_list_view: 1,
                read_only:1,
                columns:2,
            }, 
            {
                fieldtype: 'Check',
                fieldname: 'check',
                label: __('Check'),
                in_list_view: 1,
                read_only:1,
                columns:1,
            },
            {
                fieldtype: 'Attach',
                fieldname: 'file',
                label: __('File'),
                read_only:1,
                in_list_view: 1,
                columns:2,
            },
            {
                fieldtype: 'Date',
                fieldname: 'next_remainder_or_expiry_on',
                label: __('Next remainder or expiry on'),
                in_list_view: 1,
                columns:2,
                read_only:1,
            },
            {
                fieldtype: 'Small Text',
                fieldname: 'description',
                label: __('Description'),
                in_list_view: 1,
                columns:2,
                read_only:1,
            },
            {
                fieldtype: 'Data',
                fieldname: 'receive_or_send',
                label: __('Receive Or Send'),
                in_list_view: 1,
                read_only:1,
                columns:1,
            },
        ]

        let for_label = {}
        let check_list = {}
        let check_table ={}
        let remainder_data = {}
        let desti_attach_table ={}
        for(let i=0;i<frm.doc.family_member_details.length;i++){
            check_list[frm.doc.family_member_details[i].members_name]=[]
            check_table[frm.doc.family_member_details[i].members_name]=[]
            desti_attach_table[frm.doc.family_member_details[i].members_name]=[]
            for_label[frm.doc.family_member_details[i].members_name] = frm.doc.family_member_details[i].customer_id
            remainder_data[frm.doc.family_member_details[i].customer_id]=[]
        }
        for(let i=0;i<frm.doc.project_members_check_list.length;i++){ 
            if(check_table[frm.doc.project_members_check_list[i].members_name]){
                check_table[frm.doc.project_members_check_list[i].members_name ].push(
                    {
                        members_name:frm.doc.project_members_check_list[i].members_name,
                        check_list_name:frm.doc.project_members_check_list[i].check_list_name,
                        check:frm.doc.project_members_check_list[i].check,
                        receive_or_send:frm.doc.project_members_check_list[i].receive_or_send,
                        file:frm.doc.project_members_check_list[i].file,
                        next_remainder_or_expiry_on:frm.doc.project_members_check_list[i].next_remainder_or_expiry_on,
                        description:frm.doc.project_members_check_list[i].description,
                    }
                )
            }
        }
        for(let i=0;i<frm.doc.family_members_destination_attachment.length;i++){  
            if(desti_attach_table[frm.doc.family_members_destination_attachment[i].members_name]){
                desti_attach_table[frm.doc.family_members_destination_attachment[i].members_name ].push(
                    {
                        members_name:frm.doc.family_members_destination_attachment[i].members_name,
                        file_type:frm.doc.family_members_destination_attachment[i].file_type,
                        file:frm.doc.family_members_destination_attachment[i].file,
                        next_remainder_or_expiry_on:frm.doc.family_members_destination_attachment[i].next_remainder_or_expiry_on,
                        description:frm.doc.family_members_destination_attachment[i].description,
                        parent_name1:frm.doc.family_members_destination_attachment[i].name,
                        checkfile:frm.doc.family_members_destination_attachment[i].file?1:0,
                        receive_or_send:frm.doc.family_members_destination_attachment[i].receive_or_send,
                        customer_id:frm.doc.family_members_destination_attachment[i].customer_id,
                    }
                )
            }
        }
        let p=[]
        let keys=Object.keys(check_table);
        for(let i=0;i<keys.length;i++){
            var desti_table_field=[
                {
                    fieldtype: 'Read Only',
                    fieldname: 'members_name',
                    read_only:1,
                    label: __('Members Name'),
                }, 
                {
                    fieldtype: 'Read Only',
                    fieldname: 'file_type',
                    label: __('File Type'),
                    in_list_view: 1,
                    read_only:1,
                    columns:2
                },
                {
                    fieldtype: 'Attach',
                    fieldname: 'file',
                    label: __('File'),
                    in_list_view: 1,
                    reqd:1,
                    columns:2,
                },
                {
                    fieldtype: 'Check',
                    fieldname: 'checkfile',
                    label: __('Attached'),
                    in_list_view: 1,
                    reqd:1,
                    columns:1,

                    onchange: function(event) {
                        let table = event.target.closest('[data-fieldtype="Table"]').getAttribute('data-fieldname');
                        let index = parseInt(event.target.closest('.grid-row').getAttribute('data-idx'))-1
                        let htmlrow = form_destination_details[table].get_field(table).get_value()[index]
                        frm.doc.family_members_destination_attachment.forEach((el) => {
                            if(htmlrow.parent_name1 == el.name){
                                frappe.model.set_value(el.doctype, el.name, 'attached_by', frappe.session.user)
                                frappe.model.set_value(el.doctype, el.name, 'file', htmlrow.file)
                                frm.save().then(()=>{
                                    frm.reload_doc()
                                })
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
                    fieldtype: 'Data',
                    fieldname: 'receive_or_send',
                    label: __('Receive Or Send'),
                    in_list_view: 1,
                    columns:1,
                    read_only:1,
                },
                {
                    fieldtype: 'Read Only',
                    fieldname: 'parent_name1',
                    label: __('Parent Name'),
                    hidden:1,
                    read_only:1,
                },
            ]


            p.push({
                fieldtype: 'Section Break',
                fieldname:keys[i],
                label: '<a href="/app/customer/'+for_label[keys[i]]+'" target="_blank" style="color:#003300">'+for_label[keys[i]]+'</a>' +' - '+keys[i],
                collapsible:1
            })
            if(check_table[keys[i]].length != 0){
                p.push({
                    fieldname: 'table'+keys[i]+'check',
                    fieldtype: 'Table',
                    label: '<a href="/app/customer/'+for_label[keys[i]]+'" target="_blank" style="color:#003300">'+for_label[keys[i]]+'</a>'+" - "+'<span style="color:#000033">'+keys[i]+" Customer Check List and Attachment </span>",
                    cannot_add_rows: true,
                    in_editable_grid: true,
                    cannot_delete_rows:true,
                    fields: check,
                    data: check_table[keys[i]]
                })
            }
            p.push({
                fieldtype: 'HTML',
                fieldname: keys[i]+'_destination_html',
            })
            
        }
        form = new frappe.ui.FieldGroup({
            fields: p,
            body: attr_html
        });
        form.make()
        for(let resend=0;resend<2;resend++){
            for(let i=0;i<frm.doc.destination_check_list.length;i++){
                if(resend == 0){
                    if(frm.doc.destination_check_list[i].receive_or_send=="To Receive"){
                        if(check_list[frm.doc.destination_check_list[i].members_name]){
                            check_list[frm.doc.destination_check_list[i].members_name].push(
                                {
                                    fieldtype: 'Check',
                                    fieldname:frm.doc.destination_check_list[i].members_name+frm.doc.destination_check_list[i].check_list_name,
                                    label:(frm.doc.destination_check_list[i].check_list_name)+(frm.doc.destination_check_list[i].receive_or_send=="To Send"?"(s)":frm.doc.destination_check_list[i].receive_or_send=="To Receive"?"(R)":""),
                                    default:frm.doc.destination_check_list[i].check,
                                    onchange: function(event) {
                                        let row = frm.doc.destination_check_list[i]
                                        frappe.model.set_value(row.doctype, row.name, 'check', event.target.checked)
                                    }
                                }
                            )
                        }
                    }
                } else {
                    if(frm.doc.destination_check_list[i].receive_or_send=="To Send"){
                        if(check_list[frm.doc.destination_check_list[i].members_name]){
                            check_list[frm.doc.destination_check_list[i].members_name].push(
                                {
                                    fieldtype: 'Check',
                                    fieldname:frm.doc.destination_check_list[i].members_name+frm.doc.destination_check_list[i].check_list_name,
                                    label:(frm.doc.destination_check_list[i].check_list_name)+(frm.doc.destination_check_list[i].receive_or_send=="To Send"?"(s)":frm.doc.destination_check_list[i].receive_or_send=="To Receive"?"(R)":""),
                                    default:frm.doc.destination_check_list[i].check,
                                    onchange: function(event) {
                                        let row = frm.doc.destination_check_list[i]
                                        frappe.model.set_value(row.doctype, row.name, 'check', event.target.checked)
                                    }
                                }
                            )
                        }
                    }
                }
            }
        }

        for(let user=0;user<keys.length;user++){
            let desti = []
            let checkboxFields = []
            let check_len = check_list[keys[user]].length/4
            for(let j=0;j<check_list[keys[user]].length;j++){
                checkboxFields.push(check_list[keys[user]][j])
                if(((j+1) % Math.ceil(check_len)) == 0){
                    if(j+1 != check_list[keys[user]].length)
                        checkboxFields.push({
                            fieldtype: 'Column Break',
                            fieldname:'cb_'+keys[user]+j,
                        })
                }
            }
            desti.push({
                fieldtype: 'Section Break',
                fieldname:keys[user],
                label:'<span style="font-weight: normal;"><a href="/app/customer/'+for_label[keys[user]]+'" target="_blank" style="color:#003300">'+for_label[keys[user]]+'</a>'+'</span> - <span style="color:#330000">'+keys[user]+' Destination Check List </span> </span>',
            })
            desti.push({
                fieldtype: 'HTML',
                fieldname:`${keys[user]}_checkbox_html`,
                label:keys[user],
            })
            if(desti_attach_table[keys[user]].length != 0){
                desti.push({
                    fieldname: 'destination_table'+keys[user],
                    fieldtype: 'Table',
                    label: '<a href="/app/customer/'+for_label[keys[user]]+'" target="_blank" style="color:#003300">'+for_label[keys[user]]+'</a>'+"</span> - <span style='color:#000033'>"+keys[user]+" Destination Attachment Table </span>",
                    cannot_add_rows: true,
                    read_only:1,
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
            form_destination.make()
            new frappe.ui.FieldGroup({
                fields: checkboxFields,
                body: form_destination.get_field(`${keys[user]}_checkbox_html`).wrapper
            }).make();
        }
        let remainder_field = [
            {
                fieldtype: 'Data',
                fieldname: 'member_name',
                label: __('Member Name'),
                in_list_view: 1,
                read_only:1,
                columns:2,
            }, 
            {
                fieldtype: 'Data',
                fieldname: 'check_list',
                label: __('Check List'),
                in_list_view: 1,
                read_only:1,
                columns:2,
            },
            {
                fieldtype: 'Date',
                fieldname: 'next_remainder_on',
                label: __('Next Remainder On'),
                in_list_view: 1,
                columns:1,
                onchange: function(event) {
                    let table = event.target.closest('[data-fieldtype="Table"]').getAttribute('data-fieldname');
                    let index = parseInt(event.target.closest('.grid-row').getAttribute('data-idx'))-1
                    let htmlrow = remainder_group_details[table].get_field(table).get_value()[index]
                    frm.doc.check_list_remainder_table.forEach((el) => {
                        if(htmlrow.parent_name1 == el.name){
                            frappe.model.set_value(el.doctype, el.name, 'next_remainder_on', htmlrow.next_remainder_on)
                        }
                        
                    });
                }
            },
            
            {
                fieldtype: 'Link',
                fieldname: 'user',
                label: __('User'),
                options : 'User',
                in_list_view: 1,
                columns:2,
            },
            {
                fieldtype: 'Long Text',
                fieldname: 'notes',
                label: __('Notes'),
                in_list_view: 1,
                columns:2,
                onchange: function(event) {
                    let table = event.target.closest('[data-fieldtype="Table"]').getAttribute('data-fieldname');
                    let index = parseInt(event.target.closest('.grid-row').getAttribute('data-idx'))-1
                    let htmlrow = remainder_group_details[table].get_field(table).get_value()[index]
                    frm.doc.check_list_remainder_table.forEach((el) => {
                        if(htmlrow.parent_name1 == el.name){
                            frappe.model.set_value(el.doctype, el.name, 'notes', event.target.value)
                            frappe.model.set_value(el.doctype, el.name, 'user', htmlrow.user)
                        }
                    });
                }
            },
            {
                fieldtype: 'Check',
                fieldname: 'update',
                label: __('Update'),
                in_list_view: 1,
                columns:1,
                onchange: function(event) {
                    let table = event.target.closest('[data-fieldtype="Table"]').getAttribute('data-fieldname');
                    let index = parseInt(event.target.closest('.grid-row').getAttribute('data-idx'))-1
                    let htmlrow = remainder_group_details[table].get_field(table).get_value()[index]
                    frm.doc.check_list_remainder_table.forEach((el) => {
                        if(htmlrow.parent_name1 == el.name){
                            frappe.model.set_value(el.doctype, el.name, 'user', htmlrow.user)
                            frm.save()
                        }
                    });
                }
            },
            {
                fieldtype: 'Data',
                fieldname: 'parent_name1',
                label: __('Parent Name'),
                hidden:1,
                read_only:1,
            },
        ]
        for(let i=0;i<frm.doc.check_list_remainder_table.length;i++){ 
            if(remainder_data[frm.doc.check_list_remainder_table[i].customer_id]){
                remainder_data[frm.doc.check_list_remainder_table[i].customer_id ].push(
                    {
                        member_name:frm.doc.check_list_remainder_table[i].member_name,
                        check_list:frm.doc.check_list_remainder_table[i].check_list,
                        next_remainder_on:frm.doc.check_list_remainder_table[i].next_remainder_on,
                        notes:frm.doc.check_list_remainder_table[i].notes,
                        user:frm.doc.check_list_remainder_table[i].user,
                        parent_name1:frm.doc.check_list_remainder_table[i].name,
                    }
                )
            }
        }
        let key=Object.keys(remainder_data);
        let remainder_fields = []
        for(let i=0;i<key.length;i++){
            remainder_fields.push({
                fieldtype: 'Section Break',
                fieldname:key[i]+"_remainder",
                label: key[i],
                collapsible:1
            })
            if(remainder_data[key[i]].length != 0){
                remainder_fields.push({
                    fieldname: 'remainder_table'+key[i],
                    fieldtype: 'Table',
                    label: 'Check List Remainder',
                    cannot_add_rows: true,
                    in_editable_grid: true,
                    cannot_delete_rows:true,
                    fields: remainder_field,
                    data: remainder_data[key[i]]
                })
            }
            remainder_html.innerHTML=''
            remainder_group = new frappe.ui.FieldGroup({
                fields: remainder_fields,
                body: remainder_html
            })
            remainder_group.make();
            remainder_group_details['remainder_table'+key[i]]=remainder_group
        }
        
    }
}

frappe.ui.form.on('Task Attachments', {
    file:function (frm,cdt,cdn) {
        let row = locals[cdt][cdn]
        console.log(row.file)
        var currentdate = new Date(); 
        frappe.db.get_value('File', {"file_url":row.file}, 'name').then((data)=>{
            frappe.model.set_value(row.doctype,row.name,"ref_id",data.message.name)
            frappe.model.set_value(row.doctype,row.name,"attached_by",frappe.session.user)
            frappe.model.set_value(row.doctype,row.name,"attached_date",frappe.datetime.get_today())
            frappe.model.set_value(row.doctype,row.name,"attached_time",currentdate.getHours() + ":" + currentdate.getMinutes() + ":" + currentdate.getSeconds())
        })
    }
})