
class Page extends frappe.ui.Page {
    set_primary_action(label, click, icon, working_label) {
		if(label != "Add Project"){
			this.set_action(this.btn_primary, {
				label: label,
				click: click,
				icon: icon,
				working_label: working_label,
			});
			return this.btn_primary;
		}
	}
}
frappe.ui.Page = Page
