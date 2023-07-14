from frappe import _


def get_data():
	return {
		"fieldname": "tariff_based_on",
		"non_standard_fieldnames": {
			"Operator": "tariff_based_on",
		},
		"transactions": [
			{"label": _(""), "items": ["Operator"]},
		],
	}