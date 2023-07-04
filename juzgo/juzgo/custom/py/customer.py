import frappe
import json
@frappe.whitelist()
def add_member_details(row,doc):
    list = []
    row = json.loads(row)
    if frappe.db.exists("Customer",doc):
        doc_ = frappe.get_doc("Customer",doc)
        for j in doc_.family_members_details:
            for i in doc_.family_members_documents:
                if((row.get('member_row_id') != i.family_member_details_name) and (j.member_row_id == i.family_member_details_name)):
                    list.append({'members_name':i.get('members_name'),'age':i.get('age'),'gender':i.get('gender'),'check_list_name':i.check_list_name,'family_member_details_name':i.get('family_member_details_name'),'check':i.get('check'),'receive_or_send':i.receive_or_send})
    table_doc = frappe.get_all("Check List",{'gender':row.get('gender') or "Both",'age_limit_from':['<=', row.get('age')],'age_limit_to':['>=', row.get('age')],'disable':0,'check_list_for':"Customer"}) 
    
    if not table_doc:table_doc = frappe.get_all("Check List",{'gender':"Both",'age_limit_from':['<=', row.get('age')],'age_limit_to':['>=', row.get('age')],'disable':0,'check_list_for':"Customer"}) 
    if not table_doc:frappe.throw("Check List Not Found for Gender "+row.get('gender')+" and age "+str(row.get('age')))
    else:
        check_list_items = frappe.get_doc("Check List",table_doc[0].name).check_list_items
        for i in check_list_items:
            list.append({'members_name':row.get('members_name'),'age':row.get('age'),'gender':row.get('gender'),'check_list_name':i.check_list_name,'family_member_details_name':row.get('member_row_id'),'check':0,'receive_or_send':i.receive_or_send})
        if frappe.db.exists("Customer",doc):
            for i in list:
                for j in frappe.get_doc("Customer",doc).family_members_documents:
                    if ((i['members_name'] == j.members_name) and (str(i['age']) == str(j.age)) and (i['gender'] == j.gender) and (i['check_list_name'] == j.check_list_name) and (i['family_member_details_name'] == j.family_member_details_name)):
                        i['check'] = j.check
        return(list)
@frappe.whitelist()
def remove_list(row,name):
    row = json.loads(row)
    list=[]
    list1=[]
    doc = frappe.get_doc("Customer",name)
    for i in doc.family_members_documents:
        if(row.get('member_row_id') != i.family_member_details_name):
            list.append({'members_name':i.get('members_name'),'age':i.get('age'),'gender':i.get('gender'),'check_list_name':i.check_list_name,'family_member_details_name':i.get('family_member_details_name'),'check':i.get('check'),'receive_or_send':i.receive_or_send})
    for i in doc.family_members_table:
        if(row.get('member_row_id') != i.family_members_documents_name):
            list1.append({'members_name':i.get('members_name'),'file_type':i.get('file_type'),'file':i.get('file'),'next_remainder_or_expiry_on':i.next_remainder_or_expiry_on,'family_members_documents_name':i.get('family_members_documents_name'),'description':i.get('description'),'attached_by':i.get('attached_by'),'receive_or_send':i.receive_or_send})
    return(list,list1)

def validate(doc,even):
    if(doc.family_members_details):
        doc.family_members_documents = check_members_alive(doc,doc.family_members_documents,'family_member_details_name')
        doc.family_members_table = check_members_alive(doc,doc.family_members_table,'family_members_documents_name')
    else:
        doc.family_members_documents = []
        doc.family_members_table = []
    re_list = []
    for i in doc.family_members_documents:
        if(i.check == 0):
            re_list.append({'check_list_name':i.check_list_name,'members_name':i.members_name})
    remove_idx= []
    for j in doc.check_list_remainder_table:
        dele = 0
        for i in re_list:
            if i["check_list_name"] == j.check_list and i["members_name"] == j.member_name:
                dele = 1
        if dele == 0:
            remove_idx.append(j.idx-1)

    for i in reversed(remove_idx):
        doc.check_list_remainder_table.pop(i)
    idx = 1
    for k in doc.check_list_remainder_table:
        k.update({'idx': idx})
        idx = idx+1
    for i in re_list:
        new = 0
        for j in doc.check_list_remainder_table:
            if i["check_list_name"] == j.check_list and i["members_name"] == j.member_name:
                new = 1
        if new == 0:
            doc.append('check_list_remainder_table',dict(
                check_list=i["check_list_name"],
                member_name=i['members_name']
            ))


def check_members_alive(doc,field,id_field):
    table_field = field
    custom_list = []
    exiting_member = []
    missing_member =[]
    for i in doc.family_members_details:
        if i.get('member_row_id') not in exiting_member:custom_list.append(i.get('member_row_id'))
    for i in table_field:
        if i.get(id_field) not in exiting_member:exiting_member.append(i.get(id_field))

    for i in exiting_member:
        if i not in custom_list:
            missing_member.append(i)
    remove_idx= []
    if(missing_member):
        for i in range(0,len(table_field),1):
            if(table_field[i].get(id_field) in missing_member):
                remove_idx.append(i)

    for i in reversed(remove_idx):
        table_field.pop(i)
    return table_field