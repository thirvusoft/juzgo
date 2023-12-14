class FormDashboard extends frappe.ui.form.Dashboard {
    after_refresh() {
		// show / hide new buttons (if allowed)
		this.links_area.body.find(".btn-new").each((i, el) => {
            if(frappe.user.has_role("Juzgo Admin") || frappe.user.has_role("Thirvu Admin")){
			    if (this.frm.can_create($(el).attr("data-doctype"))) {
                    $(el).removeClass("hidden");
                }
			} else {
                if($(el).attr("data-doctype") != "Project"){
                    if (this.frm.can_create($(el).attr("data-doctype"))) {
                        $(el).removeClass("hidden");
                    }
                }
            }
		});
		!this.frm.is_new() && this.set_open_count();
	}
}
frappe.ui.form.Dashboard = FormDashboard