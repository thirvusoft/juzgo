frappe.ui.form.on('Task', {
    onload:function (frm) {
        setTimeout(() => {
            $("[data-doctype='Expense Claim']").hide();
        }, 10);
        frm.refresh_field('depends_on')
    },
    project: function(frm){
        filter(frm)
    },
    refresh: function(frm){
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
                    if(frm.fields[i].df.fieldname != "notes"){
                        frm.set_df_property(frm.fields[i].df.fieldname,"read_only",1)
                    }
                }
            }
        }
    },
    assigned_to: function(frm){
        if(!frm.doc.project){
            frappe.msgprint("Kindly Select Project.")
            frm.set_value("assigned_to","")
        }
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

//    notes: function(frm){
//     if(frm.doc.owner != frappe.session.user && frm.doc.notes != ""){
//         frappe.call({
//             method: "juzgo.juzgo.custom.py.task.notification",
//             args:{
//                 to_user: frm.doc.owner,
//                 from_user: frappe.session.user, 
//                 task_name: frm.doc.name, 
//                 data: frm.doc.notes, 
//                 doctype: frm.doc.doctype,
//                 field: "Notes"
//             }
//         })     
//     }
//    },
//    description: function(frm){
//     if(frm.doc.owner == frappe.session.user && frm.doc.description != ""){
//         frappe.call({
//             method: "juzgo.juzgo.custom.py.task.notification",
//             args:{
//                 to_user: frm.doc.assigned_to,
//                 from_user: frappe.session.user, 
//                 task_name: frm.doc.name, 
//                 data: frm.doc.description, 
//                 doctype: frm.doc.doctype,
//                 field: "Description"
//             }
//         })     
//     }
//    }

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
   
})