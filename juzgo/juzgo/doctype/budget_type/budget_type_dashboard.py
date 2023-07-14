from frappe import _


def get_data():
	return {
		"fieldname": "budget_type",
		"non_standard_fieldnames": {
			"Destination": "budget_type",
		},
		"transactions": [
			{"label": _(""), "items": ["Destination"]},
		],
	}