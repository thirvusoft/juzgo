import frappe
from frappe.model.naming import make_autoname, revert_series_if_last
from frappe.utils.data import nowdate
from frappe import _, msgprint
from frappe.utils import today
from frappe.utils import cint, cstr
import json

def user_todo(doc, actions):
    if(doc.owner != frappe.session.user and not doc.is_new()):
        if(frappe.get_value("Task",doc.name,"notes") != doc.notes):
            notification(
            doc.owner,
            frappe.session.user, 
            doc.name, 
            doc.notes, 
            doc.doctype,
            "Notes")
    if(doc.owner == frappe.session.user and not doc.is_new()):
        if(frappe.get_value("Task",doc.name,"description") != doc.description):
            notification(
            doc.assigned_to,
            frappe.session.user, 
            doc.name, 
            doc.description, 
            doc.doctype,
            "Description")
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
        
        if(doc.depends_on):
            for i in doc.depends_on:
                if not i.task:
                    sub_task=frappe.new_doc("Task")
                    if not frappe.db.exists("Task",{"name":i.task}):
                        sub_task.update({
                        "subject":i.subject1,
                        "project":doc.project,
                        "abbr":doc.abbr,
                        "assigned_to":i.assigned_to,
                        "exp_start_date":doc.exp_start_date,
                        "expected_min":i.expected_min,
                        "description":(i.get("subject",""))
                    })
                        sub_task.run_method=lambda *a,**b:0
                        sub_task.save(ignore_permissions = True)   
                        i.update({
                            'task':sub_task.name,
                            'assigned_to':sub_task.assigned_to,
                            'expected_min':sub_task.expected_min
                        })
                        frappe.msgprint(_("Sub Tasks Created successfully"))
                    elif(frappe.db.exists("Task",{"name":i.task})):
                        task_doc=frappe.get_doc("Task",i.task)
                        if i.subject != task_doc.description:
                            task_doc.description=i.subject
                            task_doc.save()
                else:
                    sub_task = frappe.get_doc("Task",i.task)
                    i.update({'subject1':sub_task.subject,'subject':sub_task.description})

            
        else:
            if frappe.db.exists("Task Depends On",{"task":doc.name}):
                save =0
                parent_task=frappe.get_doc("Task Depends On",{"task":doc.name})
                if parent_task.notes!=doc.notes:
                    parent_task.notes=doc.notes
                    save =1
                if parent_task.subject!=doc.description:
                    parent_task.subject=doc.description
                    save =1
                if parent_task.subject1!=doc.subject:
                    parent_task.subject1=doc.subject
                    save =1
                if parent_task.assigned_to!=doc.assigned_to:
                    parent_task.assigned_to=doc.assigned_to
                    save =1
                if parent_task.expected_min!=doc.expected_min:
                    parent_task.expected_min=doc.expected_min
                    save =1
                if save == 1:
                    parent_task.save()
    if(actions == "after_insert"):
        doc.save()

              

def update_number(doc, actions):
        user(doc, doc.assigned_to)
        assigned = frappe.db.get_value("Task",doc.name,"assigned_to")
        if doc.assigned_to != assigned:
            user(doc, assigned)
        for i in doc.depends_on:
            if i.task:
                task_ = frappe.get_doc("Task",i.task)
                task_.update({
                        'description': strip_html_tags(i.subject or "") or "",   
                        'subject': i.subject1
                })
                task_.save()
        if len(doc.task_approval) !=0:
            for m in doc.task_approval:
                # if frappe.session.user == m.user:
                if m.status != "Approved":
                    if doc.status == "Completed":
                        frappe.throw("Task Approval Status is Pending")
            stat = 0
            for n in doc.task_approval:
                if n.status != "Approved":
                    stat = 1

                if stat == 0:
                    doc.status = "Completed"
                # else:
                #     doc.status = "Working"


@frappe.whitelist()
def juzgo_admin_users():
        admin_user = frappe.db.get_all("User", {'role_profile_name':"Juzgo Admin"},pluck="name")
        return admin_user

