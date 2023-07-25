from frappe.desk.doctype.todo.todo import ToDo
from frappe.utils import get_fullname
import frappe
class toDo(ToDo):
	def validate(self):
		self._assignment = None
		if self.is_new():

			if self.assigned_by == self.allocated_to:
				assignment_message = frappe._("{0} self assigned this task: {1}").format(
					get_fullname(self.assigned_by), self.description
				)
			else:
				assignment_message = frappe._("{0} assigned {1}: {2}").format(
					get_fullname(self.assigned_by), get_fullname(self.allocated_to), self.description
				)

			self._assignment = {"text": assignment_message, "comment_type": "Assigned"}