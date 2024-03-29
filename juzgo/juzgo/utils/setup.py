import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def setup():
    setup_fields()
    role_creation()
    property_setter()
    email_template()
def property_setter():
    make_property_setter("Task", "status", "options", "Open\nWorking\nPending Review\nReviewed\nOverdue\nTemplate\nCompleted\nCancelled", "Long Text")
def setup_fields():
    custom_fields = {
        'HR Settings':[
            dict(
                fieldname= "send_interview_round_status",
                fieldtype= "Check",
                insert_after= "feedback_reminder_notification_template",
                label= "Send Interview Round Status",
            ),
            dict(
                fieldname= "send_interview_round_status_template",
                fieldtype= "Link",
                options= "Email Template",
                insert_after= "send_interview_round_status",
                label= "Send Interview Round Status Template",
                depends_on= "eval:doc.send_interview_round_status",
                mandatory_depends_on= "eval:doc.send_interview_round_status"
            ),
            dict(
                fieldname= "send_mail_interview_created",
                fieldtype= "Check",
                insert_after= "send_interview_round_status_template",
                label= "Send Mail Interview Created",
            ),
            dict(
                fieldname= "send_mail_interview_created_template",
                fieldtype= "Link",
                options= "Email Template",
                insert_after= "send_mail_interview_created",
                label= "Send Mail Interview Created Template",
                depends_on= "eval:doc.send_mail_interview_created",
                mandatory_depends_on= "eval:doc.send_mail_interview_created"
            ),
        ],
        'System Settings':[
            dict(
                fieldname= "sb_img_preview",
                fieldtype= "Section Break",
                insert_after= "disable_change_log_notification",
                label= "Image Preview",
                collapsible = 1
            ),
            dict(
                fieldname= "layout_width",
                fieldtype= "Data",
                insert_after= "sb_img_preview",
                label= "Layout Width",
                hidden=1
            ),
            dict(
                fieldname= "layout_height",
                fieldtype= "Data",
                insert_after= "layout_width",
                label= "Layout Height",
            ),
            dict(
                fieldname= "cb_img",
                fieldtype= "Column Break",
                insert_after= "layout_height",
            ),
            dict(
                fieldname= "image_width",
                fieldtype= "Data",
                insert_after= "cb_img",
                label= "Image Width",
            ),
            dict(
                fieldname= "image_height",
                fieldtype= "Data",
                insert_after= "image_width",
                label= "Image Height",
            ),
        ],
        # 'Projects Settings':[
        #     dict(
        #         fieldname= "default_task_approvel",
        #         fieldtype= "Table",
        #         insert_after= "ignore_employee_time_overlap",
        #         label= "Default Task Approvel",
        #         options="Default Task Approvel"
        #     ),
        # ]
    }
    create_custom_fields(custom_fields)

def role_creation():
    if not frappe.db.exists("Role", "Juzgo Employee"):
        role = frappe.new_doc("Role")
        role.role_name = "Juzgo Employee"
        role.save()
    if not frappe.db.exists("Role", "Juzgo Admin"):
        role = frappe.new_doc("Role")
        role.role_name = "Juzgo Admin"
        role.save()

    if not frappe.db.exists("File Type", "Client Copy"):
        ft = frappe.new_doc("File Type")
        ft.file_type = "Client Copy"
        ft.save()

    if not frappe.db.exists("File Type", "Itinerary File"):
        ft = frappe.new_doc("File Type")
        ft.file_type = "Itinerary File"
        ft.save()

    if not frappe.db.exists("File Type", "Air Ticketing"):
        ft = frappe.new_doc("File Type")
        ft.file_type = "Air Ticketing"
        ft.save()
            
