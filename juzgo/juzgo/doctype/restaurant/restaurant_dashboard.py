from frappe import _


def get_data():
	return {
		"fieldname": "restaurant",
		"non_standard_fieldnames": {
			"Hotel Details": "restaurant_name",
		},
		"transactions": [
			{"label": _(""), "items": ["Hotel Details"]},
		],
	}