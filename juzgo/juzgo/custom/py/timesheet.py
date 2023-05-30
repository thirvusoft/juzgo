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
    filtered_tasks = frappe.get_all('Task', filters={'name':['in', assigned_tasks], 'exp_start_date':['<=', today()], 'status':['in', ['Open', 'Working', 'Overdue', 'Pending Client Approval']]}, fields=['name as task', 'project', 'description', 'priority', '(expected_time - actual_time) as expected_hours', 'issue'])
    filtered_tasks.extend(
        frappe.get_all('Task', filters={'name':['in', assigned_tasks], 'exp_start_date':['<=', today()], 'exp_end_date':['>=', today()], 'status':['in', ['Open', 'Working', 'Overdue', 'Pending Client Approval']]}, fields=['name as task', 'project', 'description', 'priority', '(expected_time - actual_time) as expected_hours', 'issue'])
        )
    for i in filtered_tasks:
        if(i.get('description')):
            i['description'] = strip_html_tags(i['description'])
    filtered_tasks = list({i['task']:i for i in filtered_tasks if i['task'] not in tasks}.values())
    return filtered_tasks