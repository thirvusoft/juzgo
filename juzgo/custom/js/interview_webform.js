var questions = [];

function fill_question_fields () {
    let res = []
    questions.forEach(field => {
        res.push({
            question: field.label,
            answer: frappe.web_form.doc[field.fieldname] || ""
        });
    });
    frappe.web_form.doc["interview_questions"] = res
}

frappe.web_form.after_load = async () => {
    questions = []
    await frappe.call({
        method: "juzgo.custom.py.interview_webform.get_question_fields",
        args: {
            data: decodeURIComponent(window.location.hash?.substr(1))
        },callback(r) {
            r.message.forEach(field => {
                questions.push(field);
                frappe.web_form.make_section({});
                frappe.web_form.make_field(field, undefined, 1);
            });
        }
    });
    
    let save = frappe.web_form.save;
    function o_save () {
        fill_question_fields();
        save.call(frappe.web_form);
    }
    frappe.web_form.save = o_save
}
