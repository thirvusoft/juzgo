frappe.ui.form.on("Interview", {
    refresh: async function (frm) {
        if (frm.is_new()) {
            frm.set_value("allow_multiple_responses", await frappe.db.get_single_value("Interview Settings", "allow_multiple_responses"))
        }
        if (!frm.is_new() && frm.doc.docstatus != 2 && frm.doc.status == "Pending") {
            frm.add_custom_button(__("Send Link in Email"), async function () {
                await frappe.call({
                    method: "juzgo.custom.py.interview.send_email_url",
                    args: {
                        interview: frm.doc.name
                    },
                    async: true,
                    freeze: true,
                    freeze_message: "Sending Email",
                    callback: function (r) { 
                        if (r.message) {
                            frappe.show_alert({message: "Email has been queued", indicator: "green"});
                        } else {
                            frappe.show_alert({message: "Couldn't send Email", indicator: "red"});
                        }
                    }
                })
            });
        }
    }
});
