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
        if doc.assigned_to:
            if not doc.priority_number:
                task_list = frappe.get_value("Task", {"status": ["in", ["Open", "Working"]], 'assigned_to':doc.assigned_to, 'name':['!=',doc.name]}, "priority_number", order_by = "priority_number desc" ) or 0
                if doc.status in ["Open", "Working"]:
                    doc.priority_number = task_list + 1
            task_dec = frappe.get_all("Task", filters={"status": ["in", ["Open", "Working"]], 'assigned_to':doc.assigned_to, 'name':['!=',doc.name],'priority_number':[">",doc.priority_number]}, fields=['priority_number','name'])
            if doc.status == "Completed":
                for i in task_dec:
                    frappe.db.set_value("Task",i.name,"priority_number",i.priority_number-1)

        # if doc.priority_number ==0 and doc.status in ["Open", "Working"]:
        #      doc.priority_number += 1
        #      print("==")
                # frappe.db.set_value("Task",task.name,"priority_number",doc.priority_number + task.priority_number)
        # if doc.status in ["Open", "Working"]:
        #     doc.priority_number += 1    
            # else:
            #     c=task.priority_number+c
            #     doc.priority_number = c

# def on_update(doc,actions):
#     task = frappe.get_all("Timesheet Detail",filters={'task':doc.name,'completed':["!=",1]},fields=['parent','priority_order','task'])
#     frappe.db.set_value("Timesheet Detail",task.task,'priority_order',)

