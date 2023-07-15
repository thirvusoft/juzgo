frappe.ui.form.on('Task', {
    subject:function(frm){
        if (frm.doc.subject.length >= 3){
            frappe.call({
                method: "juzgo.juzgo.custom.py.task.task_exist_list",
                args: {
                    "subject": frm.doc.subject
                },
                callback: function (r) {
                    if (r && r.message) {
                        frm.set_df_property(
                            "subject",
                            "description",
                            ('This Task Name already exists: {0}', [r.message.map(function (d) {
                                return repl('<a href="/app/task/%(name)s">%(or_name)s</a>', { name: d['name'], or_name: d['subject'] })
                            }).join(', ')]));
                    }
                },
            })
        } else {
            frm.set_df_property(
                "subject",
                "description",
                "");
        }
    },
    onload:function (frm) {
        setTimeout(() => {
            $("[data-doctype='Expense Claim']").hide();
        }, 10);
        frm.refresh_field('depends_on')
    },
    project: function(frm){
        filter(frm)
    },
    refresh: function(frm,cdt,cdn){
        filter(frm)
        // let quality_inspection_field = frm.fields_dict.depends_on.grid.get_docfield("task")
        // quality_inspection_field.get_route_options_for_new_doc = function(row) {
        //     return  {
        //         "project": row.frm.doc.project,
        //         "subject": row.frm.doc.subject,
        //         "assigned_to": row.frm.doc.assigned_to,
        //         "exp_start_date":row.frm.doc.exp_start_date,
        //         "department":row.frm.doc.department,

        //     };
        // };
        if(!frappe.user.has_role('System Manager') && !frappe.user.has_role('Thirvu Admin') && !frappe.user.has_role('Juzgo Admin') ){
            if(frm.doc.owner != frappe.session.user){
                for(let i=0;i<frm.fields.length;i++){
                    if((frm.fields[i].df.fieldname == "sb_details") || (frm.fields[i].df.fieldname == "notes") || (frm.fields[i].df.fieldname == "completed_by") || (frm.fields[i].df.fieldname == "completed_on") || (frm.fields[i].df.fieldname == "status")){
                        
                    } else {
                        frm.set_df_property(frm.fields[i].df.fieldname,"read_only",1)
                    }
                }
            }
        }
        
        frappe.call({
            
            method: "juzgo.juzgo.custom.py.task.juzgo_admin_users",
            args:{
            },
            callback: function(r) {
                frm.set_query("user","task_approval", function () {
                    return {
                        filters: {
                            name: ["in",r.message],
                        },
                    };
                });

        }
        }) 
        // if(frappe.user.has_role('Juzgo Admin') ){
        //     let rows = locals[cdt][cdn]
        //     frm.set_df_property("task", "read_only", 0, rows.name, 'depends_on');
        //     frm.refresh_field('depends_on');
        // }

    },
    assigned_to: function(frm){
        if(!frm.doc.project){
            frappe.msgprint("Kindly Select Project.")
            frm.set_value("assigned_to","")
        }
    },
    status: function(frm){
        frm.refresh()
    },
    expected_min: function(frm){
         frappe.call({
            
            method: "juzgo.juzgo.custom.py.task.minutes_to_hours",
            args:{
                minutes:frm.doc.expected_min,
            },
            callback: function(r) {
				frm.set_value("expected_time",r.message)
				

        }
        })       
    },
    expected_time: function(frm){
        frappe.call({
           
           method: "juzgo.juzgo.custom.py.task.hours_to_minutes",
           args:{
                hours:frm.doc.expected_time,
           },
           callback: function(r) {
               frm.set_value("expected_min",r.message)
               

       }
       })       
   },
})

async function filter(frm){
    var list = []
        if(frm.doc.project){
            var d = await frappe.db
            .get_list("ToDo", {
                filters: { reference_type: "Project", reference_name: frm.doc.project},
                fields: ["allocated_to"],
            })
            .then((l) => {
                for(var i=0;i<l.length;i++){
                    list.push(l[i].allocated_to)
                }
            })
        }
        frm.set_query("assigned_to", function () {
			return {
				filters: {
					name: ["in",list],
				},
			};
		});
        frm.set_query("task_lead", function () {
			return {
				filters: {
					name: ["in",list],
				},
			};
		});
        frm.set_query("assigned_to","depends_on", function () {
			return {
				filters: {
					name: ["in",list],
				},
			};
		});
}

frappe.ui.form.on('Task Depends On', {
	task: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		
        frappe.call({
			method:"juzgo.juzgo.custom.py.task.getdesc",
			args:{
				'task':row.task
			},
			callback:function(r){
				if(r.message){
					frappe.model.set_value(row.doctype,row.name,"subject",r.message[0])
					// frappe.model.set_value(row.doctype,row.name,"notes",r.message[1])
					frm.refresh_field('depends_on')
                    frm.save()
				}
			}
		})
	},
    subject: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		update_data(row)
	},
    subject1: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		update_data(row)
	},
    assigned_to: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		update_data(row)
	},
    expected_min: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		update_data(row)
	},
    depends_on_add: function(frm,cdt,cdn){
        frappe.model.set_value(cdt,cdn,"assigned_to",frm.doc.assigned_to)
        frappe.model.set_value(cdt,cdn,"expected_min",frm.doc.expected_min)
    }
})

function update_data(row){
    frappe.call({
        method:"juzgo.juzgo.custom.py.task.update_data",
        args:{
            'subject':row.subject,
            'subject1':row.subject1,
            'task':row.task,
            'assigned_to':row.assigned_to,
            'expected_min':row.expected_min
        }
    })
}

frappe.ui.form.on('Task Approval', {
	status: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        frm.call({
            method: "juzgo.juzgo.custom.py.task.status_approval",
            args: {
                name: frm.doc.name,
                task_approval:row
            },
            callback: function (r) {
                console.log(r.message)
                if(frappe.session.user != row.user){
                    frappe.model.set_value(cdt, cdn, "status", r.message)
                    frappe.throw("You are not allow to update others status")
                    
                } 
            }
        })  
	},
})