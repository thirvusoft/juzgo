from frappe import _


def get_data():
	return {
		"fieldname": "exclusion",
		"non_standard_fieldnames": {
			"Spots": "exclusion_name",
		},
		"transactions": [
			{"label": _(""), "items": ["Spots"]},
		],
	}