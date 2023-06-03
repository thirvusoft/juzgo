from frappe import _


def get_data(*a, **b):
	return {
		"fieldname": "interview",
		"transactions": [
			{"items": ["Interview Feedback", "Interview Response"]},
		],
	}
