frappe.ui.form.on("Interview Feedback", {
    interview_round: function (frm) {
        frappe.call({
            method: 'juzgo.custom.py.interview_feedback.get_interview_questions',
            args: {
                interview: frm.doc.interview,
                interview_round: frm.doc.interview_round
            },
            callback: function (r) {
                frm.set_value('interview_results', r.message);
            }
        });
    },
});
frappe.ui.form.on("Interview Questions Results", {
    score_points: function (frm,cdt,cdn) {
        var row = locals[cdt][cdn]
        if(row.score_points > row.actual_points ){
            frappe.throw("Score Points Cannot be Greater then Actual Points")
        }
    },
});