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
        if doc.custom_airtickets_details_:
            ticket_amt = 0
            for ticket_detail in doc.custom_airtickets_details_:
                ticket_amt += ticket_detail.amount
            doc.custom_total_airtickets_amount = ticket_amt
        if doc.custom_package_details:
            pack_amt=0
            for pack in doc.custom_package_details:
                pack_amt += pack.amount + (doc.custom_other_charges_total or 0)
            doc.custom_total_package_amount = pack_amt
        if doc.custom_total_package_amount and doc.custom_package_amount_percentage:
            pack_account=float((doc.custom_total_package_amount or 0)*(int(doc.custom_package_amount_percentage or 0)/100))
            doc.custom_package_amount_account = pack_account
        if doc.custom_total_package_amount and doc.custom_package_amount_account:
            doc.custom_package_amount_cash=((doc.custom_total_package_amount)-(doc.custom_package_amount_account))
            doc.custom_package_cash_percentage=((doc.custom_total_package_amount)-(doc.custom_package_amount_account))
        if doc.custom_total_airtickets_amount or doc.custom_package_amount_account:
            doc.custom_net_payable_in_account = ((doc.custom_total_airtickets_amount or 0)+(doc.custom_package_amount_account or 0))
            doc.custom_net_payable_in_cash = doc.custom_package_cash_percentage
        if doc.custom_net_payable_in_account or doc.custom_net_payable_in_cash:
            doc.custom_net_total = ((doc.custom_net_payable_in_account or 0)+(doc.custom_net_payable_in_cash or 0))