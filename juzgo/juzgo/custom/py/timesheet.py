import frappe
import datetime
from frappe.utils import (
    strip_html_tags, 
    today
    )
@frappe.whitelist()
def get_assigned_tasks(tasks=[]):
    tasks = eval(tasks)
    user = frappe.session.user
    assigned_tasks = frappe.get_all('ToDo', filters={'reference_type':'Task', 'allocated_to':user, 'status':['!=', 'Cancelled']}, pluck='reference_name')
    filtered_tasks = frappe.get_all('Task', filters={'name':['in', assigned_tasks], 'exp_start_date':['<=', today()], 'status':['in', ['Open', 'Working', 'Overdue', 'Pending Client Approval',]]}, fields=['name as task', 'project', 'description', 'priority', '(expected_time - actual_time) as expected_hours', 'issue','priority_number as priority_order','expected_min','subject as task_name'],order_by = "priority_number")
    filtered_tasks.extend(
        frappe.get_all('Task', filters={'name':['in', assigned_tasks], 'exp_start_date':['<=', today()], 'exp_end_date':['>=', today()], 'status':['in', ['Open', 'Working', 'Overdue', 'Pending Client Approval']]}, fields=['name as task', 'project', 'description', 'priority', '(expected_time - actual_time) as expected_hours', 'issue','priority_number as priority_order','expected_min','subject as task_name'],order_by = "priority_number")
        )
    for i in filtered_tasks:
        if(i.get('description')):
            i['description'] = strip_html_tags(i['description'])
    filtered_tasks = list({i['task']:i for i in filtered_tasks if i['task'] not in tasks}.values())
    return filtered_tasks

def status_updated(doc,actions):
    existing_draft_timesheet(doc.owner, doc.name)
    for i in doc.time_logs:
        if i.task:
            if i.completed == 1:
                desc = frappe.get_value("Task",i.task,'status')
                if desc != "Completed":
                    i.priority_order = 0
                    user = frappe.db.get_value("User",doc.owner,"name")
                    task = frappe.get_doc("Task",i.task)
                    task.update({
                            'status':'Completed',
                            'completed_by':user,
                            'completed_on':doc.end_date,
                            'priority_number':0
                    })
                    task.save()

            task_ = frappe.get_doc("Task",i.task)
            task_.update({
                    'notes': i.notes
            })
            task_.save()


@frappe.whitelist()               
def existing_draft_timesheet(owner,doc_name):
    user = frappe.db.get_value("User", owner, "name")
    timesheets = frappe.get_all("Timesheet", filters={'owner': user,'name':['!=',doc_name], 'status': ['not in', ['Cancelled', 'Submitted']]},fields=['name','status'])
    for timesheet in timesheets:
        if timesheet.status != "Completed" or timesheet.status != "Cancelled":
            return frappe.throw(f"Submit your Existing Timesheet {timesheet.name} to create new timesheet")

