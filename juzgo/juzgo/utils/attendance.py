import frappe
from datetime import datetime, timedelta

def early_late_time(self,event):
    if self.in_time:
        shift = frappe.get_doc('Shift Type', self.shift)
        in_time_str = datetime.strptime(self.in_time, '%Y-%m-%d %H:%M:%S')
        start_time_str = str(shift.start_time)
        start_time_parts = start_time_str.split(':')
        hours, minutes, seconds = map(int, start_time_parts)
        shift_end_time = in_time_str.replace(hour=hours, minute=minutes, second=seconds)
        if in_time_str > shift_end_time:
            resulting_datetime = in_time_str - shift_end_time
            self.custom_late_by = resulting_datetime

    
    if self.out_time:
        shift = frappe.get_doc('Shift Type', self.shift)
        in_time_str = datetime.strptime(self.out_time, '%Y-%m-%d %H:%M:%S')
        start_time_str = str(shift.end_time)
        start_time_parts = start_time_str.split(':')
        hours, minutes, seconds = map(int, start_time_parts)
        shift_end_time = in_time_str.replace(hour=hours, minute=minutes, second=seconds)

        if in_time_str < shift_end_time:
            resulting_datetime = shift_end_time - in_time_str
            self.custom_early_by = resulting_datetime
