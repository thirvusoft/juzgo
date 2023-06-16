frappe.ui.form.on("Employee",{
    create_user:function(frm){
        var d = new frappe.ui.Dialog({
            title: 'Profile Details',
            size: 'small',
            minimizable: true,
            static: true,
            fields: [
                {
                    label:"Role Profile",
                    fieldname: 'role_profile_name',
                    fieldtype: 'Link',
                    options: "Role Profile",
                },
                {
                    label:"Module Profile",
                    fieldname: 'module_profile',
                    fieldtype: 'Link',
                    options: "Module Profile",
                },
                {
                    label:"Password",
                    fieldname: 'new_password',
                    fieldtype: 'Password',
                }
            ],
            primary_action_label: 'Update User',
            secondary_action_label: 'Close',
            async primary_action(data) {
                if (!frm.doc.prefered_email) {
                    frappe.throw(__("Please enter Preferred Contact Email"));
                }
                frappe.call({
                    method: "juzgo.juzgo.custom.py.employee.create_users",
                    args: {
                        employee: frm.doc.name,
                        email: frm.doc.prefered_email,
                        data:data
                    },
                    callback: function (r) {
                        frm.set_value("user_id", r.message);
                        frm.save() //corecodewhile creating a user employee can save the auto
                    }
                });
                d.hide()
            },
            secondary_action() {
                d.hide()
            }
        })
        d.$wrapper.find('.btn-link').css('width', '100px');
        d.show()
    }
})