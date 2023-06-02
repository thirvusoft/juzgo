frappe.ui.form.on("Interview Feedback", {
    interview_round: function (frm) {
        frappe.call({
            method: 'juzgo.custom.py.interview_feedback.get_interview_questions',
            args: {
                interview_round: frm.doc.interview_round
            },
            callback: function (r) {
                frm.set_value('interview_results', r.message);
            }
        });
    },
});
