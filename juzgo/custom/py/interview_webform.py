import frappe
from cryptography.fernet import Fernet
from frappe.utils import cstr, encode
from frappe.utils.password import get_encryption_key

@frappe.whitelist(allow_guest=True)
def get_question_fields(data):
    try:
        cipher_suite = Fernet(encode(get_encryption_key()))
        data = cstr(cipher_suite.decrypt(encode(data)))
        questions = frappe.get_all("Interview Questions", filters={"parent": data}, pluck="question", order_by="idx")
        return [
            {
                "fieldname": f"interview_question_{ques+1}",
                "label": questions[ques],
                "fieldtype": "Small Text"
            } for ques in range(len(questions))
        ]
    except BaseException:
        return []
