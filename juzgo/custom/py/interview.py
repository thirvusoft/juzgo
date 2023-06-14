import frappe
from frappe.utils.password import encrypt
from time import sleep

def get_url(self, event=None):
    url = f"{frappe.utils.get_url()}/interview/new?#{encrypt(self.name)}"
    self.web_form_url = url

@frappe.whitelist()
def send_email_url(interview):
    try:
        interview_doc = frappe.get_doc("Interview", interview)
        subject_template = frappe.db.get_single_value("Interview Settings", "subject_template")
        message_template = frappe.db.get_single_value("Interview Settings", "message_template")
        job_application = frappe.get_doc("Job Applicant", interview_doc.job_applicant)
        
        frappe.sendmail(
            recipients=[job_application.email_id],
            subject=frappe.render_template(template=subject_template, context={"interview": interview_doc, "job_application": job_application, "frappe": frappe}),
            message=frappe.render_template(template=message_template, context={"interview": interview_doc, "job_application": job_application, "frappe": frappe}),
        )
        return True
    except:
        pass