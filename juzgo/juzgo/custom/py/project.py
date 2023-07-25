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
    x = slice(5)
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
        attach_details = frappe.get_doc("Customer",cus).family_members_table
        for i in custom_details:
            if i.check == 1:
                for j in attach_details:
                    if i.family_member_details_name == j.family_members_documents_name and i.check_list_name == j.file_type:
                        members_attachment_project.append({
                            "members_name":i.members_name,
                            "check_list_name":i.check_list_name,
                            "check":i.check,
                            "receive_or_send":i.receive_or_send,
                            "file":j.file,
                            "next_remainder_or_expiry_on":j.next_remainder_or_expiry_on,
                            "description":j.description
                        })
            else:
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
    print(destination)
    if(destination):
        for des in destination:
            for row in doc.family_member_details:
                destination_list = frappe.get_all("Destination Table",{"Destination":des,"parentfield":"destination_name"},pluck="parent") 
                table_doc = []
                for i in destination_list:
                    table_doc = frappe.get_all("Check List",{'gender':row.get('gender') or "Both",'age_limit_from':['<=', row.get('age')],'age_limit_to':['>=', row.get('age')],'disable':0,'check_list_for':"Destination",'name':i}) 
                    if not table_doc:table_doc = frappe.get_all("Check List",{'gender':"Both",'age_limit_from':['<=', row.get('age')],'age_limit_to':['>=', row.get('age')],'disable':0,'check_list_for':"Destination","name":i}) 
                    if table_doc:break
                if not table_doc:frappe.msgprint("In Destination Check List Not Found for Gender "+row.get('gender')+" and age "+str(row.get('age'))+" for "+row.get('members_name'))
                else:
                    check_list_items = frappe.get_doc("Check List",table_doc[0].name).check_list_items
                    for i in check_list_items:
                       list.append({'members_name':row.get('members_name'),'age':row.get('age'),'gender':row.get('gender'),'check_list_name':i.check_list_name,'family_member_details_name':row.get('member_row_id'),'check':0,'destination':des,'customer_id':row.get('customer_id'),"receive_or_send":i.receive_or_send})
    for i in list:
        for j in old_destination_check_list:
            if ((i['members_name'] == j.members_name) and (str(i['age']) == str(j.age)) and (i['gender'] == j.gender) and (i['check_list_name'] == j.check_list_name) and (i['family_member_details_name'] == j.family_member_details_name) and (i['customer_id'] == j.customer_id) and (i['destination'] == j.destination)):
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
    parent = ""
    for i in table:
        table_seprate[i["customer_id"]]=[]
        parent = i["parent"]
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
                .addbutton {
                    background-color: #4287f5;
                    border: none;
                    color: white;
                    padding: 5px 5px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 10px;
                    margin: 4px 2px;
                    cursor: pointer;
                    -webkit-transition-duration: 0.4s; /* Safari */
                    transition-duration: 0.4s;
                }
                .removebutton {
                    background-color: red;
                    border: none;
                    color: white;
                    padding: 5px 5px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 10px;
                    margin: 4px 2px;
                    cursor: pointer;
                    -webkit-transition-duration: 0.4s; /* Safari */
                    transition-duration: 0.4s;
                }
                .addbutton:hover {
                    box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24),0 17px 50px 0 rgba(0,0,0,0.19);
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
                .modal1 {
                    display: none; 
                    position: fixed; 
                    z-index: 6; 
                    left: 0;
                    top: 0;
                    width: 100%; 
                    height: 100%; 
                    overflow: auto;
                    background-color: #474e5d;
                    padding-top: 50px;
                }
                .clearfix::after {
                    content: "";
                    clear: both;
                    display: table;
                }
                .modal1-content {
                    background-color: #fefefe;
                    margin: 15% auto 15% auto; /* 5% from the top, 15% from the bottom and centered */
                    border: 1px solid #888;
                    width: 30%;
                    border-radius: 10px;
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
            html = html + f"""
            </table>
            <button class="addbutton" onclick="addmember('{i}','{parent}')" style="width:auto;">Add Member</button>
            </div>
            <hr>
            """
        html = html+"""
<div id="id01" class="modal1">
  <form class="modal1-content" onsubmit="return AddtoTable()">
    <div class="container">
      <h4 id="member_name_label">Add New Family Member</h4>
      <label for="member_name"><b>Member Name</b></label>
      <input id="customer_id" value="" hidden=1 ></input>
	  <select id="child_select"><option value="" disabled="disabled">Select Family Member</option></select>
      <div class="clearfix">
        <button class="removebutton" type="button" onclick="document.getElementById('id01').style.display='none'" class="cancelbtn">Cancel</button>
        <button class="addbutton" type="button" onclick="AddtoTable()" class="signupbtn">Add</button>
      </div>
    </div>
  </form>
</div>

<script>
var modal = document.getElementById('id01');

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
function addmember(cus_id,table) {
  document.getElementById('id01').style.display='block';
  document.getElementById('member_name_label').innerHTML="Add "+cus_id+"'s Family Member";
  document.getElementById('customer_id').value=cus_id;
  var el_child = document.getElementById("child_select");
  frappe.call({
        method:'juzgo.juzgo.custom.py.project.collect_details',
        args:{
            cus_id:cus_id,
            parent:table
        },
        callback(t){
            var r = t.message[0]
            var r1 = t.message[1]
            for(let i=0;i<r.length;i++){
                let p = 0
                for(let j=0;j<r1.length;j++){
                    if(r[i].members_name == r1[j].members_name && r[i].member_row_id == r1[j].member_row_id){
                    p=1
                    }
                }
                if(p == 0){
                    el_child.innerHTML = el_child.innerHTML + '<option value='+r[i].name+'>'+ r[i].members_name +'</option>';
                }
            }
        }
    })
}
function AddtoTable(){
    let cus_id =  document.getElementById('customer_id').value
    let member_row_id = document.getElementById('child_select').value
    frappe.call({
        method:'juzgo.juzgo.custom.py.project.add_family_details',
        args:{
            name:member_row_id,
        },
        callback(t){
            let row = t.message
            let child = cur_frm.add_child("family_member_details")
            frappe.model.set_value(child.doctype, child.name, "members_name", row[0].members_name)
            frappe.model.set_value(child.doctype, child.name, "date_of_birth", row[0].date_of_birth)
            frappe.model.set_value(child.doctype, child.name, "gender", row[0].gender)
            frappe.model.set_value(child.doctype, child.name, "age", row[0].age)
            frappe.model.set_value(child.doctype, child.name, "relationship", row[0].relationship)
            frappe.model.set_value(child.doctype, child.name, "member_row_id", row[0].member_row_id)
            frappe.model.set_value(child.doctype, child.name, "customer_id", cus_id)
            refresh_field("family_member_details");
            cur_frm.save()
            document.getElementById('id01').style.display='none'
        }
    })
    
}
</script>

        """
    return html

@frappe.whitelist()
def collect_details(cus_id,parent):
    family_members_details = frappe.get_all('Family Members Details',filters={'parent':cus_id}, fields=['name','members_name','member_row_id'])
    project_family_details = frappe.get_all('Project Family Details',filters={'parent':parent,'customer_id':cus_id}, fields=['name','members_name','member_row_id'])
    return(family_members_details,project_family_details)
@frappe.whitelist()
def add_family_details(name):
    return frappe.get_all('Family Members Details', filters={'name':name}, fields=['date_of_birth','gender','age','relationship','members_name','member_row_id'])
def project_head(doc,actions):
    if doc.project_head and (actions == "after_insert" or not doc.is_new()):
        doc_ = frappe.new_doc("ToDo")    
        if frappe.db.exists("ToDo", {'reference_name': doc.name , 'field_name':'project_head'}):
            doc_ = frappe.get_doc("ToDo", {'reference_name': doc.name , 'field_name':'project_head'})
        user = frappe.db.get_value("User", doc.owner, "username")
        doc_.update({
            'date': frappe.utils.nowdate(),
            'allocated_to': doc.project_head,
            'description': f'Project is assigned {doc.name}',
            'reference_type': doc.doctype,
            'reference_name': doc.name,
            'assigned_by': user,
            'field_name':'project_head',
            'status':"Open",
        })
        doc_.flags.ignore_permissions = True
        doc_.flags.ignore_links = True
        doc_.save()


def validate_check(doc,even):
    re_list = []
    for i in doc.destination_check_list:
        if(i.check == 0):
            re_list.append({'check_list_name':i.check_list_name,'members_name':i.members_name,'customer_id':i.customer_id})
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
                member_name=i['members_name'],
                customer_id = i["customer_id"]
            ))

@frappe.whitelist()
def project_exist_list(project_name):
    task_name=frappe.db.get_all("Project", filters={"project_name":["Like", "%"+project_name+"%"]}, fields=["name","project_name"])
    return task_name