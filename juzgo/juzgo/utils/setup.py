import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def setup():
    setup_fields()
    role_creation()
    property_setter()
def property_setter():
    make_property_setter("Task", "status", "options", "Open\nWorking\nPending Review\nReviewed\nOverdue\nTemplate\nCompleted\nCancelled", "Long Text")
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
        ],
        'System Settings':[
            dict(
                fieldname= "sb_img_preview",
                fieldtype= "Section Break",
                insert_after= "disable_change_log_notification",
                label= "Image Preview",
                collapsible = 1
            ),
            dict(
                fieldname= "layout_width",
                fieldtype= "Data",
                insert_after= "sb_img_preview",
                label= "Layout Width",
                hidden=1
            ),
            dict(
                fieldname= "layout_height",
                fieldtype= "Data",
                insert_after= "layout_width",
                label= "Layout Height",
            ),
            dict(
                fieldname= "cb_img",
                fieldtype= "Column Break",
                insert_after= "layout_height",
            ),
            dict(
                fieldname= "image_width",
                fieldtype= "Data",
                insert_after= "cb_img",
                label= "Image Width",
            ),
            dict(
                fieldname= "image_height",
                fieldtype= "Data",
                insert_after= "image_width",
                label= "Image Height",
            ),
        ]
    }
    create_custom_fields(custom_fields)

def role_creation():
    if not frappe.db.exists("Role", "Juzgo Employee"):
        role = frappe.new_doc("Role")
        role.role_name = "Juzgo Employee"
        role.save()
    if not frappe.db.exists("Role", "Juzgo Admin"):
        role = frappe.new_doc("Role")
        role.role_name = "Juzgo Admin"
        role.save()