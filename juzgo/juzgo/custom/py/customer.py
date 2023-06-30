import frappe
import json
@frappe.whitelist()
def add_member_details(row,doc):
    list = []
    row = json.loads(row)
    if frappe.db.exists("Customer",doc):
        doc = frappe.get_doc("Customer",doc)
        for j in doc.family_members_details:
            for i in doc.family_members_documents:
                if((row.get('member_row_id') != i.family_member_details_name) and (j.member_row_id == i.family_member_details_name)):
                    list.append({'members_name':i.get('members_name'),'age':i.get('age'),'gender':i.get('gender'),'check_list_name':i.check_list_name,'family_member_details_name':i.get('family_member_details_name'),'check':i.get('check'),'receive_or_send':i.receive_or_send})
    table_doc = frappe.get_all("Check List",{'gender':row.get('gender') or "Both",'age_limit_from':['<=', row.get('age')],'age_limit_to':['>=', row.get('age')],'disable':0,'check_list_for':"Customer"}) 
    
    if not table_doc:table_doc = frappe.get_all("Check List",{'gender':"Both",'age_limit_from':['<=', row.get('age')],'age_limit_to':['>=', row.get('age')],'disable':0,'check_list_for':"Customer"}) 
    if not table_doc:frappe.throw("Check List Not Found for Gender "+row.get('gender')+" and age "+str(row.get('age')))
    else:
        check_list_items = frappe.get_doc("Check List",table_doc[0].name).check_list_items
        for i in check_list_items:
            list.append({'members_name':row.get('members_name'),'age':row.get('age'),'gender':row.get('gender'),'check_list_name':i.check_list_name,'family_member_details_name':row.get('member_row_id'),'check':0,'receive_or_send':i.receive_or_send})
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
