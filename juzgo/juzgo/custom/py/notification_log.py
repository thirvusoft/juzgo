import frappe
@frappe.whitelist()
def get_notification_logs(limit=20):
	notification_logs = frappe.db.get_list(
		"Notification Log", fields=["*"], filters={"read":0}, limit=limit, order_by="modified desc"
	)

	users = [log.from_user for log in notification_logs]
	users = [*set(users)]  # remove duplicates
	user_info = frappe._dict()

	for user in users:
		frappe.utils.add_user_info(user, user_info)

	return {"notification_logs": notification_logs, "user_info": user_info}