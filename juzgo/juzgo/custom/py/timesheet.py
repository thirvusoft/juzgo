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
    assigned_tasks = frappe.get_all('Task', filters={'assigned_to':user, 'status':['in', ['Open', 'Working', 'Overdue','Pending Review']]}, pluck='name')
    filtered_tasks = frappe.get_all('Task', filters={'name':['in', assigned_tasks], 'exp_start_date':['<=', today()], 'status':['in', ['Open', 'Working', 'Overdue', 'Pending Review']]}, fields=['name as task', 'project', 'description', 'priority', '(expected_time) as expected_hours', 'issue','priority_number as priority_order','expected_min','subject as task_name','notes'],order_by = "priority_number")
    filtered_tasks.extend(
        frappe.get_all('Task', filters={'name':['in', assigned_tasks], 'exp_start_date':['<=', today()], 'exp_end_date':['>=', today()], 'status':['in', ['Open', 'Working', 'Overdue','Pending Review']]}, fields=['name as task', 'project', 'description', 'priority', '(expected_time) as expected_hours', 'issue','priority_number as priority_order','expected_min','subject as task_name','notes'],order_by = "priority_number")
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

            # task_ = frappe.get_doc("Task",i.task)
            # task_.update({
            #         'notes': i.notes
            # })
            # task_.save()


@frappe.whitelist()               
def existing_draft_timesheet(owner,doc_name):
    user = frappe.db.get_value("User", owner, "name")
    timesheets = frappe.get_all("Timesheet", filters={'owner': user,'name':['!=',doc_name], 'status': ['not in', ['Cancelled', 'Submitted']]},fields=['name','status'])
    for timesheet in timesheets:
        if timesheet.status != "Submitted" or timesheet.status != "Cancelled" :
            return frappe.throw(f"Submit your Existing Timesheet {timesheet.name} to create new timesheet")

class OverlapError(frappe.ValidationError):
	pass
from erpnext.projects.doctype.timesheet.timesheet import Timesheet
from frappe.utils import add_to_date, flt, get_datetime, getdate, time_diff_in_hours
from frappe import _
class time_sheet(Timesheet):
    def validate_dates(self):
        for data in self.time_logs:
            if data.from_time and data.to_time and time_diff_in_hours(data.to_time, data.from_time) < 0:
                frappe.throw(_("To Time {0} cannot be before from Time {1} (Negative time {2} is not accept) for the Task {3}").format(data.to_time, data.from_time,round(data.taken_min), data.task))
    def validate_mandatory_fields(self):
        c=0
        for data in self.time_logs:
            if not data.from_time and not data.to_time:
                c = c+1
        if c == len(self.time_logs):
            frappe.throw(_("Atleast 1 Row From Time and To Time is mandatory to Submit."))
    def check_internal_overlap(self, fieldname, args):
        for time_log in self.time_logs:
            if not (time_log.from_time and time_log.to_time and args.from_time and args.to_time):
                continue

            from_time = get_datetime(time_log.from_time)
            to_time = get_datetime(time_log.to_time)
            args_from_time = get_datetime(args.from_time)
            args_to_time = get_datetime(args.to_time)

            if (
                (args.get(fieldname) == time_log.get(fieldname))
                and (args.idx != time_log.idx)
                and (
                    (args_from_time > from_time and args_from_time < to_time)
                    or (args_to_time > from_time and args_to_time < to_time)
                    or (args_from_time <= from_time and args_to_time >= to_time)
                )
            ):
                frappe.throw(
                _("Row {0}: From Time and To Time is overlapping with Row {1}").format(
                    args.idx, time_log.idx
                ),
                OverlapError,
            )
                return True
        return False
def get_notes(doc, actions):
    for i in doc.time_logs:
        if i.task:
            notes,description = frappe.get_value("Task",  i.task,['notes','description']) or ["",""]
            if notes:
                i.notes = strip_html_tags(notes) 
            if description:
                i.description = strip_html_tags(description) 

