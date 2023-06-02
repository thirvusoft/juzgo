import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def setup():
    setup_fields()

def setup_fields():
    custom_fields = {
        'HR Settings':[
            dict(
                fieldname= "send_interview_round_status",
                fieldtype= "Check",
                insert_after= "feedback_reminder_notification_template ",
                label= "Send Interview Round Status",
            ),
            dict(
                fieldname= "send_interview_round_status_template",
                fieldtype= "Check",
                insert_after= "send_interview_round_status ",
                label= "Send Interview Round Status Template",
                depends_on= "eval:doc.send_interview_round_status"
            ),
        ]
    }
    create_custom_fields(custom_fields)