def email_template():
    if not frappe.db.exists("Email Template", "Visa Supplier"):
        new = frappe.new_doc("Email Template")
        new.name = "Visa Supplier"
        new.subject = "Quotation Request-{{doc.project}}/{% for i in doc.destination %}{{i.destination_name}},{% endfor %}/PAX:-{{doc.no_of_pax}}/{{doc.travel_from_dates}}/{{doc.travel_to_dates}}"
        new.use_html = 1
        new.response_html = '''<h3>Dear {{supplier_name}},</h3>
<br>
            <p>Warm greetings from JuzGo Holidays Co.!</p><br>
            <p>We hope this message finds you well.</p><br>
            <p>We are currently in need of your esteemed services to facilitate a Group Tour/Individual tour  for the following dates and specifications:</p>
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;Destination: {% for i in doc.destination %}{{i.destination_name}},{% endfor %}<br>
            &nbsp;&nbsp;&nbsp;&nbsp;Travel dates <br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;From : {{doc.travel_from_dates}} <br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To: {{doc.travel_to_dates}} <br>
            &nbsp;&nbsp;&nbsp;&nbsp;Duration of stay : {{doc.duration_of_stay_in_destination}} <br>
            &nbsp;&nbsp;&nbsp;&nbsp;Total Pax: {{doc.no_of_pax}} <br>
            &nbsp;&nbsp;&nbsp;&nbsp;No. Of Adults: {{doc.no_of_adults}} <br>
            &nbsp;&nbsp;&nbsp;&nbsp;No. Of Child : {{doc.no_of_child}} <br>
            &nbsp;&nbsp;&nbsp;&nbsp;Child Ages: {{doc.child_ages}} <br>
            &nbsp;&nbsp;&nbsp;&nbsp;Visa Type: {{visa_type}} <br>
			&nbsp;&nbsp;&nbsp;&nbsp;Question: {{questions}} <br>
            <p>We kindly request your assistance in providing a comprehensive package that aligns with our requirements. Additionally, please include details regarding any additional services or amenities available, as well as any relevant terms and conditions.
            <br><br>
            We prioritize professionalism, reliability, and customer satisfaction, and we are confident that your expertise and services will greatly contribute to the success of our Group Tour.
            <br><br>
            Looking forward to your prompt response and partnership in this endeavor.
            <br><br>
            Thank you for your attention and cooperation.</p>
            <br>
            Best Regards,
            <br><br>
            {{doc.modified_by}} <br>
            JuzGo Holidays Co <br>
            Signature and phone numbers <br>
            
            
        
        '''
    if not frappe.db.exists("Email Template", "DMC Supplier"):
        new = frappe.new_doc("Email Template")
        new.name = "DMC Supplier"
        new.subject = "Quotation Request-{{doc.project}}/{% for i in doc.destination %}{{i.destination_name}},{% endfor %}/{{doc.no_of_pax}} PAX/Travel Dates : From {{doc.travel_from_dates}} To {{doc.travel_to_dates}}"
        new.use_html = 1
        new.response_html = '''<html>
    <body>
            <h3>Dear {{supplier_name}},</h3>
            <br>
            <p>Warm greetings from JuzGo Holidays Co.!</p><br>
            <p>We hope this message finds you well.</p><br>
            <p>We are currently in need of your esteemed services to facilitate a Group Tour/Individual tour  for the following dates and specifications:</p>
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;Destination: {% for i in doc.destination %}{{i.destination_name}},{% endfor %}<br>
            &nbsp;&nbsp;&nbsp;&nbsp;Travel dates <br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;From : {{doc.travel_from_dates}} <br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To: {{doc.travel_to_dates}} <br>
            &nbsp;&nbsp;&nbsp;&nbsp;Duration of stay : {{doc.duration_of_stay_in_destination}} <br>
            &nbsp;&nbsp;&nbsp;&nbsp;Total Pax: {{doc.no_of_pax}} <br>
            &nbsp;&nbsp;&nbsp;&nbsp;No. Of Adults: {{doc.no_of_adults}} <br>
            &nbsp;&nbsp;&nbsp;&nbsp;No. Of Child : {{doc.no_of_child}} <br>
            &nbsp;&nbsp;&nbsp;&nbsp;Child Ages: {{doc.child_ages}} <br>
            {% if spots or hotels or vehicle %}
            <h2 style="text-align:center;">Inclusions</h2>
            <table>
                <tr style="boder:1px soild black;">
                    <td style="boder:1px soild black;">
                        Options Descriptions
                    </td>
                    <td>
                        Option 1
                    </td>
                    <td>
                        Option 2
                    </td>
                    <td>
                        Option 3
                    </td>
                    <td>
                        Option 4
                    </td>
                    <td>
                        Option 5
                    </td>
                </tr>
                {% if hotels %}
                <tr>
                    <td>
                        Accommodation Details
                    </td>
                    <td>
                        {% set no = [] %}
                        {% for i in hotels %}
                            {% if i.options == "Option 1" and  i.hotel_name %}
                                {% set _ = no.append(1) %}
                                &nbsp;&nbsp;<b>{{no|len}}</b>{{"."}}
                                {{i.hotel_name}}
                                {% if i.room_category %}
                                    ({{i.room_category}})
                                {% endif %}
                                {% if i.meal_preference %}
                                    and Meal Plan is {{ i.meal_preference }}
                                {% endif %}
                                {% if i.no_of_nights or i.no_of_days %}
                                    for {{i.no_of_nights}} Nights {{i.no_of_days}} days.
                                {% endif %}
                                {{"/-"}}
                            {% endif %}
                        {% endfor %}

                    </td>
                    <td>
                        {% set no = [] %}
                        {% for i in hotels %}
                            {% if i.options == "Option 2" and  i.hotel_name %}
                                {% set _ = no.append(1) %}
                                &nbsp;&nbsp;<b>{{no|len}}</b>{{"."}}
                                {{i.hotel_name}}
                                {% if i.room_category %}
                                    ({{i.room_category}})
                                {% endif %}
                                {% if i.meal_preference %}
                                    and Meal Plan is {{ i.meal_preference }}
                                {% endif %}
                                {% if i.no_of_nights or i.no_of_days %}
                                    for {{i.no_of_nights}} Nights {{i.no_of_days}} days.
                                {% endif %}
                                {{"/-"}}
                            {% endif %}
                        {% endfor %}
                    </td>
                    <td>
                        {% set no = [] %}
                        {% for i in hotels %}
                            {% if i.options == "Option 3" and  i.hotel_name %}
                                {% set _ = no.append(1) %}
                                &nbsp;&nbsp;<b>{{no|len}}</b>{{"."}}
                                {{i.hotel_name}}
                                {% if i.room_category %}
                                    ({{i.room_category}})
                                {% endif %}
                                {% if i.meal_preference %}
                                    and Meal Plan is {{ i.meal_preference }}
                                {% endif %}
                                {% if i.no_of_nights or i.no_of_days %}
                                    for {{i.no_of_nights}} Nights {{i.no_of_days}} days.
                                {% endif %}
                                {{"/-"}}
                            {% endif %}
                        {% endfor %}
                    </td>
                    <td>
                        {% set no = [] %}
                        {% for i in hotels %}
                            {% if i.options == "Option 4" and  i.hotel_name %}
                                {% set _ = no.append(1) %}
                                &nbsp;&nbsp;<b>{{no|len}}</b>{{"."}}
                                {{i.hotel_name}}
                                {% if i.room_category %}
                                    ({{i.room_category}})
                                {% endif %}
                                {% if i.meal_preference %}
                                    and Meal Plan is {{ i.meal_preference }}
                                {% endif %}
                                {% if i.no_of_nights or i.no_of_days %}
                                    for {{i.no_of_nights}} Nights {{i.no_of_days}} days.
                                {% endif %}
                                {{"/-"}}
                            {% endif %}
                        {% endfor %}
                    </td>
                    <td>
                        {% set no = [] %}
                        {% for i in hotels %}
                            {% if i.options == "Option 5" and  i.hotel_name %}
                                {% set _ = no.append(1) %}
                                &nbsp;&nbsp;<b>{{no|len}}</b>{{"."}}
                                {{i.hotel_name}}
                                {% if i.room_category %}
                                    ({{i.room_category}})
                                {% endif %}
                                {% if i.meal_preference %}
                                    and Meal Plan is {{ i.meal_preference }}
                                {% endif %}
                                {% if i.no_of_nights or i.no_of_days %}
                                    for {{i.no_of_nights}} Nights {{i.no_of_days}} days.
                                {% endif %}
                                {{"/-"}}
                            {% endif %}
                        {% endfor %}
                    </td>
                </tr>
                {% endif %}
                {% if spots %}
                <tr>
                    <td>
                        Sightseeing Details
                    </td>
                    <td>
                        {% set no = [] %}
                        {% for i in spots %}
                            {% if i.options == "Option 1" and  i.spots%}
                                {% set _ = no.append(1) %}
                                &nbsp;&nbsp;<b>{{no|len}}</b>{{"."}}
                                {{i.spots}} 
                                {% if i.transfer_type %}
                                    on {{i.transfer_type}}
                                {% endif %}
                                {{"/-"}}
                            {% endif %}
                        {% endfor %}
                    </td>
                    <td>
                        {% set no = [] %}
                        {% for i in spots %}
                            {% if i.options == "Option 2" and  i.spots%}
                                {% set _ = no.append(1) %}
                                &nbsp;&nbsp;<b>{{no|len}}</b>{{"."}}
                                {{i.spots}} 
                                {% if i.transfer_type %}
                                    on {{i.transfer_type}}
                                {% endif %}
                                {{"/-"}}
                            {% endif %}
                        {% endfor %}
                    </td>
                    <td>
                        {% set no = [] %}
                        {% for i in spots %}
                            {% if i.options == "Option 3" and  i.spots%}
                                {% set _ = no.append(1) %}
                                &nbsp;&nbsp;<b>{{no|len}}</b>{{"."}}
                                {{i.spots}} 
                                {% if i.transfer_type %}
                                    on {{i.transfer_type}}
                                {% endif %}
                                {{"/-"}}
                            {% endif %}
                        {% endfor %}
                    </td>
                    <td>
                        {% set no = [] %}
                        {% for i in spots %}
                            {% if i.options == "Option 4" and  i.spots%}
                                {% set _ = no.append(1) %}
                                &nbsp;&nbsp;<b>{{no|len}}</b>{{"."}}
                                {{i.spots}} 
                                {% if i.transfer_type %}
                                    on {{i.transfer_type}}
                                {% endif %}
                                {{"/-"}}
                            {% endif %}
                        {% endfor %}
                    </td>
                    <td>
                        {% set no = [] %}
                        {% for i in spots %}
                            {% if i.options == "Option 5" and  i.spots%}
                                {% set _ = no.append(1) %}
                                &nbsp;&nbsp;<b>{{no|len}}</b>{{"."}}
                                {{i.spots}} 
                                {% if i.transfer_type %}
                                    on {{i.transfer_type}}
                                {% endif %}
                                {{"/-"}}
                            {% endif %}
                        {% endfor %}
                    </td>
                </tr>
                {% endif %}
                {% if vehicle %}
                <tr>
                    <td>
                        Vehicle Details
                    </td>
                    <td>
                        {% set no = [] %}
                        {% for i in vehicle %}
                            {% if i.options == "Option 1" and  i.vehicle%}
                                {% set _ = no.append(1) %}
                                &nbsp;&nbsp;<b>{{no|len}}</b>{{"."}}
                                {{i.vehicle}} 
                                {% if i.transfer_type %}
                                    on {{i.transfer_type}}
                                {% endif %}
                                {{"/-"}}
                            {% endif %}
                        {% endfor %}
                    </td>
                    <td>
                        {% set no = [] %}
                        {% for i in vehicle %}
                            {% if i.options == "Option 2" and  i.vehicle%}
                                {% set _ = no.append(1) %}
                                &nbsp;&nbsp;<b>{{no|len}}</b>{{"."}}
                                {{i.vehicle}} 
                                {% if i.transfer_type %}
                                    on {{i.transfer_type}}
                                {% endif %}
                                {{"/-"}}
                            {% endif %}
                        {% endfor %}
                    </td>
                    <td>
                        {% set no = [] %}
                        {% for i in vehicle %}
                            {% if i.options == "Option 3" and  i.vehicle%}
                                {% set _ = no.append(1) %}
                                &nbsp;&nbsp;<b>{{no|len}}</b>{{"."}}
                                {{i.vehicle}} 
                                {% if i.transfer_type %}
                                    on {{i.transfer_type}}
                                {% endif %}
                                {{"/-"}}
                            {% endif %}
                        {% endfor %}
                    </td>
                    <td>
                        {% set no = [] %}
                        {% for i in vehicle %}
                            {% if i.options == "Option 4" and  i.vehicle%}
                                {% set _ = no.append(1) %}
                                &nbsp;&nbsp;<b>{{no|len}}</b>{{"."}}
                                {{i.vehicle}} 
                                {% if i.transfer_type %}
                                    on {{i.transfer_type}}
                                {% endif %}
                                {{"/-"}}
                            {% endif %}
                        {% endfor %}
                    </td>
                    <td>
                        {% set no = [] %}
                        {% for i in vehicle %}
                            {% if i.options == "Option 5" and  i.vehicle%}
                                {% set _ = no.append(1) %}
                                &nbsp;&nbsp;<b>{{no|len}}</b>{{"."}}
                                {{i.vehicle}} 
                                {% if i.transfer_type %}
                                    on {{i.transfer_type}}
                                {% endif %}
                                {{"/-"}}
                            {% endif %}
                        {% endfor %}
                    </td>
                </tr>
                {% endif %}
            </table>
            {% endif %}
            <br>
            {% if others %}
            <h3>Others Details :</h3>
            
            {% for i in others %}
                {% if i.others %}
                
                    &nbsp;&nbsp;&nbsp;&nbsp;&#8227; {{i.others}}<br>
                
                {% endif %}
            {% endfor %}
            
            <br>
            {% endif %}
            <h3>Guide services Details:</h3>
            &nbsp;&nbsp;&nbsp;&nbsp;&#8227; English Speaking Guide Mandatory
            <br>
            <br>
            <p>Please provide optional costs for the below tours to accommodate the client preferences. Your prompt response is appreciated for crafting tailored itineraries</p>
            {% if optional_costs %}
            <br>
            <h3>Optional costs needed for the below tours :</h3>
            {% set no = [] %}
            {% for i in optional_costs %}
                {% if i.spots %}
                    {% set _ = no.append(1) %}
                    &nbsp;&nbsp;&nbsp;&nbsp;{{no|len}}{{". "}}{{i.spots}} 
                    {% if i.transfer_type %}
                        on {{i.transfer_type}}
                    {% endif %}
                    <br>
                {% endif %}
            {% endfor %}
            {% endif %}
            <br>
            <br>
            <p>We kindly request your assistance in providing a comprehensive package that aligns with our requirements. Additionally, please include details regarding any additional services or amenities available, as well as any relevant terms and conditions.
            <br><br>
            We prioritize professionalism, reliability, and customer satisfaction, and we are confident that your expertise and services will greatly contribute to the success of our Group Tour.
            <br><br>
            Looking forward to your prompt response and partnership in this endeavor.
            <br><br>
            Thank you for your attention and cooperation.</p>
            <br>
            Best Regards,
            <br><br>
            {%set user_name = frappe.get_doc("User",doc.modified_by)%}
            {{user_name.username}} <br>
            JuzGo Holidays Co <br>
            {{user_name.email_signature}} <br>
    </body>
</html>
                
            
            '''
        new.save()