frappe.ui.form.on('Job Opening', {
    refresh:function(frm){
        frm.add_custom_button(__('Staffing Plan'), () => frm.events.get_items_from_staffing_plan(frm),
            __("Get Items From"));
        
    },
	get_items_from_staffing_plan: function(frm) {
		erpnext.utils.map_current_doc({
			method: "juzgo.juzgo.custom.py.jobopening.make_material_request",
			source_doctype: "Staffing Plan",
			target: frm,
			setters: {
				// name: undefined,
			},
			get_query_filters: {
				docstatus: 1,
				company: frm.doc.company
			}
		});
	},

})