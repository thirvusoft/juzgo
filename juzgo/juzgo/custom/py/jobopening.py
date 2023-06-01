import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_material_request(source_name, target_doc=None):

	def update_item(source, target, source_parent):
		# qty is for packed items, because packed items don't have stock_qty field
		args = target.as_dict().copy()
		args.update(
			{
				"company": source_parent.get("company"),
			}
		)
	doc = get_mapped_doc(
		"Staffing Plan",
		source_name,
		{
			"Staffing Plan": {"doctype": "Job Opening", "validation": {"docstatus": ["=", 1]}},
			# "Staffing Plan Detail": {
			# 	"doctype": "Job Opening",
			# 	"field_map": {"designation": "designation"},
			# },
		},
		target_doc,
	)

	return doc