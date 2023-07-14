from frappe import _


def get_data():
	return {
		"fieldname": "vehicle_detail",
		"non_standard_fieldnames": {
			"Operator": "vehicle",
		},
		"transactions": [
			{"label": _(""), "items": ["Operator"]},
		],
	}