@frappe.whitelist()
def status_approval(name,task_approval):
    task_approval = json.loads(task_approval)
    status = frappe.get_value("Task Approval", {"parent": name,"user":task_approval["user"]}, 'status')
    return status

       

            
def user(doc, user):
    if user:
        priority_update = frappe.get_all("Task", filters={"status": ["in", ["Open", "Working","Overdue","Pending Review"]], 'assigned_to': user}, pluck='name',order_by = "priority_number")
        if doc.name not in priority_update:
            priority_update.insert(((doc.priority_number  -1) if doc.priority_number else len(priority_update)), doc.name)
            doc.priority_number =priority_update.index(doc.name)+1
        if user!= doc.assigned_to:
            try:
                priority_update.remove(doc.name)
            except:
                pass
        if doc.status not in ["Open", "Working","Overdue","Pending Review"]:
            try:
                priority_update.remove(doc.name)
            except:
                pass
            doc.priority_number =0
        if doc.name in priority_update:
            if not doc.priority_number:
                doc.priority_number = priority_update.index(doc.name)+1
            current = priority_update.pop(priority_update.index(doc.name))
            priority_update.insert(doc.priority_number -1, current)
        idx =1 
        for m in priority_update:
            frappe.db.set_value("Task",m,"priority_number",idx)
            idx+=1

def trash_task(doc, actions):
    priority_rearrange = frappe.get_all("Task", filters={"status": ["in", ["Open", "Working","Overdue","Pending Review"]], 'assigned_to': doc.assigned_to,'name':['not in',doc.name]}, pluck='name',order_by = "priority_number")
    idx =1 
    for n in priority_rearrange:
        frappe.db.set_value("Task",n,"priority_number",idx)
        idx+=1


def validate_minutes_to_hours(doc, actions):
    if doc.expected_min:
        minutes = float(doc.expected_min)
        hours = minutes / 60
        doc.expected_time = hours
    if doc.status == "Completed":
        doc.priority_number = 0


def validate_hours_to_minutes(doc, actions):
    if doc.expected_time:
        hours = float(doc.expected_time)
        minutes = hours * 60
        doc.expected_min = minutes
    
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
from frappe.utils import date_diff,getdate, now,nowdate, strip_html_tags
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
   

@frappe.whitelist()
def getdesc(task):
    if task:
        doc = frappe.get_doc("Task",task)
        return strip_html_tags(doc.get('description') or "")

@frappe.whitelist()
def update_data(subject=None,subject1=None,task=None,assigned_to=None,expected_min=None):
    if task:
        save = 0
        doc = frappe.get_doc("Task",task)
        if doc.description!=subject and subject:
            doc.description=subject
            save =1
        if doc.subject!=subject1 and subject1:
            doc.subject=subject1
            save =1
        if doc.assigned_to!=assigned_to:
            doc.assigned_to=assigned_to
            save =1
        if doc.expected_min!=expected_min:
            doc.expected_min=expected_min
            save =1
        if save == 1:
            doc.run_method=lambda *a,**b:0
            doc.save(ignore_permissions = True)


def autoname(doc, actions):
    if doc.abbr :
        if frappe.db.exists("Task", doc.abbr + "-" + doc.subject):
            doc.name = make_autoname(doc.abbr + "-" + doc.subject + "-.#")
    else:
        frappe.throw("Kindly Fill the Project Abbr in Project")

def on_trash(doc, actions):
    if doc.abbr and doc.subject:
        revert_series_if_last(doc.abbr + "-" + doc.subject+"-.#", doc.name)
    
# @frappe.whitelist()
def notification(to_user, from_user, task_name, data, doctype, field):
    doc=frappe.new_doc('Notification Log')
    doc.update({
    'subject': f'{from_user} added {field} in Task {task_name}: {data}',
    'for_user': to_user,
    'send_email': 1,
    'type': 'Alert',
    'document_type': doctype,
    'document_name': task_name,
    'from_user':from_user,
    'email_content': f'{data}'
    })
    doc.flags.ignore_permissions=True
    doc.save()

