frappe.ui.form.on('Reference Table', {
	open_url: function(frm,cdt,cdn){
        let row = locals[cdt][cdn]
        if(!row.url){
            frappe.throw('Enter URL in Row '+row.idx+' .')
        }
        else{
        window.open(row.url, '_blank')
        }
    },
})
frappe.ui.form.on('R and D Attachment', {
	open_url: function(frm,cdt,cdn){
        let row = locals[cdt][cdn]
        if(!row.url){
            frappe.throw('Enter URL in Row '+row.idx+' .')
        }
        else{
        window.open(row.url, '_blank')
        }
    },
})