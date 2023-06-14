import frappe

def send_interview_round_status(doc,action):
    send_main(doc,"send_interview_round_status", "send_interview_round_status_template")
    
def send_mail_interview_created(doc,action):
    send_main(doc,"send_mail_interview_created", "send_mail_interview_created_template")

def send_main(doc, check_field, template_field):
    
    if not frappe.get_value(
        "HR Settings",
        "HR Settings",
        check_field
    ):
        return
    
    interview_template = frappe.get_doc(
        "Email Template", frappe.get_value(
        "HR Settings",
        "HR Settings",
        template_field
    )
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
from hrms.hr.doctype.interview.interview import get_interviewers
@frappe.whitelist()
def create_interview(doc, interview_round):
	import json

	if isinstance(doc, str):
		doc = json.loads(doc)
		doc = frappe.get_doc(doc)

	round_designation = frappe.db.get_value("Interview Round", interview_round, "designation")

	if round_designation and doc.designation and round_designation != doc.designation:
		frappe.throw(
			_("Interview Round {0} is only applicable for the Designation {1}").format(
				interview_round, round_designation
			)
		)

	interview = frappe.new_doc("Interview")
	interview.interview_round = interview_round
	interview.job_applicant = doc.name
	interview.designation = doc.designation
	interview.resume_link = doc.resume_link
	interview.job_opening = doc.job_title
	interview.resume_attachment = doc.resume_attachment
	interviewer_detail = get_interviewers(interview_round)

	for d in interviewer_detail:
		interview.append("interview_details", {"interviewer": d.interviewer})
	return interview