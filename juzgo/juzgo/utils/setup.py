import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def setup():
    setup_fields()
    role_creation()
def setup_fields():
    custom_fields = {
        'HR Settings':[
            dict(
                fieldname= "send_interview_round_status",
                fieldtype= "Check",
                insert_after= "feedback_reminder_notification_template",
                label= "Send Interview Round Status",
            ),
            dict(
                fieldname= "send_interview_round_status_template",
                fieldtype= "Link",
                options= "Email Template",
                insert_after= "send_interview_round_status",
                label= "Send Interview Round Status Template",
                depends_on= "eval:doc.send_interview_round_status",
                mandatory_depends_on= "eval:doc.send_interview_round_status"
            ),
            dict(
                fieldname= "send_mail_interview_created",
                fieldtype= "Check",
                insert_after= "send_interview_round_status_template",
                label= "Send Mail Interview Created",
            ),
            dict(
                fieldname= "send_mail_interview_created_template",
                fieldtype= "Link",
                options= "Email Template",
                insert_after= "send_mail_interview_created",
                label= "Send Mail Interview Created Template",
                depends_on= "eval:doc.send_mail_interview_created",
                mandatory_depends_on= "eval:doc.send_mail_interview_created"
            ),
        ]
    }
    create_custom_fields(custom_fields)

def role_creation():
    if not frappe.db.exists("Role", "Juzgo Employee"):
        role = frappe.new_doc("Role")
        role.role_name = "Juzgo Employee"
        role.save()