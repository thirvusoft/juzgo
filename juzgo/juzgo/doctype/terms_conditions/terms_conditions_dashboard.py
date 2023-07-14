from frappe import _


def get_data():
	return {
		"fieldname": "terms_conditions",
		"non_standard_fieldnames": {
			"Destination": "terms_conditions",
		},
		"transactions": [
			{"label": _(""), "items": ["Destination"]},
		],
	}