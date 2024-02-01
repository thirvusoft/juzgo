from frappe.model.naming import parse_naming_series, make_autoname
from frappe.model.naming import parse_naming_series
import frappe

import json

def autoname(self,action):
    if self.branch == "Test":
        series = 'SI-TST-.YY.-'
        self.name = make_autoname(series, doc=self)
        self.naming_series = parse_naming_series(series, doc=self)
    else:
        series = 'SINV-.YY.-'
        self.name = make_autoname(series, doc=self)
        self.naming_series = parse_naming_series(series, doc=self)

def tax_details(doc):

    sgst_list = []
    cgst_list = []
    igst_list = []
    tcs_list = []

    for tax in doc.taxes:

        if "SGST" in tax.account_head and tax.tax_amount != 0:
            tax_details = json.loads(tax.item_wise_tax_detail)
            values = list(tax_details.values())

            for value in values:

                if sgst_list:

                    matched = False

                    for i in range (0, len(sgst_list), 1):

<<<<<<< HEAD
                        if sgst_list[i].get(f"SGST@ {value[0]} %"):
                            sgst_list[i][f"SGST@ {value[0]} %"] += value[1]
                            break

                        if len(sgst_list) == i + 1 and not matched:
                            sgst_list.append({f"SGST@ {value[0]} %": value[1]})
                else:
                    sgst_list.append({f"SGST@ {value[0]} %": value[1]})
=======
                        if value[0] != 0:

                            if sgst_list[i].get(f"SGST@ {value[0]} %"):
                                sgst_list[i][f"SGST@ {value[0]} %"] += value[1]
                                break

                            if len(sgst_list) == i + 1 and not matched:
                                sgst_list.append({f"SGST@ {value[0]} %": value[1]})
                else:
                    if value[0] != 0:
                        sgst_list.append({f"SGST@ {value[0]} %": value[1]})
>>>>>>> c06d5715bf2a77bcea50c88e7b8892c64b139710

        if "CGST" in tax.account_head and tax.tax_amount != 0:
            tax_details = json.loads(tax.item_wise_tax_detail)
            values = list(tax_details.values())

            for value in values:

                if cgst_list:

                    matched = False

                    for i in range (0, len(cgst_list), 1):

<<<<<<< HEAD
                        if cgst_list[i].get(f"CGST@ {value[0]} %"):
                            cgst_list[i][f"CGST@ {value[0]} %"] += value[1]
                            break

                        if len(cgst_list) == i + 1 and not matched:
                            cgst_list.append({f"CGST@ {value[0]} %": value[1]})
                else:
                    cgst_list.append({f"CGST@ {value[0]} %": value[1]})
=======
                        if value[0] != 0:

                            if cgst_list[i].get(f"CGST@ {value[0]} %"):
                                cgst_list[i][f"CGST@ {value[0]} %"] += value[1]
                                break

                            if len(cgst_list) == i + 1 and not matched:
                                cgst_list.append({f"CGST@ {value[0]} %": value[1]})
                else:
                    if value[0] != 0:
                        cgst_list.append({f"CGST@ {value[0]} %": value[1]})
>>>>>>> c06d5715bf2a77bcea50c88e7b8892c64b139710

        if "IGST" in tax.account_head and tax.tax_amount != 0:
            tax_details = json.loads(tax.item_wise_tax_detail)
            values = list(tax_details.values())

            for value in values:

                if igst_list:

                    matched = False

                    for i in range (0, len(igst_list), 1):

<<<<<<< HEAD
                        if igst_list[i].get(f"IGST@ {value[0]} %"):
                            igst_list[i][f"IGST@ {value[0]} %"] += value[1]
                            break

                        if len(igst_list) == i + 1 and not matched:
                            igst_list.append({f"IGST@ {value[0]} %": value[1]})
                else:
                    igst_list.append({f"IGST@ {value[0]} %": value[1]})
=======
                        if value[0] != 0:

                            if igst_list[i].get(f"IGST@ {value[0]} %"):
                                igst_list[i][f"IGST@ {value[0]} %"] += value[1]
                                break

                            if len(igst_list) == i + 1 and not matched:
                                igst_list.append({f"IGST@ {value[0]} %": value[1]})
                else:
                    if value[0] != 0:
                        igst_list.append({f"IGST@ {value[0]} %": value[1]})
>>>>>>> c06d5715bf2a77bcea50c88e7b8892c64b139710

        if "TCS" in tax.account_head and tax.tax_amount != 0:
            tax_details = json.loads(tax.item_wise_tax_detail)
            values = list(tax_details.values())

            for value in values:
                tcs_list.append({f"TCS@ {value[0]} ": value[1]})
        
    key = []
    value = []

    if cgst_list and sgst_list:

        key.append("Taxable Value")
        value.append(f'{round(doc.net_total, 2): .2f}')

        for i in range(0, len(sgst_list), 1):
            key.append(list(sgst_list[i].keys())[0])
            
            final_value = f'{round(list(sgst_list[i].values())[0], 2): .2f}'
            value.append(final_value)


            key.append(list(cgst_list[i].keys())[0])

            final_value = f'{round(list(cgst_list[i].values())[0], 2): .2f}'
            value.append(final_value)

        if tcs_list:
            key.append(list(tcs_list[0].keys())[0])
            
            final_value = f'{round(list(tcs_list[0].values())[0], 2): .2f}'
            value.append(final_value)

    elif igst_list:

        key.append("Taxable Value")
        value.append(f'{round(doc.net_total, 2): .2f}')

        for igst in igst_list:
            key.append(list(igst.keys())[0])

            final_value = f'{round(list(igst.values())[0], 2): .2f}'
            value.append(final_value)

        if tcs_list:
            key.append(list(tcs_list[0].keys())[0])

            final_value = f'{round(list(tcs_list[0].values())[0], 2): .2f}'
            value.append(final_value)

    elif tcs_list:

        key.append("Taxable Value")
        value.append(f'{round(doc.net_total, 2): .2f}')

        key.append(list(tcs_list[0].keys())[0])

        final_value = f'{round(list(tcs_list[0].values())[0], 2): .2f}'
        value.append(final_value)

    return key, value
