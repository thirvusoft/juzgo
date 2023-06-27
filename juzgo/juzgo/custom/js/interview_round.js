frappe.ui.form.on("Interview Round",{
    refresh:function(frm){
        var list =[]
        frappe.db.get_list("Interview Question", {
            fields: ["name","designation"],
          }).then((data) => {
            if (data.length > 0) {
              data.forEach((el) => {
                if(el.designation == frm.doc.designation || !el.designation)
                    list.push(el.name);
              });
            }
            frm.set_query("interview_question","questions", function () {
                return { filters:{name: ["in",list] }};
              });
          });
    }
})