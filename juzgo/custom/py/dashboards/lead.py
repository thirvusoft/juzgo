from frappe import _


def get_data(*a, **b):
	return {
		"fieldname": "lead",
		"transactions": [
			{"items": ["CA Form","Project"]},
		],
	}
