import json
import frappe

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
    exiting_customer = []
    missing_customer =[]
    for i in family_members_attachment:
        if i.get('customer_id') not in exiting_customer:exiting_customer.append(i.get('customer_id'))
   
    for i in exiting_customer:
        if i not in custom_list:
            missing_customer.append(i)

    remove_idx= []
    if(missing_customer):
        for i in range(0,len(family_members_attachment),1):
            if(family_members_attachment[i].get('customer_id') in missing_customer):
                remove_idx.append(i)

    for i in reversed(remove_idx):
        family_members_attachment.pop(i)

    for cus in custom_list:
        custom_details = frappe.get_doc("Customer",cus).family_members_table
        for i in custom_details:
            if cus not in exiting_customer:
                family_members_attachment.append({
                    "members_name":i.members_name,
                    "file_type":i.file_type,
                    "file":i.file,
                    "next_remainder_or_expiry_on":i.next_remainder_or_expiry_on,
                    "description":i.description,
                    "attached_by":i.attached_by,
                    "family_members_documents_name":i.family_members_documents_name,
                    "customer_id":cus
                })
    return family_members_attachment


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
                if not table_doc:frappe.throw("Check List Not Found for Gender "+row.get('gender')+" and age "+str(row.get('age')))
                else:
                    check_list_items = frappe.get_doc("Check List",table_doc[0].name).check_list_items
                    for i in check_list_items:
                       list.append({'members_name':row.get('members_name'),'age':row.get('age'),'gender':row.get('gender'),'check_list_name':i.check_list_name,'family_member_details_name':row.get('member_row_id'),'check':0,'destination':des,'customer_id':row.get('customer_id')})
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