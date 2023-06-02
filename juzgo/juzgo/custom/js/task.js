frappe.ui.form.on('Task', {
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