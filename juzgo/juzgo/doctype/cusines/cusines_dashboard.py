from frappe import _


def get_data():
	return {
		"fieldname": "cusines",
		"non_standard_fieldnames": {
			"Restaurant": "cusines_name",
		},
		"transactions": [
			{"label": _(""), "items": ["Restaurant"]},
		],
	}