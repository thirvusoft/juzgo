import frappe
from frappe.utils import cint, get_datetime, get_time, getdate
from hrms.hr.doctype.shift_type.shift_type import ShiftType

def thirvusoft_process_auto_attendance_shift1():
    shift_list = frappe.get_all("Shift Type", filters={"enable_auto_attendance": "1"}, pluck="name")
    for shift in shift_list:
        doc = frappe.get_cached_doc("Shift Type", shift)
        doc.last_sync_of_checkin=get_datetime()
        doc.save()
        doc.process_auto_attendance()