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
    filtered_tasks = frappe.get_all('Task', filters={'name':['in', assigned_tasks], 'exp_start_date':['<=', today()], 'status':['in', ['Open', 'Working', 'Overdue', 'Pending Client Approval']]}, fields=['name as task', 'project', 'description', 'priority', '(expected_time - actual_time) as expected_hours', 'issue','priority_number as priority_order'],order_by = "priority_number")
    filtered_tasks.extend(
        frappe.get_all('Task', filters={'name':['in', assigned_tasks], 'exp_start_date':['<=', today()], 'exp_end_date':['>=', today()], 'status':['in', ['Open', 'Working', 'Overdue', 'Pending Client Approval']]}, fields=['name as task', 'project', 'description', 'priority', '(expected_time - actual_time) as expected_hours', 'issue','priority_number as priority_order'],order_by = "priority_number")
        )
    for i in filtered_tasks:
        if(i.get('description')):
            i['description'] = strip_html_tags(i['description'])
    filtered_tasks = list({i['task']:i for i in filtered_tasks if i['task'] not in tasks}.values())
    return filtered_tasks

def status_updated(doc,actions):
    for i in doc.time_logs:
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
        # else:
        #     desc = frappe.get_value("Task",i.task,'status')
        #     if desc != "Completed":
        #         if i.priority_order > 0:
        #             i.priority_order =-1
                            