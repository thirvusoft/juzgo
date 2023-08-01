class AssignTo extends frappe.ui.form.AssignTo {
    render(assignments) {
		this.frm.get_docinfo().assignments = assignments;

		let assignments_wrapper = this.parent.find(".assignments");

		assignments_wrapper.empty();
		let assigned_users = assignments.map((d) => d.owner);

		if (!assigned_users.length) {
			assignments_wrapper.hide();
			return;
		}

		let avatar_group = frappe.avatar_group(assigned_users, 5, {
			align: "left",
			overlap: true,
		});

		assignments_wrapper.show();
		assignments_wrapper.append(avatar_group);
		avatar_group.click(() => {
			//thirvu change
			if (this.frm.doctype == "Task"){
				this.frm.scroll_to_field('assigned_to')
				frappe.throw(__('You can assign task only in "Assigned To" to do the work. If you want to share with others, Assign in Task lead. Not allowed to assign task More then 2 persons'));
				return;
			}
            if (this.frm.doctype == "Lead"){
				this.frm.scroll_to_field('assign_to')
				frappe.throw(__('You can assign Lead only in "Assign To" or "Lead Owner".'));
				return;
			}
			if (this.frm.doctype == "CA Form"){
				this.frm.scroll_to_field('assigned_to')
				frappe.throw(__('You can assign CA Form only in "Assigned To" or "CA Owner".'));
				return;
			}
			new frappe.ui.form.AssignmentDialog({
				assignments: assigned_users,
				frm: this.frm,
			});
		});
	}
	add() {
		var me = this;
		//thirvu change
		if (this.frm.doctype == "Task"){
			this.frm.scroll_to_field('assigned_to')
			frappe.throw(__('You can assign task only in "Assigned To" to do the work. If you want to share with others, Assign in Task lead. Not allowed to assign task More then 2 persons'));
			return;
		}
        if (this.frm.doctype == "Lead"){
			this.frm.scroll_to_field('assign_to')
			frappe.throw(__('You can assign task only in "Assign To" or "Lead Owner".'));
			return;
		}
		if (this.frm.doctype == "CA Form"){
			this.frm.scroll_to_field('assigned_to')
			frappe.throw(__('You can assign CA Form only in "Assigned To" or "CA Owner".'));
			return;
		}
		if (this.frm.is_new()) {
			frappe.throw(__("Please save the document before assignment"));
			return;
		}

		if (!me.assign_to) {
			me.assign_to = new frappe.ui.form.AssignToDialog({
				method: "frappe.desk.form.assign_to.add",
				doctype: me.frm.doctype,
				docname: me.frm.docname,
				frm: me.frm,
				callback: function (r) {
					me.render(r.message);
				},
			});
		}
		me.assign_to.dialog.clear();
		me.assign_to.dialog.show();
	}
}

frappe.ui.form.AssignTo = AssignTo