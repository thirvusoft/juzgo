from frappe import _


def get_data():
	return {
		"fieldname": "spots",
		"non_standard_fieldnames": {
			"Hotel Details": "places",
		},
		"transactions": [
			{"label": _(""), "items": ["Hotel Details"]},
		],
	}