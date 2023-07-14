from frappe import _


def get_data():
	return {
		"fieldname": "class",
		"non_standard_fieldnames": {
			"Operator": "class",
		},
		"transactions": [
			{"label": _(""), "items": ["Operator"]},
		],
	}