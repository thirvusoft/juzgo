import "./attach_formatter";
import "../templates/web_form/interview/error.html";
import "../templates/web_form/interview/already_responded.html";
import "../templates/web_form/interview/not_opened_or_closed.html";
import "../templates/web_form/interview/not_opened_or_closed.html";

$(document).on('app_ready', function () {
    console.log("Hii Test")
    frappe.realtime.off("show_notification")
    frappe.realtime.on("show_notification", (args)=>{
        var log = frappe.model.get_new_doc('Error Log')

        
        function show_notifications(notif){
            var log = frappe.model.get_new_doc('Error Log')
            log.method = "notif.subject"        
            log.error = notif.email_content
            frappe.call({method:"frappe.client.save", args:{doc:log}})
            var clicks = new Notification(strip_html(notif.subject), { body: strip_html(notif.email_content), icon: "https://app.juzgoholidays.com/files/juzgo%20length%20logo.jpg"});
            clicks.addEventListener('click', function(){
                frappe.set_route("Form", notif.document_type, notif.document_name);
            });       
           
        }
            if(args.doc.for_user==frappe.session.user){
                Notification.requestPermission((res) => {
                    console.log(res)
                    if(res == "granted")
                    show_notifications(args.doc)
                    });
            }

  
    })
});