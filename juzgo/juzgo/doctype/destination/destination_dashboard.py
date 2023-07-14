from frappe import _


def get_data():
	return {
		"fieldname": "destination",
		"non_standard_fieldnames": {
			"Check List": "destination",
			"Project": "destination",
			"Vehicle Detail": "destination_name",
			"Cruise": "from_destination",
		},
		"transactions": [
			{"label": _(""), "items": ["Check List","Project","Vehicle Detail"]},
			{"label": _(""), "items": ["Hotel Details","Restaurant","Cruise"]},
			{"label": _(""), "items": ["Spots","Operator"]},
		],
	}