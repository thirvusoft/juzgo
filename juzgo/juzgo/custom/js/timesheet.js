frappe.ui.form.on('Timesheet', {
    
	refresh: function(frm){
        let fetch_task_btn = document.querySelector('button[data-fieldname="fetch_task"]')
		if(fetch_task_btn){
			fetch_task_btn.style.backgroundColor = "#ffe6a1"
		}
		if(frm.is_new()){
			frm.events.get_tasks(frm, 1)
		}	
	},

	get_tasks: async function(frm){
        let tasks = []
		for(let c=0; c<frm.doc.time_logs.length; c++){
			if(frm.doc.time_logs[c].task){
				tasks.push(frm.doc.time_logs[c].task)
			}
		}
		frappe.call({
			method:"juzgo.juzgo.custom.py.timesheet.get_assigned_tasks",
			args:{
				tasks: tasks
			},
			callback: function(r){
				if(r.message){
					r.message.forEach((row)=>{
						
						var new_child = frm.add_child('time_logs')
						for (const [key, value] of Object.entries(row)) {
							new_child[key] = value
						  }
						  frm.refresh_field('time_logs')
					})
	
				}
			}
		})
	},
    fetch_task: function(frm){
		frm.events.get_tasks(frm)
	},
})
