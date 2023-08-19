# Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
class CAForm(Document):
	def validate(doc):
		if doc.ca_owner and (not doc.is_new()):
			assigned_to(doc,"ca_owner")
		if doc.assigned_to and (not doc.is_new()):
			assigned_to(doc,"assigned_to")
	def autoname(doc):
		if doc.party_type == "Lead":
			doc.party_name = doc.first_name + " "+(doc.last_name or "")
		elif doc.party_type == "Customer":
			doc.party_name = doc.customer
	def after_insert(doc):
		if doc.ca_owner:
			assigned_to(doc,"ca_owner")
		if doc.assigned_to:
			assigned_to(doc,"assigned_to")
@frappe.whitelist()
def room_preferences_remaining(room_preferences = None,family_details_table = None):
	if family_details_table == None:return
	if room_preferences:
		room_preferences = json.loads(room_preferences)
	family_details_table = json.loads(family_details_table)
	room_preferences_list = []
	family_list=[]
	if room_preferences:
		for i in range (0,len(room_preferences),1):
			if room_preferences[i].get('family') not in family_list:
				family_list.append(room_preferences[i].get('family'))
				adults = (room_preferences[i].get("adults") or 0)
				child_nbs = (room_preferences[i].get("child_nbs") or 0)
				child_wbeds = (room_preferences[i].get("child_wbeds") or 0)
				infant = (room_preferences[i].get("infant") or 0)
				for j in range(i+1,len(room_preferences),1):
					if(room_preferences[i].get("family") == room_preferences[j].get("family")):
						adults = (room_preferences[j].get("adults") or 0 ) + adults
						child_nbs = (room_preferences[j].get("child_nbs") or 0) + child_nbs
						child_wbeds = (room_preferences[j].get("child_wbeds") or 0) + child_wbeds
						infant = (room_preferences[j].get("infant") or 0) + infant
				room_preferences_list.append({'family':room_preferences[i].get('family'),"adults":adults,"child_nbs":child_nbs,"child_wbeds":child_wbeds,"infant":infant})
	remainding_list = []
	for i in family_details_table:
		for j in room_preferences_list:
			if i['family'] == j['family']:
				remainding_list.append({'family':(i.get('family') or 0) ,"adults":(i.get('adults') or 0) - (j.get('adults') or 0),"child_nbs":(i.get('child_no_beds') or 0) - (j.get('child_nbs') or 0),"child_wbeds":(i.get('child_with_beds') or 0) - (j.get('child_wbeds') or 0),"infant":(i.get('no_of_infant') or 0) - (j.get('infant') or 0)})
		if i.get('family') not in family_list:
			remainding_list.append({'family':(i.get('family') or 0) ,"adults":(i.get('adults') or 0),"child_nbs":(i.get('child_no_beds') or 0),"child_wbeds":(i.get('child_with_beds') or 0),"infant":(i.get('no_of_infant') or 0)})
	html = '''
				<style>
					th,td{
						border:1px solid black;
						padding:2px;
						text-align:center;
					}
					tr:nth-child(even){
						background-color:#eef3ad;
					}
					tr:nth-child(odd) {
						background-color:#adebbe;
					}
				</style>
				<h6>Family Members Remainding</h6>
				<table>
					<tr style="background-color:#74bec1;color:#516091">
						<th>
							Family
						</th>
						<th>
							adults
						</th>
						<th>
							CWB
						</th>
						<th>
							CNB
						</th>
						<th>
							infants
						</th>
					</tr>
					'''
	for j in remainding_list:
		html =html + f'''       
				<tr style="color:#364968">
					<td style="width:30%;">
						{j.get('family')}
					</td>
					<td style="width:20%;">
						{j.get('adults')}
					</td>
					<td style="width:20%;">
						{j.get('child_wbeds')}
					</td>
					<td style="width:20%;">
						{j.get('child_nbs')}
					</td>
					<td style="width:10%;">
						{j.get('infant')}
					</td>
				</tr>'''
	html =html + f'''   
		</table>
		'''
	return html
