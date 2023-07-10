frappe.ui.form.on("Interview Round",{
    // refresh:function(frm){
    //   frm.set_query("interview_question","questions", function () {
    //       return { 
    //         filters:{designation: ["in",[frm.doc.designation,""]] }
    //       };
    //     });
    // }
    set_question:function(frm){
      if(frm.doc.designation){
        frappe.call({
          method:"juzgo.juzgo.custom.py.interview.interview_designation",
          args:{
            'designation' : frm.doc.designation,
            'table': frm.doc.questions
          },
          callback: function(r){
            r.message.forEach(row => {
              let child = cur_frm.add_child("questions")
              frappe.model.set_value(child.doctype, child.name, "interview_question", row.interview_question)
              frappe.model.set_value(child.doctype, child.name, "question", row.question)
              frappe.model.set_value(child.doctype, child.name, "actual_point", row.actual_point)
            });
            refresh_field("questions");
          }
        })
      } else {
        frappe.throw("Kindly Fill Designation")
      }
    }
})