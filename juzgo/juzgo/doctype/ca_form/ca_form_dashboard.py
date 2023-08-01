from frappe import _


def get_data():
	return {
		"fieldname": "ca_form",
		# "non_standard_fieldnames": {
		# 	
		# },
		"transactions": [
			{"label": _("Project"), "items": ["Project"]},
		],
	}