@frappe.whitelist()
def table_preview():
	table_pre = frappe.get_doc("Passport Document", "Passport Document")
	layout_height = frappe.db.get_single_value("System Settings","layout_height") or "Auto"
	image_width = frappe.db.get_single_value("System Settings","image_width") or "250px"
	image_height = frappe.db.get_single_value("System Settings","image_height") or "Auto"
	html = '''
		<html>
		<head>
			<style>
				div.gallery {
			border: 1px solid #ccc;
			}

			div.gallery:hover {
			border: 1px solid #777;
			box-shadow: 0 22px 26px 0 rgba(0,0,0,0.24),0 27px 60px 0 rgba(0,0,0,0.19);
			}

			div.gallery img {
			width:'''+image_width+''';
			height:'''+image_height+''';
			}

			div.desc {
			padding: 5px;
			width: '''+image_width+''';
			height: 50px;
			text-align: center;
			overflow:scroll;
			}

			* {
			box-sizing: border-box;
			}

			.responsive {
			padding: 0 6px 6px;
			height:'''+layout_height+''';
			float: left;
			}
			.responsive1 td{
			   border-right:1px solid black;
			   border-left:1px solid black;
			   border-top:1px solid black;
			   border-bottom:1px solid black;
			}
			.responsive1 th{
			   text-align : center;
			   border-right:1px solid black;
			   border-left:1px solid black;
			   border-top:1px solid black;
			   border-bottom:1px solid black;
			}
			.responsive2 td{
			   border-right:1px solid black;
			   border-left:1px solid black;
			   border-top:1px solid black;
			   border-bottom:1px solid black;
			}
			.responsive2 th{
			   text-align : center;
			   border-right:1px solid black;
			   border-left:1px solid black;
			   border-top:1px solid black;
			   border-bottom:1px solid black;
			}
			.clearfix:after {
			content: "";
			display: table;
			clear: both;
			}
			</style>
		</head>
		<body>
			<div class="responsive1">
				<div class="gallery1">
					<table style = "width: 80%">
						<tr style="background-color:#74bec1;color:#516091">
							<th style = "width: 3%">S.No</th>
							<th style = "width: 40%">Passport Document</th>
							<th>Reference URL</th>
						</tr>
	'''
	for i in table_pre.passport_document_table:
		# Use <td> for table data, not <div>
		html += f''' 
			<tr>
				<td> {i.idx} </td>
				<td>{i.document_details}</td>
				<td style = "color:blue"><a href ="{i.notes}" target="_blank">{i.notes}  </a></td>
			</tr>
		'''
	html += '''
				</table>
			</div>
		</div>
						<br>
				<br>
				 <h5>Image Reference</h5>
	'''
   
			  
			   
   
	for m in table_pre.passport_image_doc_table:
		# Use <td> for table data, not <div>
		html += f''' 
		
	 <div class="responsive">
				<div class="gallery">
				
			<a target="_blank" href="{m.image}">
					<img src="{m.image}" alt="No Image" >
					</a>
					<div class="desc">{m.description or ""}</div>
								</div>
		</div>
		'''
	html = html +'''
	 
		<div class="clearfix"></div>
		</body>
		</html>
	'''

	html1 = '''
		<style>
			th,td{
				border:1px solid black;
				padding:2px;
				text-align:center;
			}
		</style>
		<table style="width:100%;">
			<tr style="background-color:#74bec1;color:#516091">
				<th>
					S.No
				</th>
				<th>
					Issue Type
				</th>
				<th>
					Age
				</th>
				<th>
					Reissue Reason
				</th>
				<th>
					Books Page
				</th>
				<th>
					Scheme
				</th>
				<th>
					Gov. Fee
				</th>
				 <th>
					Service Fee Total
				</th>
				 <th>
					Other Company Fee
				</th>
			</tr>
	'''
	 
	for j in table_pre.passport_budget:
		html1 =html1 + f'''       
				<tr style="background-color:#eef3ad;color:#364968">
					<td style="width:3%;">
						{j.idx}
					</td>
					<td style="width:17%;">
						{j.issue_type or ""}
					</td>
					<td style="width:10%;">
						{j.age or ""}
					</td>
					<td style="width:28%;">
						{j.reissue_reason or ""}
					</td>
					<td style="width:5%;">
						{j.books_page or ""}
					</td>
					<td style="width:7%;">
						{j.scheme or ""}
					</td>
					<td style="text-align:left;width:10%;">
						{j.gov_fee or ""}
					</td>
					<td style="text-align:left;width:10%;">
						{j.service_fee_total or ""}
					</td>
					<td style="text-align:left;width:10%;">
						{j.other_company_fee or ""}
					</td>
				</tr>'''
	html1 =html1 + f'''   
			</table>
			'''
	return html,html1,table_pre.forex_ref_link,table_pre.train_info

