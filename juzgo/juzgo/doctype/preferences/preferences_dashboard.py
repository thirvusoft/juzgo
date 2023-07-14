from frappe import _


def get_data():
	return {
		"fieldname": "preferences",
		"non_standard_fieldnames": {
			"Destination": "preferences",
		},
		"transactions": [
			{"label": _(""), "items": ["Destination"]},
		],
	}