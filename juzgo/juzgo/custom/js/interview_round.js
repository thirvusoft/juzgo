frappe.ui.form.on("Interview Round",{
    refresh:function(frm){
      frm.set_query("interview_question","questions", function () {
          return { filters:{designation: ["in",[frm.doc.designation,""]] }};
        });
    }
})