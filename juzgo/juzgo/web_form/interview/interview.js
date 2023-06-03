function setuppages() {
    $(document.getElementsByClassName("page_content")).append(frappe.render_template("error"));
    $(document.getElementsByClassName("page_content")).append(frappe.render_template("already_responded"));
}


frappe.ready(function () {
    setuppages()
    frappe.web_form.questions = [];
    function fill_question_fields() {
        let grid_is_editable = frappe.web_form.fields_dict.interview_reponse_question_tab.grid.is_editable;
        frappe.web_form.fields_dict.interview_reponse_question_tab.grid.is_editable = () => 1;

        frappe.web_form.fields_dict.interview_reponse_question_tab.grid.data = [];
        frappe.web_form.questions.forEach(field => {
            frappe.web_form.fields_dict.interview_reponse_question_tab.grid.add_new_row()
            let idx = frappe.web_form.fields_dict.interview_reponse_question_tab.grid.data.length - 1;
            frappe.web_form.fields_dict.interview_reponse_question_tab.grid.data[idx]['question'] = field.label || "";
            frappe.web_form.fields_dict.interview_reponse_question_tab.grid.data[idx]['answer'] = frappe.web_form.doc[field.fieldname] || "";
        });

        frappe.web_form.fields_dict.interview_reponse_question_tab.grid.is_editable = grid_is_editable;
    }

    let save = frappe.web_form.save;
    function o_save() {
        fill_question_fields();
        save.call(frappe.web_form);
    }
    frappe.web_form.save = o_save

    frappe.web_form.errorWebform = () => {
        $(".web-form-container").hide();
        $(".success-page").hide();
        $(".form-not-opened-page").hide();
        $(".already-responded-page").hide();
        $(".error-page").removeClass("hide");
    }

    frappe.web_form.alreadyRespondedWebform = () => {
        $(".web-form-container").hide();
        $(".success-page").hide();
        $(".form-not-opened-page").hide();
        $(".error-page").hide();
        $(".already-responded-page").removeClass("hide")
    }

    frappe.web_form.formNotOpened = (form_opening_date, form_closing_date, form_opening_time, form_closing_time) => {
        let data = {
            form_opening_date: form_opening_date,
            form_closing_date: form_closing_date,
            form_opening_time: form_opening_time,
            form_closing_time: form_closing_time
        }
        $(document.getElementsByClassName("page_content")).append(frappe.render_template("not_opened_or_closed", data));
        $(".web-form-container").hide();
        $(".success-page").hide();
        $(".already-responded-page").hide();
        $(".error-page").hide();
        $(".form-not-opened-page").removeClass("hide");
    }
})

