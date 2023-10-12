import frappe
from frappe.model.mapper import get_mapped_doc
def validate(doc,actions):
	if doc.lead_owner and (actions == "after_insert" or not doc.is_new()):
		assigned_to(doc,"lead_owner")
	if doc.assign_to and (actions == "after_insert" or not doc.is_new()):
		assigned_to(doc,"assign_to")

def assigned_to(doc,field_name):
	doc_ = frappe.new_doc("ToDo")        
	if frappe.db.exists("ToDo", {'reference_name': doc.name, 'field_name':field_name}):
		doc_ = frappe.get_doc("ToDo", {'reference_name': doc.name, 'field_name':field_name})
	user = frappe.db.get_value("User", doc.owner, "username")
	doc_.update({
		'date': frappe.utils.nowdate(),
		'allocated_to': doc.get(field_name),
		'description': f'Assignment for {doc.doctype} {doc.name}',
		'reference_type': doc.doctype,
		'reference_name': doc.name,
		'assigned_by': user,
		'field_name': field_name
	})
	doc_.flags.ignore_permissions = True
	doc_.flags.ignore_links = True
	doc_.save()

@frappe.whitelist()
def make_ca_form(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.party_type = "Lead"

	target_doc = get_mapped_doc(
		"Lead",
		source_name,
		{"Lead": {"doctype": "CA Form", "field_map": {"mobile_no": "mobile","whatsapp_no": "whatsapp_number", "email_id":"e_mail","mobile":"mobile_no"}}},
		target_doc,
		set_missing_values,
	)

	return target_doc