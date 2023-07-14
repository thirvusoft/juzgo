from frappe import _


def get_data():
	return {
		"fieldname": "mode_of_transport",
		"non_standard_fieldnames": {
			"Spots": "preferred_transfer",
			"Operator": "mode_of_transport",
		},
		"transactions": [
			{"label": _(""), "items": ["Spots","Operator"]},
		],
	}