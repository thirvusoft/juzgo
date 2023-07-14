from frappe import _


def get_data():
	return {
		"fieldname": "visa_type",
		"non_standard_fieldnames": {
			"Destination": "visa_type",
		},
		"transactions": [
			{"label": _(""), "items": ["Destination"]},
		],
	}