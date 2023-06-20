var form
frappe.ui.form.on('Customer', {
    refresh:function (frm,cdt,cdn) {
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
                    frm.doc.family_members_table.forEach((el) => {
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
                    frm.doc.family_members_table.forEach((el) => {
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
                    frm.doc.family_members_table.forEach((el) => {
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
            },
        ]
        let user = {}
        let file_table ={}
        for(let i=0;i<frm.doc.family_members_details.length;i++){
            user[frm.doc.family_members_details[i].members_name]=[]
            file_table[frm.doc.family_members_details[i].members_name]=[]
        }
        for(let i=0;i<frm.doc.family_members_documents.length;i++){
            
            user[frm.doc.family_members_documents[i].members_name ].push(
                {
                    fieldtype: 'Check',
                    fieldname:frm.doc.family_members_documents[i].members_name+frm.doc.family_members_documents[i].check_list_name,
                    label:frm.doc.family_members_documents[i].check_list_name,
                    default:frm.doc.family_members_documents[i].check,
                    onchange: function(event) {
                        let row = frm.doc.family_members_documents[i]
                        frappe.model.set_value(row.doctype, row.name, 'check', event.target.checked)
                    }
                }
            )
        }
        for(let i=0;i<frm.doc.family_members_table.length;i++){
            file_table[frm.doc.family_members_table[i].members_name ].push(
                {
                    members_name:frm.doc.family_members_table[i].members_name,
                    file_type:frm.doc.family_members_table[i].file_type,
                    file:frm.doc.family_members_table[i].file,
                    next_remainder_or_expiry_on:frm.doc.family_members_table[i].next_remainder_or_expiry_on,
                    description:frm.doc.family_members_table[i].description,
                    parent_name1:frm.doc.family_members_table[i].name,
                    checkfile:frm.doc.family_members_table[i].file?1:0
                }
            )
        }
        let p=[]
        let keys=Object.keys(user);
        let checkboxFields = {}, _checkboxFields = {}
        for(let i=0;i<keys.length;i++){
            _checkboxFields[keys[i]] = []
            checkboxFields[keys[i]] = []
            p.push({
                fieldtype: 'Section Break',
                fieldname:keys[i],
                label:keys[i],
                collapsible:1
            })
            for(let j=0;j<user[keys[i]].length;j++){
                p.push(user[keys[i]][j])
            }
            // p.push({
            //     fieldtype: 'HTML',
            //     fieldname:`${keys[i]}_checkbox_html`,
            //     label:keys[i],
            // })
            // for(let j=0;j<user[keys[i]].length;j++){
            //     _checkboxFields[keys[i]].push(user[keys[i]][j])
            // }
            // console.log(Math.round(_checkboxFields[keys[i]].length/4))

            // let checkfields = [[], [], [], []]
            // for(let j=0; j<_checkboxFields[keys[i]].length;j++) {
            //     checkfields[j%(checkfields.length)].push(_checkboxFields[keys[i]][j])

               
            // }
            // console.log(checkfields)
            // for (let j = 0; j<checkfields.length;j++) {
            //     if (checkfields[j]) {
            //         console.log(true, checkboxFields[keys[i]],  checkboxFields[keys[i]].length, checkfields[j].length)
            //         checkboxFields[keys[i]].concat(checkfields[j]);
            //         console.log(true, checkboxFields[keys[i]].length, checkfields[j].length)
            //         if (checkfields[j+1]) {
            //             checkboxFields[keys[i]].push({
            //                 fieldtype: 'Column Break'
            //             })
            //         }
            //     }
            //     console.log(checkboxFields[keys[i]])

            // }
        
            if(file_table[keys[i]].length != 0){
                p.push({
                    fieldname: 'table'+keys[i],
                    fieldtype: 'Table',
                    label: keys[i]+" Attachment Table",
                    cannot_add_rows: true,
                    in_editable_grid: true,
                    cannot_delete_rows:true,
                    fields: fields,
                    data: file_table[keys[i]]
                })
            }
            
        }
        let attr_html = frm.$wrapper.find('div[data-fieldname="family_member_html"]')[0]
        attr_html.innerHTML=''
        form = new frappe.ui.FieldGroup({
            fields: p,
            body: attr_html
        });
        form.make()

        // for(let i=0;i<keys.length;i++){
        //     new frappe.ui.FieldGroup({
        //         fields: checkboxFields[keys[i]],
        //         body: form.get_field(`${keys[i]}_checkbox_html`).wrapper
        //     }).make();
        // }
        // console.log(form)
    },
})

frappe.ui.form.on('Family Members Details', {
    date_of_birth:function (frm,cdt,cdn) {
        let row = locals[cdt][cdn]
        frappe.model.set_value(cdt,cdn,"age",new Date().getFullYear() - new Date(row.date_of_birth).getFullYear())
        create_id(frm,row)
    },
    age:function (frm,cdt,cdn) {
        let row = locals[cdt][cdn]
        if(row.member_row_id){
            add_member_details(frm,row)
        }
    },
    gender:function (frm,cdt,cdn) {
        let row = locals[cdt][cdn]
        if(row.member_row_id){
            add_member_details(frm,row)
        }
    },
    members_name:function (frm,cdt,cdn) {
        let row = locals[cdt][cdn]
        create_id(frm,row)

    },
    before_family_members_details_remove:function (frm,cdt,cdn) {
        let row = locals[cdt][cdn]
        frappe.call({
            method:'juzgo.juzgo.custom.py.customer.remove_list',
            args:{
                row:row,
                name:frm.doc.name
            },
            callback(r1){
                if(r1.message){
                    frm.doc.family_members_documents = []
                    let i = 0 
                    for (const d of r1.message[0]){
                        cur_frm.add_child("family_members_documents")
                        frappe.model.set_value(frm.doc.family_members_documents[i].doctype,frm.doc.family_members_documents[i].name,"members_name",d.members_name)
                        frappe.model.set_value(frm.doc.family_members_documents[i].doctype,frm.doc.family_members_documents[i].name,"age",d.age)
                        frappe.model.set_value(frm.doc.family_members_documents[i].doctype,frm.doc.family_members_documents[i].name,"gender",d.gender)
                        frappe.model.set_value(frm.doc.family_members_documents[i].doctype,frm.doc.family_members_documents[i].name,"check_list_name",d.check_list_name)
                        frappe.model.set_value(frm.doc.family_members_documents[i].doctype,frm.doc.family_members_documents[i].name,"family_member_details_name",d.family_member_details_name)
                        frappe.model.set_value(frm.doc.family_members_documents[i].doctype,frm.doc.family_members_documents[i].name,"check",d.check)
                        i++;
                    }
                    refresh_field("family_members_documents");
                    frm.doc.family_members_table = []
                    let j = 0 
                    for (const d of r1.message[1]){
                        cur_frm.add_child("family_members_tabel")
                        frappe.model.set_value(frm.doc.family_members_table[j].doctype,frm.doc.family_members_table[j].name,"members_name",d.members_name)
                        frappe.model.set_value(frm.doc.family_members_table[j].doctype,frm.doc.family_members_table[j].name,"file_type",d.file_type)
                        frappe.model.set_value(frm.doc.family_members_table[j].doctype,frm.doc.family_members_table[j].name,"file",d.file)
                        frappe.model.set_value(frm.doc.family_members_table[j].doctype,frm.doc.family_members_table[j].name,"next_remainder_or_expiry_on",d.next_remainder_or_expiry_on)
                        frappe.model.set_value(frm.doc.family_members_table[j].doctype,frm.doc.family_members_table[j].name,"family_members_documents_name",d.family_members_documents_name)
                        frappe.model.set_value(frm.doc.family_members_table[j].doctype,frm.doc.family_members_table[j].name,"description",d.description)
                        frappe.model.set_value(frm.doc.family_members_table[j].doctype,frm.doc.family_members_table[j].name,"attached_by",d.attached_by)
                        j++;
                    }
                    refresh_field("family_members_table");
                    frm.save()
                }
            }
        })
    },
})
function create_id(frm,row){
    if(row.age && row.date_of_birth){
        frappe.model.set_value(row.doctype,row.name,"member_row_id",row.members_name+row.date_of_birth )
    }
}
function add_member_details(frm,row){
    if(row.age && row.gender){
        frappe.call({
            method:'juzgo.juzgo.custom.py.customer.add_member_details',
            args:{
                row:row,
                name:frm.doc.name
            },
            callback(r1){
                if(r1.message){
                    frm.doc.family_members_documents = []
                    let i = 0 
                    for (const d of r1.message){
                        cur_frm.add_child("family_members_documents")
                        frappe.model.set_value(frm.doc.family_members_documents[i].doctype,frm.doc.family_members_documents[i].name,"members_name",d.members_name)
                        frappe.model.set_value(frm.doc.family_members_documents[i].doctype,frm.doc.family_members_documents[i].name,"age",d.age)
                        frappe.model.set_value(frm.doc.family_members_documents[i].doctype,frm.doc.family_members_documents[i].name,"gender",d.gender)
                        frappe.model.set_value(frm.doc.family_members_documents[i].doctype,frm.doc.family_members_documents[i].name,"check_list_name",d.check_list_name)
                        frappe.model.set_value(frm.doc.family_members_documents[i].doctype,frm.doc.family_members_documents[i].name,"family_member_details_name",d.family_member_details_name)
                        frappe.model.set_value(frm.doc.family_members_documents[i].doctype,frm.doc.family_members_documents[i].name,"check",d.check)
                        i++;
                    }
                    refresh_field("family_members_documents");
                    frm.save()
                }
            }
        })
    }
}

frappe.ui.form.on('Family members Table', {
    family_members_table_add:function (frm,cdt,cdn) {
        frappe.model.set_value(cdt,cdn,"attached_by",frappe.session.user)
    }
})
frappe.ui.form.on('Family Members Documents', {
    check:function (frm,cdt,cdn) {
        let row = locals[cdt][cdn]
        let c = 1
        if(row.check == 1){
            if (frm.doc.family_members_table.length == 0){
                c = 0
            }
            for(let i=0; i<frm.doc.family_members_table.length; i++){
                if((frm.doc.family_members_table[i].family_members_documents_name == row.family_member_details_name)&&(frm.doc.family_members_table[i].file_type == row.check_list_name) ){
                    c = 1
                    break
                }else{
                    c =0
                }
            }
        } else {
            for(let i=0; i<frm.doc.family_members_table.length; i++){
                if((frm.doc.family_members_table[i].family_members_documents_name == row.family_member_details_name)&&(frm.doc.family_members_table[i].file_type == row.check_list_name) ){
                    frm.doc.family_members_table.splice(i, 1);
                    refresh_field("family_members_table");
                    frm.save()
                }
            }
        }
        if(c == 0){
            let child = cur_frm.add_child("family_members_table")
            frappe.model.set_value(child.doctype, child.name, "file_type", row.check_list_name)
            frappe.model.set_value(child.doctype, child.name, "members_name", row.members_name)
            frappe.model.set_value(child.doctype, child.name, "family_members_documents_name", row.family_member_details_name)
            refresh_field("family_members_table");
            frm.save()
        }

    }
})