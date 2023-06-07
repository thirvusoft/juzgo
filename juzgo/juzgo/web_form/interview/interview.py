import frappe, datetime
from cryptography.fernet import Fernet
from frappe.utils import cstr, encode, formatdate
from frappe.utils.password import get_encryption_key

def get_context(context):
	context.template = "juzgo/web_form/interview/interview_web_form.html"
	pass

def get_time(timedelta):
	total_seconds = timedelta.total_seconds()
	hours = int(total_seconds // 3600)
	minutes = int((total_seconds % 3600) // 60)
	seconds = int(total_seconds % 60)

	return  datetime.time(hour=hours, minute=minutes, second=seconds)

@frappe.whitelist(allow_guest=True)
def get_question_fields(data):
	result = {}
	try:
		cipher_suite = Fernet(encode(get_encryption_key()))
		interview = cstr(cipher_suite.decrypt(encode(data)))

		if not frappe.db.exists("Interview", interview):
			result = {
				'error': True
			}
		else:
			interview = frappe.get_doc("Interview", interview)
			questions = frappe.get_all("Interview Questions", filters={"parent": interview.interview_round}, fields=["question", "interview_question"], order_by="idx")
			job_applicant = frappe.get_doc("Job Applicant", interview.job_applicant)
			already_response_submitted = False
			form_status = ""

			if not interview.allow_multiple_responses:
				if frappe.get_all("Interview Response", {"interview": interview.name}):
					already_response_submitted=True

			form_opening_date = formatdate(interview.scheduled_on)
			
			form_opening_time = get_time(interview.from_time)
			form_closing_date = formatdate(interview.scheduled_on)
			form_closing_time = get_time(interview.to_time)

			if interview.allow_responses_only_in_the_scheduled_time:
				if interview.docstatus == 2:
					form_status = "form-closed"
				elif interview.status != "Pending":
					form_status = "form-closed"
				elif interview.scheduled_on > datetime.datetime.now().date():
					form_status = "form-closed"
				elif interview.scheduled_on < datetime.datetime.now().date():
					form_status = "form-not-opened"
				elif form_opening_time > datetime.datetime.now().time():
					form_status = "form-closed"
				elif form_closing_time < datetime.datetime.now().time():
					form_status = "form-not-opened"
				
			result = {
				"already_response_submitted": already_response_submitted,
				"form_status": form_status,
				"form_opening_date": form_opening_date,
				"form_opening_time": form_opening_time,
				"form_closing_date": form_closing_date,
				"form_closing_time": form_closing_time,
				"questions": [
					{
						"fieldname": f"interview_question_{ques+1}",
						"interview_question": questions[ques]["interview_question"],
						"label": questions[ques]["question"],
						"fieldtype": "Small Text"
					} for ques in range(len(questions))
				],
				"interview": interview.name,
				"job_applicant": job_applicant.name,
				"email_id": job_applicant.email_id,
				"phone_number": job_applicant.phone_number,
				"job_opening": job_applicant.job_title,
				"country": job_applicant.country,
				"designation": job_applicant.designation	
			}
	except BaseException:
		frappe.log_error(title="INTERVIEW WEB FORM", message=frappe.get_traceback())
		result = {
			"error": True
		}
	return result
