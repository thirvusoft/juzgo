import "./attach_formatter";
import "../templates/web_form/interview/error.html";
import "../templates/web_form/interview/already_responded.html";
import "../templates/web_form/interview/not_opened_or_closed.html";
import "../templates/web_form/interview/not_opened_or_closed.html";

document.addEventListener("DOMContentLoaded", function (event) {
    frappe.realtime.off("show_notification")
    frappe.realtime.on("show_notification", (args)=>{
        var log = frappe.model.get_new_doc('Error Log')

        
        function show_notification(notif){
            var log = frappe.model.get_new_doc('Error Log')
            log.method = notif.subject        
            log.error = notif.email_content
            frappe.call({method:"frappe.client.save", args:{doc:log}})
            new Notification("To do list")
             }
                    
            Notification.requestPermission((res) => {
                console.log(res)
                if(res == "granted")
                show_notification(args.doc)
                });  
    })
});