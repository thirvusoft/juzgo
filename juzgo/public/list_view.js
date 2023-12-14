class ListView extends frappe.views.ListView {
    make_new_doc() {
        if(this.doctype == "Project"){
            if(frappe.user.has_role("Juzgo Admin") || frappe.user.has_role("Thirvu Admin")){
                
            } else {
				frappe.throw("You Not Have Permission to Create Project Directly. You Can Create from CA Form.")
			}
        }
		const doctype = this.doctype;
		const options = {};
		this.filter_area.get().forEach((f) => {
			if (f[2] === "=" && frappe.model.is_non_std_field(f[1])) {
				options[f[1]] = f[3];
			}
		});
		frappe.new_doc(doctype, options);
	}
}
frappe.views.ListView =ListView
