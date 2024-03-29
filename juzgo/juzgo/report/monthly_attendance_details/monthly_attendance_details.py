# Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt


from datetime import datetime, timedelta
from calendar import monthrange
import datetime
from itertools import groupby
from typing import Dict, List, Optional, Tuple

import frappe
from frappe import _
from frappe.query_builder.functions import Count, Extract, Sum
from frappe.utils import cint, cstr, getdate

Filters = frappe._dict

status_map = {
	"Present": "P",
	"Absent": "A",
	"Half Day": "HD",
	"Work From Home": "WFH",
	"On Leave": "L",
	"Holiday": "H",
	"Weekly Off": "WO",
}

day_abbr = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def execute(filters: Optional[Filters] = None) -> Tuple:
	filters = frappe._dict(filters or {})

	if not (filters.month and filters.year):
		frappe.throw(_("Please select month and year."))

	attendance_map = get_attendance_map(filters)

	if not attendance_map:
		frappe.msgprint(_("No attendance records found."), alert=True, indicator="orange")
		return [], [], None, None

	columns = get_columns(filters)
	data = get_data(filters, attendance_map)

	if not data:
		frappe.msgprint(
			_("No attendance records found for this criteria."), alert=True, indicator="orange"
		)
		return columns, [], None, None

	message = get_message() if not filters.summarized_view else ""
	chart = get_chart_data(attendance_map, filters)

	return columns, data, message, None


def get_message() -> str:
	message = ""
	colors = ["green", "red", "orange", "green", "#318AD8", "", ""]

	count = 0
	for status, abbr in status_map.items():
		message += f"""
			<span style='border-left: 2px solid {colors[count]}; padding-right: 12px; padding-left: 5px; margin-right: 3px;'>
				{status} - {abbr}
			</span>
		"""
		count += 1
	message += f"""<br> <span style='border-left: 2px solid red; padding-right: 12px; padding-left: 5px; margin-right: 3px;'>
					 Less Than 5 Hours - <b style="color: red;">Absent</b></span>
     			<span style='border-left: 2px solid orange; padding-right: 12px; padding-left: 5px; margin-right: 3px;'>
				 Between 5 to 6 Hours - <b style="color: orange;">Half Day</b></span>
				<span style='border-left: 2px solid green; padding-right: 12px; padding-left: 5px; margin-right: 3px;'>
				 Greater Than 6 Hours - <b style="color: green;">Present</b></span>
			 """

	return message


