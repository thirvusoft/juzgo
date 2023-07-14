from frappe import _


def get_data():
	return {
		"fieldname": "season",
		"non_standard_fieldnames": {
			"Destination": "season_name",
			"Spots": "season",
		},
		"transactions": [
			{"label": _(""), "items": ["Operator","Destination"]},
			{"label": _(""), "items": ["Hotel Details"]},
			{"label": _(""), "items": ["Spots"]},
		],
	}