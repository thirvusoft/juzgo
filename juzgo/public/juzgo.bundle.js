import "./attach_formatter";
import "./assign_to";
import "./page.js";
import "./comman_func"
import "../templates/web_form/interview/error.html";
import "../templates/web_form/interview/already_responded.html";
import "../templates/web_form/interview/not_opened_or_closed.html";
import "../templates/web_form/interview/not_opened_or_closed.html";

$(document).on('app_ready', function () {
    frappe.realtime.off("show_notification")
    frappe.realtime.on("show_notification", (args)=>{
        function show_notifications(notif){
            var clicks = new Notification(strip_html(notif.subject), { body: strip_html(notif.email_content), icon: "https://app.juzgoholidays.com/files/juzgo%20length%20logo.jpg"});
            clicks.addEventListener('click', function(){
                frappe.set_route("Form", notif.document_type, notif.document_name);
            });       
           
        }
            if(args.doc.for_user==frappe.session.user){
                frappe.db.get_value("User", {"name": args.doc.for_user}, "notify", (r) => {
                    if(r.notify == 1){
                        Notification.requestPermission((res) => {
                            if(res == "granted")
                            show_notifications(args.doc)
                            });
                    }

                });
            
            }

  
    })
});