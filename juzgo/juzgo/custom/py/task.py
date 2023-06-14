import frappe
from frappe.utils.data import nowdate

def user_todo(doc, actions):
    if doc.assigned_to and (actions == "after_insert" or not doc.is_new()):
        doc_ = frappe.new_doc("ToDo")        
        if frappe.db.exists("ToDo", {'reference_name': doc.name}):
            doc_ = frappe.get_doc("ToDo", {'reference_name': doc.name})
        user = frappe.db.get_value("User", doc.owner, "username")
        doc_.update({
            'date': frappe.utils.nowdate(),
            'allocated_to': doc.assigned_to,
            'description': f'Assignment for {doc.doctype} {doc.name}',
            'reference_type': doc.doctype,
            'reference_name': doc.name,
            'assigned_by': user,
        })
        doc_.flags.ignore_permissions = True
        doc_.flags.ignore_links = True
        doc_.save()

def update_number(doc, actions):
        user(doc, doc.assigned_to)
        assigned = frappe.db.get_value("Task",doc.name,"assigned_to")
        if doc.assigned_to != assigned:
            user(doc, assigned)
        
            
def user(doc, user):
    if user:
        priority_update = frappe.get_all("Task", filters={"status": ["in", ["Open", "Working"]], 'assigned_to': user}, pluck='name',order_by = "priority_number")
        if doc.name not in priority_update:
            priority_update.insert(((doc.priority_number  -1) if doc.priority_number else len(priority_update)), doc.name)
            doc.priority_number =priority_update.index(doc.name)+1
        if user!= doc.assigned_to:
            priority_update.remove(doc.name)
        if doc.status not in ["Open", "Working"]:
            priority_update.remove(doc.name)
        if doc.name in priority_update:
            if not doc.priority_number:
                doc.priority_number = priority_update.index(doc.name)+1
            current = priority_update.pop(priority_update.index(doc.name))
            priority_update.insert(doc.priority_number -1, current)
        idx =1 
        for m in priority_update:
            frappe.db.set_value("Task",m,"priority_number",idx)
            idx+=1
            
@frappe.whitelist()
def minutes_to_hours(minutes = None):
    if minutes:
        minutes = float(minutes)
        hours = minutes / 60
        return hours
    return 0

@frappe.whitelist()
def hours_to_minutes(hours = None):
    if hours:
        hours = float(hours)
        minutes = hours * 60
        return minutes
    return 0
from frappe.utils import date_diff,getdate, now,nowdate
def overdue_days():
    overdue_task = frappe.db.get_all("Task",filters={"status":"Overdue"},fields=["exp_end_date","name"])
    for i in overdue_task:
        overdue_days = date_diff(getdate(nowdate()), i.exp_end_date)
        if overdue_days > 0:
            frappe.db.set_value(
                    "Task",
                    i.name,
                    "overdue_days",
                    overdue_days 
                )
