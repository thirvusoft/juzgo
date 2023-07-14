from frappe import _


def get_data():
	return {
		"fieldname": "meal_plan",
		"non_standard_fieldnames": {
			"Hotel Details": "meal_plan",
		},
		"transactions": [
			{"label": _(""), "items": ["Hotel Details"]},
		],
	}