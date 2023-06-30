import json
import frappe
from frappe.contacts.doctype.address.address import get_address_display
def validate(doc,action):
    doc.customer_contact_details = []
    for i in doc.family_member_details:
        doc.append("customer_contact_details",{
            "customer":i.customer_id,
            "address":frappe.get_value("Customer",i.customer_id,'customer_primary_address'),
            "contact":frappe.get_value("Customer",i.customer_id,'customer_primary_contact')
        })
@frappe.whitelist()
def get_project_abbr(project_name):
    m = project_name
    x = slice(3)
    return m[x].upper()

@frappe.whitelist()
def get_family_member_details_list(family_member_details,custom_list):
    family_member_details = json.loads(family_member_details)
    custom_list = json.loads(custom_list)
    exiting_customer = []
    missing_customer =[]
    for i in family_member_details:
        if i.get('customer_id') not in exiting_customer:exiting_customer.append(i.get('customer_id'))
   
    for i in exiting_customer:
        if i not in custom_list:
            missing_customer.append(i)

    remove_idx= []
    if(missing_customer):
        for i in range(0,len(family_member_details),1):
            if(family_member_details[i].get('customer_id') in missing_customer):
                remove_idx.append(i)

    for i in reversed(remove_idx):
        family_member_details.pop(i)

    for cus in custom_list:
        custom_details = frappe.get_doc("Customer",cus).family_members_details
        for i in custom_details:
            if cus not in exiting_customer:
                family_member_details.append({
                    "members_name":i.members_name,
                    "date_of_birth":i.date_of_birth,
                    "gender":i.gender,
                    "age":i.age,
                    "relationship":i.relationship,
                    "member_row_id":i.member_row_id,
                    "customer_id":cus
                })
    return family_member_details

@frappe.whitelist()
def get_family_member_attachment(family_members_attachment,custom_list):
    family_members_attachment = json.loads(family_members_attachment)
    custom_list = json.loads(custom_list)
    # exiting_customer = []
    # missing_customer =[]
    # for i in family_members_attachment:
    #     if i.get('customer_id') not in exiting_customer:exiting_customer.append(i.get('customer_id'))
   
    # for i in exiting_customer:
    #     if i not in custom_list:
    #         missing_customer.append(i)

    # remove_idx= []
    # if(missing_customer):
    #     for i in range(0,len(family_members_attachment),1):
    #         if(family_members_attachment[i].get('customer_id') in missing_customer):
    #             remove_idx.append(i)

    # for i in reversed(remove_idx):
    #     family_members_attachment.pop(i)
    # cus_file_type={}
    # for cus in custom_list:
    #     cus_file_type[cus] = []
    # exiting_doc = [(i.get("members_name") or '')+(i.get("file_type") or '') for i in family_members_attachment]
    family_members_attachment = []
    for cus in custom_list:
        custom_details = frappe.get_doc("Customer",cus).family_members_table
        for i in custom_details:
            # if cus not in exiting_customer:
                family_members_attachment.append({
                    "members_name":i.members_name,
                    "file_type":i.file_type,
                    "file":i.file,
                    "next_remainder_or_expiry_on":i.next_remainder_or_expiry_on,
                    "description":i.description,
                    "attached_by":i.attached_by,
                    "family_members_documents_name":i.family_members_documents_name,
                    "customer_id":cus,
                    "receive_or_send":i.receive_or_send
                })
            # else:
            #     for update in range (len(family_members_attachment)):
            #         if((family_members_attachment[update].get('members_name') == i.members_name) and (family_members_attachment[update].get('family_members_documents_name') == i.family_members_documents_name) and (family_members_attachment[update].get('file_type') == i.file_type) ):
            #             family_members_attachment[update].update({
            #                 'file_type':i.file_type,
            #                 'file' : i.file,
            #                 'next_remainder_or_expiry_on' : i.next_remainder_or_expiry_on,
            #                 'description' : i.description,
            #                 'attached_by' : i.attached_by,
            #                 "receive_or_send":i.receive_or_send
            #             })
            #         if (i.get("members_name") or '')+(i.get("file_type") or '') not in exiting_doc:
            #             family_members_attachment.append({
            #                 "members_name":i.members_name,
            #                 "file_type":i.file_type,
            #                 "file":i.file,
            #                 "next_remainder_or_expiry_on":i.next_remainder_or_expiry_on,
            #                 "description":i.description,
            #                 "attached_by":i.attached_by,
            #                 "family_members_documents_name":i.family_members_documents_name,
            #                 "customer_id":cus,
            #                 "receive_or_send":i.receive_or_send
            #             })
            #             exiting_doc.append((i.get("members_name") or '')+(i.get("file_type") or ''))
    members_attachment_project = []
    for cus in custom_list:
        custom_details = frappe.get_doc("Customer",cus).family_members_documents
        for i in custom_details:
            members_attachment_project.append({
                "members_name":i.members_name,
                "check_list_name":i.check_list_name,
                "check":i.check,
                "receive_or_send":i.receive_or_send,
            })
    return family_members_attachment,members_attachment_project


