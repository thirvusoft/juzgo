$(document).ready(function () {
    frappe.form.formatters['Attach'] = function(value, df) {
        if (!value)
            return ''
    let filename = value.substring(value.lastIndexOf("/") + 1);
    
    return filename || value
    }
    
    frappe.form.formatters['Attach Image'] = function(value, df) {
        if (!value)
            return ''
    let filename = value.substring(value.lastIndexOf("/") + 1);
    
    return filename || value
    }
}
