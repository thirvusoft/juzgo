frappe.form.formatters['Attach'] = function(value, df) {
    if (!value)
        return ''
let filename = value.substring(value.lastIndexOf("/") + 1);

return filename || value
}
