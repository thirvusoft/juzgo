from frappe import _


def get_data():
	return {
		"fieldname": "cancellation_policy",
		"non_standard_fieldnames": {
			"Destination": "cancellation_policy",
		},
		"transactions": [
			{"label": _(""), "items": ["Destination"]},
		],
	}