var desig_filter = [];
frappe.ui.form.on('Job Opening', {
    refresh:async function(frm){
		await frm.trigger("staffing_plan")
		frm.set_query("designation",function(){
			return {
				filters:desig_filter.length?{
					name:["in", desig_filter]
				}:{}
				
			}
		})
    },
    staffing_plan: async function(frm){
        await frappe.call({
            
            method: "juzgo.juzgo.custom.py.jobopening.get_staf_designation",
            args:{
                staffing_plan:frm.doc.staffing_plan,
            },
            callback: function(r) {
				desig_filter=r.message
				if(desig_filter.length == 1){
					frm.set_value("designation",desig_filter[0])
				}

        }
        })
        
    },

})

