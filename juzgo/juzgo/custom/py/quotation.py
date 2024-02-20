import frappe

def item_adding(doc, action):
    if doc.items:
        air_ticket=[]
        package=[]
        for i in doc.items:
            if i.item_group == "Air Ticket":
                air_ticket.append({'description': i.item_name, 'amount':i.amount})
            if i.item_group == "Package":
                package.append({'description':i.item_name, 'amount':i.amount})
        doc.update({"custom_airtickets_details_": air_ticket})
        doc.update({'custom_package_details':package})