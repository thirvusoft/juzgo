from frappe import _


def get_data():
	return {
		"fieldname": "operator",
		"non_standard_fieldnames": {
			"Vehicle Detail":"operator",
		},
		"transactions": [
			{"label": _(""), "items": ["Vehicle Detail"]},
		],
	}