from frappe import _


def get_data(data):
	return {
		"fieldname": "destination",
		"non_standard_fieldnames": {
			"Check List": "destination",
			"Project": "destination",
		},
		"transactions": [
			{"label": _("Check List"), "items": ["Check List","Project"]},
			{"label": _("Master"), "items": ["Hotel Details","Restaurant","Spots","Operator"]},
		],
	}