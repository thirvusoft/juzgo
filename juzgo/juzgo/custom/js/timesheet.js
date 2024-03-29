frappe.ui.form.on('Timesheet', {
    onload:function (frm) {
        setTimeout(() => {
            $("[data-doctype='Expense Claim']").hide();
        }, 10);
    },
	refresh: function(frm){
		frm.fields_dict.time_logs.$wrapper.find('.grid-remove-rows')[0].style.display = 'none'
		frm.$wrapper.find(".row.form-dashboard-section.form-links").addClass("hidden")
        let fetch_task_btn = document.querySelector('button[data-fieldname="fetch_task"]')
		if(fetch_task_btn){
			fetch_task_btn.style.backgroundColor = "#ffe6a1"
		}
		if(frm.is_new()){
			frm.events.get_tasks(frm)
		
			frappe.call({
				method: "juzgo.juzgo.custom.py.timesheet.existing_draft_timesheet",
				args:{
					owner: frm.doc.employee,
					doc_name : frm.doc.name
				},
				error: function(r){
					window.history.back()
				}
			})
		}
	},
	// on_submit(frm){
	// 	// frm.events.get_tasks(frm)
	// 	for(let c=0; c<frm.doc.time_logs.length; c++){
	// 		if(frm.doc.time_logs[c].task){
	// 			frappe.db
	// 			.get_list("Task", {
	// 				filters: { name: frm.doc.time_logs[c].task },
	// 				fields: ["notes"],
	// 			})
	// 			.then((result) => {
	// 			if(result){
	// 				frappe.model.set_value("Timesheet Detail",tasks[row.task],'notes',result)
	// 			}
	// 			});
	// 		}
	// 	}

		
	// },
	get_tasks: async function(frm){
        let tasks = {}
		for(let c=0; c<frm.doc.time_logs.length; c++){
			if(frm.doc.time_logs[c].task){
				tasks[frm.doc.time_logs[c].task] = frm.doc.time_logs[c].name
			}
		}
		frappe.call({
			method:"juzgo.juzgo.custom.py.timesheet.get_assigned_tasks",
			args:{
				emp: frm.doc.employee,
				tasks: []
			},
			callback: function(r){
				if(r.message){
					r.message.forEach((row)=>{
						if(!Object.keys(tasks).includes(row.task)){
							var new_child = frm.add_child('time_logs')
						
							for (const [key, value] of Object.entries(row)) {
								new_child[key] = value
							  }					
							  frm.refresh_field('time_logs')	
							  	
						}
						else{
							
							frappe.model.set_value("Timesheet Detail",tasks[row.task],'priority_order',row.priority_order)
							frappe.model.set_value("Timesheet Detail",tasks[row.task],'description',row.description)
							frappe.model.set_value("Timesheet Detail",tasks[row.task],'task_name',row.task_name)
							frappe.model.set_value("Timesheet Detail",tasks[row.task],'expected_hours',row.expected_hours)
							frappe.model.set_value("Timesheet Detail",tasks[row.task],'expected_min',row.expected_min)
							frappe.model.set_value("Timesheet Detail",tasks[row.task],'notes',row.notes)
						}
						calculate_time(frm);
					})
	
				}

			}
		})
	},
    fetch_task: function(frm){
		frm.events.get_tasks(frm)
	},
})
frappe.ui.form.on('Timesheet Detail', {
	time_logs_remove: function(frm) {
		calculate_time(frm);
	},
	taken_min: function(frm,cdt,cdn){
		var row = locals[cdt][cdn]
		frappe.call({
		method: "juzgo.juzgo.custom.py.task.minutes_to_hours",
		args:{
			minutes:row.taken_min,
		},
		callback: function(r) {
			frappe.model.set_value(cdt,cdn,"hours",r.message)
	   	}
	   })       
	},
	hours: function(frm,cdt,cdn){
		var row = locals[cdt][cdn]
	   frappe.call({
		method: "juzgo.juzgo.custom.py.task.hours_to_minutes",
		args:{
			hours:row.hours,
		},
		callback: function(r) {
			frappe.model.set_value(cdt,cdn,"taken_min",r.message)
	  	}
	  })       
  },
})

function calculate_time(frm){
	let tl = frm.doc.time_logs || [];
	let total_exp_hr = 0;
	for(var i=0; i<tl.length; i++) {
		if (tl[i].expected_hours) {
			total_exp_hr += tl[i].expected_hours;
		}
	}
	frm.set_value("total_expected_hours", total_exp_hr);
}

