from frappe import _


def get_data():
	return {
		"fieldname": "holidays_list",
		"non_standard_fieldnames": {
			"spots":"holidays_list_name"
		},
		"transactions": [
			{"label": _(""), "items": ["Spots"]},
		],
	}