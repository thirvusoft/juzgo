frappe.ready(async function () {
	await frappe.call({
		method: "juzgo.juzgo.web_form.employment_form.employment_form.get_designation",
		callback: function (r) {
			frappe.web_form.fields_dict.job_title._data = r.message || []
		}
	});
})