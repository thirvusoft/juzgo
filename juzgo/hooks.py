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
# web_include_js = "/assets/juzgo/js/juzgo.js"

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
        "Task" : "/juzgo/custom/js/task.js",
		# "Staffing Plan" : "/juzgo/custom/js/staffplanning.js",
		"Job Opening" : "/juzgo/custom/js/jobopening.js"

	}
doc_events = {
    "Task" : {
        "validate" : ["juzgo.juzgo.custom.py.task.user_todo",
                      "juzgo.juzgo.custom.py.task.update_number",
                      
					  ],
        "after_insert" : "juzgo.juzgo.custom.py.task.user_todo",
        # "on_update" : "juzgo.juzgo.custom.py.task.on_update"
	},
	"Timesheet": {
		"validate": "juzgo.juzgo.custom.py.timesheet.status_updated",
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

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

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

# scheduler_events = {
#	"all": [
#		"juzgo.tasks.all"
#	],
#	"daily": [
#		"juzgo.tasks.daily"
#	],
#	"hourly": [
#		"juzgo.tasks.hourly"
#	],
#	"weekly": [
#		"juzgo.tasks.weekly"
#	],
#	"monthly": [
#		"juzgo.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "juzgo.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "juzgo.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "juzgo.task.get_dashboard_data"
# }

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
