import frappe

def send_interview_round_status(doc,action):
    send_main(doc,"send_interview_round_status", "send_interview_round_status_template")
    
def send_mail_interview_created(doc,action):
    send_main(doc,"send_mail_interview_created", "send_mail_interview_created_template")

def send_main(doc, check_field, template_field):
    reminder_settings = frappe.db.get_value(
        "HR Settings",
        "HR Settings",
        [check_field, template_field],
        as_dict=True,
    )

    if not reminder_settings[check_field] or reminder_settings[check_field] == "0":
        return
    
    interview_template = frappe.get_doc(
        "Email Template", reminder_settings.get(template_field)
    )
    
    context = doc.as_dict()
    message = frappe.render_template(interview_template.response, context)
    recipients = frappe.db.get_value("Job Applicant", doc.job_applicant, "email_id")

    frappe.sendmail(
        recipients=recipients,
        subject=interview_template.subject,
        message=message,
        reference_doctype=doc.doctype,
        reference_name=doc.name,
    )