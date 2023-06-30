from . import __version__ as app_version

app_name = "juzgo"
app_title = "Juzgo"
app_publisher = "Thirvusoft Pvt Limited"
app_description = "The world is a book and those who do not travel read only One page"
app_email = "thirvusoft@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/juzgo/css/juzgo.css"
# app_include_js = "/assets/juzgo/js/juzgo.js"

# include js, css files in header of web template
# web_include_css = "/assets/juzgo/css/juzgo.css"
web_include_js = ["juzgo.bundle.js"]

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "juzgo/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
		"Timesheet" : "/juzgo/custom/js/timesheet.js",
        "Interview Feedback": "/custom/js/interview_feedback.js",
        "Interview Round": "/juzgo/custom/js/interview_round.js",
		"Interview": "/custom/js/interview.js",
        "Task" : "/juzgo/custom/js/task.js",
		"Job Opening" : "/juzgo/custom/js/jobopening.js",
        "Project" : "/juzgo/custom/js/project.js",
  
    "Employee" : "/juzgo/custom/js/employee.js",


		"Customer" : "/juzgo/custom/js/customer.js"

	}
doc_events = {
    "Task" : {
        "validate" : ["juzgo.juzgo.custom.py.task.user_todo",
                      "juzgo.juzgo.custom.py.task.update_number",
                      "juzgo.juzgo.custom.py.task.validate_minutes_to_hours",
                      "juzgo.juzgo.custom.py.task.validate_hours_to_minutes",
					  
                      
					  ],
        "after_insert" : "juzgo.juzgo.custom.py.task.user_todo",
        "on_trash" : "juzgo.juzgo.custom.py.task.trash_task",
        "autoname": "juzgo.juzgo.custom.py.task.autoname",
        "on_trash": "juzgo.juzgo.custom.py.task.on_trash"
	},
    "Interview Feedback":{
        "validate" : "juzgo.custom.py.interview_feedback.validate",
	},
	"Timesheet": {
		"validate": [
			"juzgo.juzgo.custom.py.timesheet.status_updated",
					"juzgo.juzgo.custom.py.timesheet.get_notes"
			   	]
	},
    "Interview": {
        "validate": "juzgo.custom.py.interview.get_url",
        "after_insert" : "juzgo.juzgo.custom.py.interview.send_mail_interview_created",
        "on_submit": "juzgo.juzgo.custom.py.interview.send_interview_round_status"
	},
    "Customer":{
        "validate": "juzgo.juzgo.custom.py.customer.validate"
	}

}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "juzgo.utils.jinja_methods",
#	"filters": "juzgo.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "juzgo.install.before_install"
# after_install = "juzgo.install.after_install"

# Migrate
# ------------

after_migrate = "juzgo.juzgo.utils.setup.setup"

# Uninstallation
# ------------

# before_uninstall = "juzgo.uninstall.before_uninstall"
# after_uninstall = "juzgo.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "juzgo.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Timesheet": "juzgo.juzgo.custom.py.timesheet.time_sheet"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"juzgo.tasks.all"
	# ],
	"daily": [
		"juzgo.juzgo.custom.py.task.overdue_days"
	],
	# "hourly": [
	# 	"juzgo.tasks.hourly"
	# ],
	# "weekly": [
	# 	"juzgo.tasks.weekly"
	# ],
	# "monthly": [
	# 	"juzgo.tasks.monthly"
	# ],
}

# Testing
# -------

# before_tests = "juzgo.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"hrms.hr.doctype.job_applicant.job_applicant.create_interview": "juzgo.juzgo.custom.py.interview.create_interview",
    "frappe.desk.doctype.notification_log.notification_log.get_notification_logs": "juzgo.juzgo.custom.py.notification_log.get_notification_logs"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
override_doctype_dashboards = {
	"Interview": "juzgo.custom.py.dashboards.interview.get_data"
}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["juzgo.utils.before_request"]
# after_request = ["juzgo.utils.after_request"]

# Job Events
# ----------
# before_job = ["juzgo.utils.before_job"]
# after_job = ["juzgo.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"juzgo.auth.validate"
# ]
