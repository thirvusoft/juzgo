from frappe import _


def get_data():
	return {
		"fieldname": "inclusion",
		"non_standard_fieldnames": {
			"Spots": "inclusion_name",
		},
		"transactions": [
			{"label": _(""), "items": ["Spots"]},
		],
	}