@frappe.whitelist()
def add_destination_details(name,destination):
    list = []
    destination = json.loads(destination)
    doc = frappe.get_doc("Project",name)
    old_destination_check_list = doc.destination_check_list
    if(destination):
        for des in destination:
            for row in doc.family_member_details:
                destination_list = frappe.get_all("Destination Table",{"Destination":des,"parentfield":"destination_name"},pluck="parent") 
                table_doc = []
                for i in destination_list:
                    table_doc = frappe.get_all("Check List",{'gender':row.get('gender') or "Both",'age_limit_from':['<=', row.get('age')],'age_limit_to':['>=', row.get('age')],'disable':0,'check_list_for':"Destination",'name':i}) 
                    if not table_doc:table_doc = frappe.get_all("Check List",{'gender':"Both",'age_limit_from':['<=', row.get('age')],'age_limit_to':['>=', row.get('age')],'disable':0,'check_list_for':"Destination","name":i}) 
                if not table_doc:frappe.msgprint("Check List Not Found for Gender "+row.get('gender')+" and age "+str(row.get('age'))+" for "+row.get('members_name'))
                else:
                    check_list_items = frappe.get_doc("Check List",table_doc[0].name).check_list_items
                    for i in check_list_items:
                       list.append({'members_name':row.get('members_name'),'age':row.get('age'),'gender':row.get('gender'),'check_list_name':i.check_list_name,'family_member_details_name':row.get('member_row_id'),'check':0,'destination':des,'customer_id':row.get('customer_id'),"receive_or_send":i.receive_or_send})
    for i in list:
        for j in old_destination_check_list:
            if ((i['members_name'] == j.members_name) and (str(i['age']) == str(j.age)) and (i['gender'] == j.gender) and (i['check_list_name'] == j.check_list_name) and (i['family_member_details_name'] == j.family_member_details_name) and (i['customer_id'] == j.customer_id)):
                i['check'] = j.check
    
    return(list)

@frappe.whitelist()
def remove_function(table_field,custom_list):
    table_field = json.loads(table_field)
    custom_list = json.loads(custom_list)
    exiting_customer = []
    missing_customer =[]
    for i in table_field:
        if i.get('customer_id') not in exiting_customer:exiting_customer.append(i.get('customer_id'))
   
    for i in exiting_customer:
        if i not in custom_list:
            missing_customer.append(i)

    remove_idx= []
    if(missing_customer):
        for i in range(0,len(table_field),1):
            if(table_field[i].get('customer_id') in missing_customer):
                remove_idx.append(i)

    for i in reversed(remove_idx):
        table_field.pop(i)
    return table_field

@frappe.whitelist()
def family_member_details_seprate(table):
    table = json.loads(table)
    table_seprate ={}
    html = ''
    for i in table:
        table_seprate[i["customer_id"]]=[]
    for i in table:
        table_seprate[i["customer_id"]].append({
            "no":i["idx"],
            "customer":i["customer_id"],
            "address":frappe.get_value("Customer",i['customer_id'],'customer_primary_address'),
            "contact":frappe.get_value("Customer",i['customer_id'],'customer_primary_contact'),
            "member_name":i["members_name"],
            "date_of_birth":i["date_of_birth"],
            "gender":i['gender'],
            "age":i['age'],
            "relationship":i.get("relationship")
        })
    if table_seprate:
        html = """
        <div>
            <style>
                table {
                border-collapse: collapse;
                width: 100%;
                }

                th, td {
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #DDD;
                }

                tr:hover {background-color: #D6EEEE;}
                .main{
                    background-color: lightgrey;border: 2px solid #4287f5;padding: 10px;margin: 10px;border-radius: 10px;
                }
                div.main:hover{
                    box-shadow: 5px 5px 5px 5px;
                }
            </style>
        </div>
        """
    
        for i in table_seprate:
            html = html + f"""
            <div class="main">
            <table>
                <tr>
                    <td style="width:20%;">
                        <b>Customer Name </b> 
                    </td>
                    <td>
                        :- {i} 
                    </td>
                </tr>
                <tr>
                    <td><b>Contact       </b></td> 
                    <td>:- {frappe.get_value("Contact",table_seprate[i][0].get("contact"),'phone') or "" } </td>
                </tr>
                <tr>
                    <td><b>Address       </b></td>
                    <td> {get_address_display(table_seprate[i][0].get("address")) if table_seprate[i][0].get("address") else ""}</td>
                </tr>
           </table>
           <table>
            <tr>
                <th>No</th>
                <th>Member Name</th>
                <th>Date Of Birth</th>
                <th>Gender</th>
                <th>Age</th>
                <th>Relationship</th>
            </tr>
            """
            for j in table_seprate[i]:
                html = html + f"""
                <tr>
                <td>
                    {j.get("no")}
                </td>
                <td>
                    {j.get("member_name")}
                </td>
                <td>
                   {str(j.get("date_of_birth"))}
                </td>
                <td>
                    {j.get("gender")}
                </td>
                <td>
                    {str(j.get("age"))}
                </td>
                <td>
                    {str(j.get("relationship") or "")}
                </td>
                </tr>
                """
            html = html + """
            </table>
            </div>
            <hr>
            """
    return html