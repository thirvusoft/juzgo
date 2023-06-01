frappe.ui.form.on('Staffing Plan', {
    refresh:function(frm){
        if(frm.doc.docstatus == 1){
            frm.add_custom_button(__('Job Opening'),
            () => frm.events.make_job_opening(frm), __('Create'));
        }

    },
    make_job_opening: function(frm) {
        frappe.call({
            method: "juzgo.juzgo.custom.py.staffplanning.make_job_opening",
            args: {
                name: frm.doc.name,
                staffing_details: frm.doc.staffing_details,
            },
            callback: function (r) {
                if (r.message >1) {
                    // Display a success message
                    frappe.show_alert({
                        message: "Job opening created successfully",
                        indicator: "green"
                    });
                } else if(r.message == 1) {
                    // Display a Already Created message
                    frappe.show_alert({
                        message: "Job Opening Already Created",
                        indicator: "green"
                    });
                } else{
                    // Display an error message
                    frappe.show_alert({
                        message: "Failed to create job opening",
                        indicator: "red"
                    });
                }
            }
        });
    },
    
})
