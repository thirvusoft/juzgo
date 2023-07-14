from frappe import _


def get_data():
	return {
		"fieldname": "flavour_type",
		"non_standard_fieldnames": {
			"Destination": "flavour_type",
			"Spots":"flavour_of_the_sopt"
		},
		"transactions": [
			{"label": _(""), "items": ["Destination","Spots"]},
		],
	}