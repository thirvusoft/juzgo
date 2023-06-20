import json
import frappe

@frappe.whitelist()
def create_users(employee, user=None, email=None, data=None):
	emp = frappe.get_doc("Employee", employee)
	data = json.loads(data)
	employee_name = emp.employee_name.split(" ")
	middle_name = last_name = ""

	if len(employee_name) >= 3:
		last_name = " ".join(employee_name[2:])
		middle_name = employee_name[1]
	elif len(employee_name) == 2:
		last_name = employee_name[1]

	first_name = employee_name[0]

	if email:
		emp.prefered_email = email

	user = frappe.new_doc("User")
	user.update(
		{
			"name": emp.employee_name,
			"email": emp.prefered_email,
			"enabled": 1,
			"first_name": first_name,
			"middle_name": middle_name,
			"last_name": last_name,
			"gender": emp.gender,
			"birth_date": emp.date_of_birth,
			"phone": emp.cell_number,
			"bio": emp.bio,
            "new_password":data.get("new_password"),
            "module_profile":data.get("module_profile"),
            "role_profile_name":data.get("role_profile_name")
		}
	)
	user.insert()
	return user.name