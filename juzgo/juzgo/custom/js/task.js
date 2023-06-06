frappe.ui.form.on('Task', {
    project: function(frm){
        filter(frm)
    },
    refresh: function(frm){
        filter(frm)
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
})

async function filter(frm){
    var list = []
        if(frm.doc.project){
            var d = await frappe.db
            .get_list("ToDo", {
                filters: { reference_type: "Project", reference_name: frm.doc.project},
                fields: ["assigned_by"],
            })
            .then((l) => {
                for(var i=0;i<l.length;i++){
                    list.push(l[i].assigned_by)
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