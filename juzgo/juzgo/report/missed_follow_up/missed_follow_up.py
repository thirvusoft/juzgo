import frappe


def execute(filters={}):
	columns, data = get_columns() or [], get_data(filters) or []
	return columns, data



def get_columns():
	columns = [
		{
			'fieldname':'name',
			'fieldtype':'Link',
			'label':'Lead ID',
			'options':"Lead",
			'width':200
		},
		{
			'fieldname':'client_name',
			'fieldtype':'Data',
			'label':'Lead Name',
			'width':150
		},
		{
			'fieldname':'next_follow_up_date',
			'fieldtype':'Date',
			'label':'Assigned Date',
			'width':150
		},	
		{
			'fieldname':'next_followup_by',
			'fieldtype':'Link',
			'label':'Follow Up By',
			'options': 'User',
			'width':220
		},
		{
			'fieldname':'status',
			'fieldtype':'Data',
			'label':'Status',
			'width':100
		},	
		{
			'fieldname':'mode_of_communication',
			'fieldtype':'Link',
			'label':'Mode of Communication',
			'options': 'Mode of Communication',
			'width':100
		},
		{
			'fieldname':'mobile_no',
			'fieldtype':'Data',
			'label':'WhatsApp No',
			'width':100
		},
		{
			'fieldname':'description',
			'fieldtype':'Data',
			'label':'Description',
			'width':400,
			'length':1000
		},
		
	]
	return columns


def get_data(filters):
	follow_up_filter = {}
	lead_filter = {'status':['not in', ['Do Not Contact','Booked']]}

	
	follow_up_filter['next_follow_up_date'] = ['<',frappe.utils.datetime.date.today()]
	if(filters.get('next_followup_by')):
		follow_up_filter["next_followup_by"] = filters.get('next_followup_by')
	all_leads = frappe.db.get_all('Follow Ups', filters=follow_up_filter, fields=['idx', 'parent'])
	all_leads1=[]
	for i in all_leads:
		follow_up_filter['parent'] = i['parent']
		
		if(max(frappe.db.get_all('Follow Ups', filters={'parent':i['parent']}, pluck='idx')) == i['idx']):	
			all_leads1.append(i)


	leads = [i['parent'] for i in all_leads1]
	lead_filter["name"] = ['in',leads]
	# lead_filter["next_follow_up_date"] = ['<',frappe.utils.datetime.date.today()]
	leads = frappe.db.get_all('Lead', filters=lead_filter, fields=['name','lead_name as client_name', 'phone', 'whatsapp_no as mobile_no', 'status'])
	
	for i in range(len(leads)):
		leads[i].next_followup_by=frappe.get_value("Follow Ups",{"parent":leads[i].name,"idx":max(frappe.db.get_all('Follow Ups', filters={'parent':leads[i].name}, pluck='idx'))},"next_followup_by")
		leads[i].mode_of_communication=frappe.get_value("Follow Ups",{"parent":leads[i].name,"idx":max(frappe.db.get_all('Follow Ups', filters={'parent':leads[i].name}, pluck='idx'))},"mode_of_communication")
		leads[i].doctype = frappe.get_value("Follow Ups",{"parent":leads[i].name,"idx":max(frappe.db.get_all('Follow Ups', filters={'parent':leads[i].name}, pluck='idx'))},"parenttype")
		leads[i].next_follow_up_date = frappe.get_value("Follow Ups",{"parent":leads[i].name,"idx":max(frappe.db.get_all('Follow Ups', filters={'parent':leads[i].name}, pluck='idx'))},"next_follow_up_date")
		leads[i].description = frappe.get_value("Follow Ups",{"parent":leads[i].name,"idx":max(frappe.db.get_all('Follow Ups', filters={'parent':leads[i].name}, pluck='idx'))},"description")
	return leads