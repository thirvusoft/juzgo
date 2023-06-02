import frappe

@frappe.whitelist()
def get_interview_questions(interview_round):
    return frappe.get_all("Interview Questions", filters={"parent": interview_round}, fields=["question"])