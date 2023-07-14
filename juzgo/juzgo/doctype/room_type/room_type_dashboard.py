from frappe import _


def get_data():
	return {
		"fieldname": "room_type",
		"non_standard_fieldnames": {
			"Hotel Details": "room_type",
		},
		"transactions": [
			{"label": _(""), "items": ["Hotel Details"]},
		],
	}