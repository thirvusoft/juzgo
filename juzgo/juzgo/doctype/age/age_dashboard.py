from frappe import _


def get_data():
	return {
		"fieldname": "age",
		"non_standard_fieldnames": {
			"Destination": "age_group",
		},
		"transactions": [
			{"label": _(""), "items": ["Destination"]},
		],
	}