def get_columns(filters: Filters) -> List[Dict]:
	columns = []

	if filters.group_by:
		columns.append(
			{
				"label": _(filters.group_by),
				"fieldname": frappe.scrub(filters.group_by),
				"fieldtype": "Link",
				"options": "Branch",
				"width": 120,
			}
		)

	columns.extend(
		[
			{
				"label": _("Employee"),
				"fieldname": "employee",
				"fieldtype": "Link",
				"options": "Employee",
				"width": 135,
			},
			{"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 120},
		]
	)

	# columns.extend(
	# 	[
	# 		{
	# 			"label": _("Total Present"),
	# 			"fieldname": "total_present",
	# 			"fieldtype": "Float",
	# 			"width": 110,
	# 		},
	# 		{"label": _("Total Leaves"), "fieldname": "total_leaves", "fieldtype": "Float", "width": 110},
	# 		{"label": _("Total Absent"), "fieldname": "total_absent", "fieldtype": "Float", "width": 110},
	# 		{
	# 			"label": _("Total Holidays"),
	# 			"fieldname": "total_holidays",
	# 			"fieldtype": "Float",
	# 			"width": 120,
	# 		},
	# 		{
	# 			"label": _("Unmarked Days"),
	# 			"fieldname": "unmarked_days",
	# 			"fieldtype": "Float",
	# 			"width": 130,
	# 		},
	# 	]
	# )
	# columns.extend(get_columns_for_leave_types())
	# columns.extend(
	# 	[
	# 		{
	# 			"label": _("Total Late Entries"),
	# 			"fieldname": "total_late_entries",
	# 			"fieldtype": "Float",
	# 			"width": 140,
	# 		},
	# 		{
	# 			"label": _("Total Early Exits"),
	# 			"fieldname": "total_early_exits",
	# 			"fieldtype": "Float",
	# 			"width": 140,
	# 		},
	# 	]
	# )
	columns.append({"label": _("Shift"), "fieldname": "shift", "fieldtype": "Data", "width": 130})
	columns.extend(get_columns_for_days(filters))

	return columns


def get_columns_for_leave_types() -> List[Dict]:
	leave_types = frappe.db.get_all("Leave Type", pluck="name")
	types = []
	for entry in leave_types:
		types.append(
			{"": entry,}
		)
	

	return types


def get_columns_for_days(filters: Filters) -> List[Dict]:
	total_days = get_total_days_in_month(filters)
	days = []

	for day in range(1, total_days + 1):
		# forms the dates from selected year and month from filters
		date = "{}-{}-{}".format(cstr(filters.year), cstr(filters.month), cstr(day))
		# gets abbr from weekday number
		weekday = day_abbr[getdate(date).weekday()]
		# sets days as 1 Mon, 2 Tue, 3 Wed
		label = "{} {}".format(cstr(day), weekday)
		days.append({"label": label, "fieldtype": "Data", "fieldname": day, "width": 100})

	return days


def get_total_days_in_month(filters: Filters) -> int:
	return monthrange(cint(filters.year), cint(filters.month))[1]


def get_data(filters: Filters, attendance_map: Dict) -> List[Dict]:
	employee_details, group_by_param_values = get_employee_related_details(filters)
	holiday_map = get_holiday_map(filters)
	data = []


	if filters.group_by:
		group_by_column = frappe.scrub(filters.group_by)

		for value in group_by_param_values:
			if not value:
				continue

			records = get_rows(employee_details[value], filters, holiday_map, attendance_map)


			if records:
				data.append({group_by_column: frappe.bold(value)})
				data.extend(records)
	else:

		data = get_rows(employee_details, filters, holiday_map, attendance_map)
	return data


def get_attendance_map(filters: Filters) -> Dict:
	"""Returns a dictionary of employee wise attendance map as per shifts for all the days of the month like
	{
	    'employee1': {
	            'Morning Shift': {1: 'Present', 2: 'Absent', ...}
	            'Evening Shift': {1: 'Absent', 2: 'Present', ...}
	    },
	    'employee2': {
	            'Afternoon Shift': {1: 'Present', 2: 'Absent', ...}
	            'Night Shift': {1: 'Absent', 2: 'Absent', ...}
	    },
	    'employee3': {
	            None: {1: 'On Leave'}
	    }
	}
	"""
	attendance_list = get_attendance_records(filters)

	attendance_map = {}
	leave_map = {}


	for d in attendance_list:

		if d.status == "On Leave":
			leave_map.setdefault(d.employee, []).append(d.day_of_month)
			continue
		hours = int(d.working_hours)
		minutes = int((d.working_hours - hours) * 60)

		logged_time = datetime.time(hours, minutes)

		formatted_time = logged_time.strftime('%H:%M')
		attendance_map.setdefault(d.employee, {}).setdefault(d.shift, {}).setdefault(d.day_of_month, {})
		attendance_map[d.employee][d.shift][d.day_of_month]['status'] = d.status
		attendance_map[d.employee][d.shift][d.day_of_month]['in_time'] = d.in_time
		attendance_map[d.employee][d.shift][d.day_of_month]['out_time'] = d.out_time
		attendance_map[d.employee][d.shift][d.day_of_month]['logged_hours'] = logged_time

		attendance_map[d.employee][d.shift][d.day_of_month]['late_by_row'] = d.custom_late_by
		attendance_map[d.employee][d.shift][d.day_of_month]['early_by_row'] = d.custom_early_by
		
		timing=frappe.get_doc("Shift Type",d.shift)
		if d.working_hours:
			shifttime=timing.end_time-timing.start_time
			shifttime = shifttime.total_seconds()/3600
			diff=d.working_hours-shifttime
			if diff>0:
				attendance_map[d.employee][d.shift][d.day_of_month]['overtime'] = datetime.timedelta(seconds=diff*3600) or 0
			elif diff<0:
				attendance_map[d.employee][d.shift][d.day_of_month]['undertime'] = datetime.timedelta(seconds=-1*diff*3600) or 0


	# leave is applicable for the entire day so all shifts should show the leave entry
	for employee, leave_days in leave_map.items():
		# no attendance records exist except leaves
		if employee not in attendance_map:
			attendance_map.setdefault(employee, {}).setdefault(None, {})

		for day in leave_days:
			for shift in attendance_map[employee].keys():
				attendance_map[employee][shift][day] ={"status": "On Leave"}

	return attendance_map


def get_attendance_records(filters: Filters) -> List[Dict]:
	Attendance = frappe.qb.DocType("Attendance")
	query = (
		frappe.qb.from_(Attendance)
		.select(
			Attendance.employee,
			Extract("day", Attendance.attendance_date).as_("day_of_month"),
			Attendance.status,
			Attendance.shift,
			Attendance.in_time,
			Attendance.out_time,
			Attendance.working_hours,
			Attendance.custom_late_by,
			Attendance.custom_early_by,
			

		)
		.where(
			(Attendance.docstatus == 1)
			& (Attendance.company == filters.company)
			& (Extract("month", Attendance.attendance_date) == filters.month)
			& (Extract("year", Attendance.attendance_date) == filters.year)
		)
	)

	if filters.employee:
		query = query.where(Attendance.employee == filters.employee)
	query = query.orderby(Attendance.employee, Attendance.attendance_date)

	return query.run(as_dict=1)


def get_employee_related_details(filters: Filters) -> Tuple[Dict, List]:
	"""Returns
	1. nested dict for employee details
	2. list of values for the group by filter
	"""
	Employee = frappe.qb.DocType("Employee")
	query = (
		frappe.qb.from_(Employee)
		.select(
			Employee.name,
			Employee.employee_name,
			Employee.designation,
			Employee.grade,
			Employee.department,
			Employee.branch,
			Employee.company,
			Employee.holiday_list,
		)
		.where(Employee.company == filters.company)
	)

	if filters.employee:
		query = query.where(Employee.name == filters.employee)

	group_by = filters.group_by
	if group_by:
		group_by = group_by.lower()
		query = query.orderby(group_by)

	employee_details = query.run(as_dict=True)
	group_by_param_values = []
	emp_map = {}

	if group_by:
		for parameter, employees in groupby(employee_details, key=lambda d: d[group_by]):
			group_by_param_values.append(parameter)
			emp_map.setdefault(parameter, frappe._dict())

			for emp in employees:
				emp_map[parameter][emp.name] = emp
	else:
		for emp in employee_details:
			emp_map[emp.name] = emp

	return emp_map, group_by_param_values


def get_holiday_map(filters: Filters) -> Dict[str, List[Dict]]:
	"""
	Returns a dict of holidays falling in the filter month and year
	with list name as key and list of holidays as values like
	{
	        'Holiday List 1': [
	                {'day_of_month': '0' , 'weekly_off': 1},
	                {'day_of_month': '1', 'weekly_off': 0}
	        ],
	        'Holiday List 2': [
	                {'day_of_month': '0' , 'weekly_off': 1},
	                {'day_of_month': '1', 'weekly_off': 0}
	        ]
	}
	"""
	# add default holiday list too
	holiday_lists = frappe.db.get_all("Holiday List", pluck="name")
	default_holiday_list = frappe.get_cached_value("Company", filters.company, "default_holiday_list")
	holiday_lists.append(default_holiday_list)

	holiday_map = frappe._dict()
	Holiday = frappe.qb.DocType("Holiday")

	for d in holiday_lists:
		if not d:
			continue

		holidays = (
			frappe.qb.from_(Holiday)
			.select(Extract("day", Holiday.holiday_date).as_("day_of_month"), Holiday.weekly_off)
			.where(
				(Holiday.parent == d)
				& (Extract("month", Holiday.holiday_date) == filters.month)
				& (Extract("year", Holiday.holiday_date) == filters.year)
			)
		).run(as_dict=True)

		holiday_map.setdefault(d, holidays)

	return holiday_map

def get_rows(
	employee_details: Dict, filters: Filters, holiday_map: Dict, attendance_map: Dict
) -> List[Dict]:
	get_columns_for_leave_types()
	records = []
	row={}
	row1={}
	row2={}
	default_holiday_list = frappe.get_cached_value("Company", filters.company, "default_holiday_list")

	for employee, details in employee_details.items():
		emp_holiday_list = details.holiday_list or default_holiday_list
		holidays = holiday_map.get(emp_holiday_list)


		attendance = get_attendance_status_for_summarized_view(employee, filters, holidays)
		if not attendance:
			continue

		leave_summary = get_leave_summary(employee, filters)
		entry_exits_summary = get_entry_exits_summary(employee, filters)

		# row = {"employee": employee, "employee_name": details.employee_name,"indent":0}
		set_defaults_for_summarized_view(filters, row)
		row1={"shift":"<b style=color:red>Total Late by Count</b>","2":"<b <b style=color:red>Total Early by Count</b>",'indent':1}
		row2={'indent':1}

		row.update(attendance)
		row2.update(leave_summary)
		row1.update(entry_exits_summary)


		employee_attendance = attendance_map.get(employee)
		if not employee_attendance:
			continue

		attendance_for_employee = get_attendance_status_for_detailed_view(
			employee, filters, employee_attendance, holidays
		)
		# set employee details in the first row
		attendance_for_employee[0].update(
			{"employee": employee, "employee_name": details.employee_name}
		)

		records += attendance_for_employee
		records.append(row.copy())
		records.append(row1)
		records.append(row2)

	return records


def set_defaults_for_summarized_view(filters, row):
	for entry in get_columns(filters):
		if entry.get("fieldtype") == "Float":
			row[entry.get("fieldname")] = 0.0


def get_attendance_status_for_summarized_view(
	employee: str, filters: Filters, holidays: List
) -> Dict:
	"""Returns dict of attendance status for employee like
	{'total_present': 1.5, 'total_leaves': 0.5, 'total_absent': 13.5, 'total_holidays': 8, 'unmarked_days': 5}
	"""
	summary, attendance_days = get_attendance_summary_and_days(employee, filters)
	if not any(summary.values()):
		return {}

	total_days = get_total_days_in_month(filters)
	total_holidays = total_unmarked_days = 0

	for day in range(1, total_days + 1):
		if day in attendance_days:
			continue

		status = get_holiday_status(day, holidays)
		if status in ["Weekly Off", "Holiday"]:
			total_holidays += 1
		elif not status:
			total_unmarked_days += 1

	return {
		"shift":"<b style=color:green>Total Present</b>",
		"1": f"<b style= color:green>{summary.total_present + summary.total_half_days} </b>",
		"2":"<b style=color:green>Present Hrs</b>",
		"3": f"<b style= color:green>{(summary.total_present + summary.total_half_days)*8}/{(total_days-total_holidays)*8} </b>",
		"4":"<b style=color:green>Payment Days</b>",
		"5": f"<b style= color:green>{summary.total_present + summary.total_half_days + total_holidays} </b>",
		"6":"<b style=color:red>Total Leaves</b>",
		"7": f"<b style = color:red>{summary.total_leaves + summary.total_half_days}</b>",
		"8":"<b style=color:red>Total Absent</b>",
		"9": f"<b style = color:red>{summary.total_absent}</b>",
		"10":"<b style=color:red>Total Holidays</b>",
		"11": f"<b style = color:red>{total_holidays}</b>",
		"12":"<b style=color:orange>Unmarked Days</b>",
		"13": f"<b style = color:orange>{total_unmarked_days}</b>",
		"indent":1,
	}


def get_attendance_summary_and_days(employee: str, filters: Filters) -> Tuple[Dict, List]:
	Attendance = frappe.qb.DocType("Attendance")

	present_case = (
		frappe.qb.terms.Case()
		.when(((Attendance.status == "Present") | (Attendance.status == "Work From Home")), 1)
		.else_(0)
	)
	sum_present = Sum(present_case).as_("total_present")

	absent_case = frappe.qb.terms.Case().when(Attendance.status == "Absent", 1).else_(0)
	sum_absent = Sum(absent_case).as_("total_absent")

	leave_case = frappe.qb.terms.Case().when(Attendance.status == "On Leave", 1).else_(0)
	sum_leave = Sum(leave_case).as_("total_leaves")

	half_day_case = frappe.qb.terms.Case().when(Attendance.status == "Half Day", 0.5).else_(0)
	sum_half_day = Sum(half_day_case).as_("total_half_days")

	summary = (
		frappe.qb.from_(Attendance)
		.select(
			sum_present,
			sum_absent,
			sum_leave,
			sum_half_day,
		)
		.where(
			(Attendance.docstatus == 1)
			& (Attendance.employee == employee)
			& (Attendance.company == filters.company)
			& (Extract("month", Attendance.attendance_date) == filters.month)
			& (Extract("year", Attendance.attendance_date) == filters.year)
		)
	).run(as_dict=True)

	days = (
		frappe.qb.from_(Attendance)
		.select(Extract("day", Attendance.attendance_date).as_("day_of_month"))
		.distinct()
		.where(
			(Attendance.docstatus == 1)
			& (Attendance.employee == employee)
			& (Attendance.company == filters.company)
			& (Extract("month", Attendance.attendance_date) == filters.month)
			& (Extract("year", Attendance.attendance_date) == filters.year)
		)
	).run(pluck=True)

	return summary[0], days


def get_attendance_status_for_detailed_view(
	employee: str, filters: Filters, employee_attendance: Dict, holidays: List
) -> List[Dict]:
	"""Returns list of shift-wise attendance status for employee
	[
	        {'shift': 'Morning Shift', 1: 'A', 2: 'P', 3: 'A'....},
	        {'shift': 'Evening Shift', 1: 'P', 2: 'A', 3: 'P'....}
	]
	"""
	total_days = get_total_days_in_month(filters)
	attendance_values = []
	zero_duration = timedelta(hours=0, minutes=0, seconds=0)
	time1 = timedelta(hours=0, minutes=0, seconds=0)
	timeunder = timedelta(hours=0, minutes=0, seconds=0)
	timeunder = timedelta(hours=0, minutes=0, seconds=0)
	tot_logged_hrs =  datetime.time(0, 0)

	early = timedelta()
	late = timedelta()

	for shift, status_dict in employee_attendance.items():

		row = {"shift": shift}
		in_time_row = {'shift': '<b>In Time</b>','indent':1}
		out_time_row = {'shift': '<b>Out Time</b>','indent':1}
		late_by_row = {'shift': '<b>Late By</b>','indent':1}
		early_by_row = {'shift': '<b>Early By</b>','indent':1}
		overtime = {'shift': '<b>Overtime</b>','indent':1}
		undertime = {'shift': '<b>Undertime</b>','indent':1}
		logged_hours = {'shift': '<b>Logged Hours</b>','indent':1}
		tot_overtime={}
		tot_undertime={}
		for day in range(1, total_days + 1):
			status = (status_dict.get(day) or {}).get('status')
			if status is None and holidays:
				status = get_holiday_status(day, holidays)

			abbr = status_map.get(status, "")
			row[day] = abbr
			in_time_row[day] = str((date_time.time()) if (type(date_time:=((status_dict.get(day) or {}).get('in_time'))) == datetime.datetime) else date_time or '')
			out_time_row[day] = str((date_time.time()) if (type(date_time:=((status_dict.get(day) or {}).get('out_time'))) == datetime.datetime) else date_time or '')
			logged_hours[day] = (status_dict.get(day) or {}).get('logged_hours')
			overtime[day] = (status_dict.get(day) or {}).get('overtime')  
			undertime[day] = (status_dict.get(day) or {}).get('undertime') 
			late_by_row[day] = (status_dict.get(day) or {}).get('late_by_row') or ''
			early_by_row[day] = (status_dict.get(day) or {}).get('early_by_row') or ''

			tot_overtime[day] = (status_dict.get(day) or {}).get('overtime')  or zero_duration
			tot_undertime[day] = (status_dict.get(day) or {}).get('undertime') or zero_duration

			time1+=tot_overtime[day]
			timeunder+=tot_undertime[day]

			late_by_str = (status_dict.get(day) or {}).get('late_by_row') or '0:0:0'
			if isinstance(late_by_str, str):
				late_by_row_day = timedelta(hours=int(late_by_str.split(':')[0]),
											minutes=int(late_by_str.split(':')[1]),
											seconds=int(late_by_str.split(':')[2]))
			elif isinstance(late_by_str, timedelta):
				late_by_row_day = late_by_str
			else:
				late_by_row_day = timedelta()  # Default to zero time if not a valid format

			# Convert early_by_row[day] to timedelta
			early_by_str = (status_dict.get(day) or {}).get('early_by_row') or '0:0:0'
			if isinstance(early_by_str, str):
				early_by_row_day = timedelta(hours=int(early_by_str.split(':')[0]),
											minutes=int(early_by_str.split(':')[1]),
											seconds=int(early_by_str.split(':')[2]))
			elif isinstance(early_by_str, timedelta):
				early_by_row_day = early_by_str
			else:
				early_by_row_day = timedelta()  # Default to zero time if not a valid format

			# Add timedelta values to late and early
			late += late_by_row_day
			early += early_by_row_day

		value_time =(time1.total_seconds()/3600)-(timeunder.total_seconds()/3600)
		nav = ""
		if value_time>=0:
				value_time = datetime.timedelta(seconds=value_time*3600) 
		elif value_time<0:
				value_time = datetime.timedelta(seconds=-1*value_time*3600) 
				nav = "-"


		time1=time1.total_seconds()
		hours = time1 // 3600
		time1 %= 3600
		minutes = time1 // 60
		seconds = time1 % 60
		time1=(f"{int(hours)}:{int(minutes)}:{int(seconds)}")


		timeunder=timeunder.total_seconds()
		hours = timeunder // 3600
		timeunder %= 3600
		minutes = timeunder // 60
		seconds = timeunder % 60
		timeunder=(f"{int(hours)}:{int(minutes)}:{int(seconds)}")

		value_time=value_time.total_seconds()
		hours = value_time // 3600
		value_time %= 3600
		minutes = value_time // 60
		seconds = value_time % 60
		value_time=(f"{int(hours)}:{int(minutes)}:{int(seconds)}")

		from datetime import time
		total_hours = 0
		total_minutes = 0

		for key, value in logged_hours.items():
			if isinstance(value, time):
				total_hours += value.hour
				total_minutes += value.minute

		# Convert excess minutes to hours if necessary
		total_hours += total_minutes // 60
		total_minutes %= 60

		total_over={"shift":"<b style=color:blue>Total Overtime hrs</b>",'1':f'<b style=color:#6A5ACD>{time1}</b>','2':"<b style=color:blue>Total Undertime hrs</b>","3":f'<b style=color:#6A5ACD>{timeunder}</b>',"4":"<b style=color:blue>Total Time</b>","5":f'<b style=color:#6A5ACD>{nav}{value_time}</b>',"indent":1}
		total_early={"shift":"<b style=color:blue>Total Late by hrs</b>",'1':f'<b style=color:#6A5ACD>{late}</b>','2':"<b style=color:blue>Total Early by hrs</b>","3":f'<b style=color:#6A5ACD>{early}</b>',"4":f"<b style=color:blue>Total Logged Hrs</b>","5": f"<b style=color:#6A5ACD>{total_hours}hrs {total_minutes}mins</b>","indent":1}

		attendance_values.append(row)
		attendance_values.append(in_time_row)
		attendance_values.append(out_time_row)
		attendance_values.append(late_by_row)
		attendance_values.append(early_by_row)
		attendance_values.append(overtime)
		attendance_values.append(undertime)
		attendance_values.append(logged_hours)
		attendance_values.append(total_over)
		attendance_values.append(total_early)

	
		

	return attendance_values


def get_holiday_status(day: int, holidays: List) -> str:
	status = None
	if holidays:
		for holiday in holidays:
			if day == holiday.get("day_of_month"):
				if holiday.get("weekly_off"):
					status = "Weekly Off"
				else:
					status = "Holiday"
				break
	return status


def get_leave_summary(employee: str, filters: Filters) -> Dict[str, float]:
	"""Returns a dict of leave type and corresponding leaves taken by employee like:
	{'leave_without_pay': 1.0, 'sick_leave': 2.0}
	"""
	Attendance = frappe.qb.DocType("Attendance")
	day_case = frappe.qb.terms.Case().when(Attendance.status == "Half Day", 0.5).else_(1)
	sum_leave_days = Sum(day_case).as_("leave_days")
	leave_details = (
		frappe.qb.from_(Attendance)
		.select(Attendance.leave_type, sum_leave_days)
		.where(
			(Attendance.employee == employee)
			& (Attendance.docstatus == 1)
			& (Attendance.company == filters.company)
			& ((Attendance.leave_type.isnotnull()) | (Attendance.leave_type != ""))
			& (Extract("month", Attendance.attendance_date) == filters.month)
			& (Extract("year", Attendance.attendance_date) == filters.year)
		)
		.groupby(Attendance.leave_type)
	).run(as_dict=True)

	leaves = {}
	index = 1

	for d in leave_details:
		if index == 1:
			leaves['shift'] = f"<b>{d.leave_type}</b>"
		else:
			leaves[str(index)] =f"<b>{d.leave_type}</b>"

		index += 1
		leaves[str(index)] = d.leave_days
		index += 1
	return leaves


def get_entry_exits_summary(employee: str, filters: Filters) -> Dict[str, float]:
	"""Returns total late entries and total early exits for employee like:
	{'total_late_entries': 5, 'total_early_exits': 2}
	"""
	Attendance = frappe.qb.DocType("Attendance")

	late_entry_case = frappe.qb.terms.Case().when(Attendance.late_entry == "1", "1")
	count_late_entries = Count(late_entry_case).as_("1")

	early_exit_case = frappe.qb.terms.Case().when(Attendance.early_exit == "1", "1")
	count_early_exits = Count(early_exit_case).as_("3")

	entry_exits = (
		frappe.qb.from_(Attendance)
		.select(count_late_entries, count_early_exits)
		.where(
			(Attendance.docstatus == 1)
			& (Attendance.employee == employee)
			& (Attendance.company == filters.company)
			& (Extract("month", Attendance.attendance_date) == filters.month)
			& (Extract("year", Attendance.attendance_date) == filters.year)
		)
	).run(as_dict=True)


	return entry_exits[0]






@frappe.whitelist()
def get_attendance_years() -> str:
	"""Returns all the years for which attendance records exist"""
	Attendance = frappe.qb.DocType("Attendance")
	year_list = (
		frappe.qb.from_(Attendance)
		.select(Extract("year", Attendance.attendance_date).as_("year"))
		.distinct()
	).run(as_dict=True)

	if year_list:
		year_list.sort(key=lambda d: d.year, reverse=True)
	else:
		year_list = [frappe._dict({"year": getdate().year})]

	return "\n".join(cstr(entry.year) for entry in year_list)


def get_chart_data(attendance_map: Dict, filters: Filters) -> Dict:
	days = get_columns_for_days(filters)
	labels = []
	absent = []
	present = []
	leave = []


	for day in days:
		labels.append(day["label"])
		total_absent_on_day = total_leaves_on_day = total_present_on_day = 0

		for employee, attendance_dict in attendance_map.items():
			for shift, attendance in attendance_dict.items():
				attendance_on_day = attendance.get(day["fieldname"])

				if attendance_on_day == "On Leave":
					# leave should be counted only once for the entire day
					total_leaves_on_day += 1
					break
				elif attendance_on_day == "Absent":
					total_absent_on_day += 1
				elif attendance_on_day in ["Present", "Work From Home"]:
					total_present_on_day += 1
				elif attendance_on_day == "Half Day":
					total_present_on_day += 0.5
					total_leaves_on_day += 0.5

		absent.append(total_absent_on_day)
		present.append(total_present_on_day)
		leave.append(total_leaves_on_day)

	return {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": "Absent", "values": absent},
				{"name": "Present", "values": present},
				{"name": "Leave", "values": leave},
			],
		},
		"type": "line",
		"colors": ["red", "green", "blue"],
	}
