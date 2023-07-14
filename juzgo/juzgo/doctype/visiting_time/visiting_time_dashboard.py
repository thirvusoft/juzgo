from frappe import _


def get_data():
	return {
		"fieldname": "visiting_time",
		"non_standard_fieldnames": {
			"Spots": "visiting",
		},
		"transactions": [
			{"label": _(""), "items": ["Spots"]},
		],
	}