@frappe.whitelist()
def temple_notes(temple = None):
	if temple:
		temple = json.loads(temple)
		temple_list = []
		for i in temple:temple_list.append(frappe.get_doc("Spots",i.get("temple_name")).dharsan_arthi)
		html = '''
				<style>
					th,td{
						border:1px solid black;
						padding:2px;
						text-align:center;
					}
				</style>
				<table style="width:100%;">
					<tr style="background-color:#74bec1;color:#516091">
						<th>
							Dharsan/Arthi Name
						</th>
						<th>
							Day
						</th>
						<th>
						Time
						</th>
						<th>
							Duration
						</th>
						<th>
							Ticket Price
						</th>
						<th>
							Notes
						</th>
					</tr>
					'''
		for i in temple_list:
			if(len(i) > 0):
				html =html + f'''
					<tr style="background-color:#adebbe;color:#364968;">
						<td colspan="5"><b>{i[0].parent}</b></td>
						<td>{frappe.get_value("Spots",i[0].parent,"notes") or ""}</td>
					</tr>
			'''
			for j in i:
				html =html + f'''       
						<tr style="background-color:#eef3ad;color:#364968">
							<td style="width:15%;">
								{j.dharsan_arthi_name or ""}
							</td>
							<td style="width:10%;">
								{j.day or ""}
							</td>
							<td style="width:15%;">
								{j.time or ""}
							</td>
							<td style="width:10%;">
								{j.duration or ""}
							</td>
							<td style="width:10%;">
								{j.ticket_price or ""}
							</td>
							<td style="text-align:left;width:40%;">
								{j.notes or ""}
							</td>
						</tr>'''
		html =html + f'''   
				</table>
				'''
		return html
@frappe.whitelist()
def make_project(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.project_name = source.party_name+"-"+source.whatsapp_number
	target_doc = get_mapped_doc(
		"CA Form",
		source_name,
		{"CA Form": {"doctype": "Project", "field_map": {"whatsapp_number": "phone_number", "expected_start_date ":"travel_start_date ","expected_end_date":"travel_end_date","ca_owner":"project_head"}}},
		target_doc,
		set_missing_values,
	)

	return target_doc

def assigned_to(doc,field_name):
	doc_ = frappe.new_doc("ToDo")        
	if frappe.db.exists("ToDo", {'reference_name': doc.name, 'field_name':field_name}):
		doc_ = frappe.get_doc("ToDo", {'reference_name': doc.name, 'field_name':field_name})
	user = frappe.db.get_value("User", doc.owner, "username")
	doc_.update({
		'date': frappe.utils.nowdate(),
		'allocated_to': doc.get(field_name),
		'description': f'Assignment for {doc.doctype} {doc.name}',
		'reference_type': doc.doctype,
		'reference_name': doc.name,
		'assigned_by': user,
		'field_name': field_name
	})
	doc_.flags.ignore_permissions = True
	doc_.flags.ignore_links = True
	doc_.save()