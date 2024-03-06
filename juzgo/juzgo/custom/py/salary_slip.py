
import frappe

@frappe.whitelist()
def get_last_from_date(employee=None, salary_structure=None, posting_date=None):
    last_salary_assignment = frappe.get_list(
        'Salary Structure Assignment',
        filters={
            'employee': employee,
            'salary_structure': salary_structure,
            'from_date': ('<', posting_date)
        },
        fields=['base', 'from_date'],
        order_by='from_date DESC',
        limit=1
    )

    return last_salary_assignment[0] if last_salary_assignment else None
