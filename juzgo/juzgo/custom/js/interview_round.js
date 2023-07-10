frappe.ui.form.on("Interview Round",{
    refresh:function(frm){
      frm.set_query("interview_question","questions", function () {
          return { 
            query: "erpnext.controllers.queries.item_query",
            filters:{designation: ["in",[frm.doc.designation,""]] }
          
          };
        });
    }
})