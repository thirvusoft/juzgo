from frappe import _


def get_data():
	return {
		"fieldname": "Cabin Specifications",
		"non_standard_fieldnames": {
			"Cruise": "spec",
		},
		"transactions": [
			{"label": _(""), "items": ["Cruise"]},
		],
	}