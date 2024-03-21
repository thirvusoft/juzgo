frappe.ui.form.on("Quotation", {
    refresh: function(frm){
        if(frm.doc.custom_airtickets_details_){
            let amount = 0
            frm.doc.custom_airtickets_details_.forEach(rows => {
                amount +=rows.amount
            });
            if(frm.doc.custom_total_airtickets_amount != amount)frm.set_value('custom_total_airtickets_amount', amount)
        }
        if(frm.doc.custom_package_details){
            let amount = 0
            let total_pack = 0
            
            frm.doc.custom_package_details.forEach(rows => {
                amount += rows.amount
                total_pack = amount+frm.doc.custom_other_charges_total
            });
            if(frm.doc.custom_total_package_amount != total_pack)frm.set_value('custom_total_package_amount', total_pack)
        }
        var items_total = 0
        var taxes_total = 0
        if(frm.doc.items){
            frm.doc.items.forEach(rows => {
                if(rows.item_tax_template)items_total += rows.net_amount
            });
        }
        if(frm.doc.taxes){
            for (let i = 0; i < frm.doc.taxes.length; i++) {
                if(frm.doc.taxes[i].charge_type == "Actual"){
                    break
                }
                if(frm.doc.taxes[i].charge_type == "On Net Total"){
                    taxes_total += frm.doc.taxes[i].tax_amount
                }
            } 
        }
        frm.set_value('tcs_amount', ((taxes_total+items_total)/100)*5)
    },
    validate: function(frm){
        if(frm.doc.custom_airtickets_details_){
            let amount = 0
            {
                frm.doc.custom_airtickets_details_.forEach(rows => {
                    amount +=rows.amount
                    frm.set_value('custom_total_airtickets_amount', amount)
                });
            }
        }
        if(frm.doc.custom_package_details){
            let amount = 0
            let total_pack = 0
            {
                frm.doc.custom_package_details.forEach(rows => {
                    amount += rows.amount
                    total_pack = amount+frm.doc.custom_other_charges_total
                    frm.set_value('custom_total_package_amount', total_pack)
                });
            }
        }
        if(frm.doc.custom_other_charges){
            let amount = 0
            {
                frm.doc.custom_other_charges.forEach(rows => {
                    amount +=rows.total_amount
                    frm.set_value('custom_other_charges_total', amount)
                });
            }
        }
        if(frm.doc.custom_other_charges_total){
            let amount = 0
            let total_pack=0
            {
                frm.doc.custom_package_details.forEach(rows => {
                    amount +=rows.amount
                    total_pack=amount+frm.doc.custom_other_charges_total
                    frm.set_value('custom_total_package_amount', total_pack)
                });
            }
        }
        if(frm.doc.custom_total_package_amount){
            let account_pay = frm.doc.custom_total_package_amount*frm.doc.custom_package_amount_percentage/100
            frm.set_value("custom_package_amount_account", account_pay)
        }
        if(frm.doc.custom_package_amount_account){
            let cash_pay=frm.doc.custom_total_package_amount-frm.doc.custom_package_amount_account
            frm.set_value("custom_package_amount_cash", cash_pay)
        }
        if(frm.doc.custom_total_airtickets_amount){
            let total_account_amount = frm.doc.custom_total_airtickets_amount + frm.doc.custom_package_amount_account
            frm.set_value("custom_net_payable_in_account", total_account_amount)
        }
        if(frm.doc.custom_total_airtickets_amount && frm.doc.custom_package_amount_account){
            let total_account_amount = frm.doc.custom_total_airtickets_amount + frm.doc.custom_package_amount_account
            frm.set_value("custom_net_payable_in_account", total_account_amount)
        }
        if(frm.doc.custom_package_amount_cash){
            let total_cash=frm.doc.custom_package_amount_cash
            frm.set_value("custom_net_payable_in_cash",total_cash)
        }
        if(frm.doc.custom_net_payable_in_account && frm.doc.custom_net_payable_in_cash){
            let nettotal=frm.doc.custom_net_payable_in_account +frm.doc.custom_net_payable_in_cash
            frm.set_value("custom_net_total", nettotal)
        }
        if(frm.doc.custom_package_amount_percentage){
            let account_pay = frm.doc.custom_total_package_amount*frm.doc.custom_package_amount_percentage/100
            frm.set_value("custom_package_amount_account", account_pay)
            let cash_percent=100-frm.doc.custom_package_amount_percentage
            frm.set_value("custom_cash_percentage", cash_percent)
        }
        if(frm.doc.custom_package_amount_account){
            let cash_percent_pay=frm.doc.custom_total_package_amount*(100-frm.doc.custom_package_amount_percentage)/100
            frm.set_value("custom_package_cash_percentage", cash_percent_pay)
        }
    },
    custom_total_package_amount: function(frm){
        if(frm.doc.custom_total_package_amount){
            let account_pay = frm.doc.custom_total_package_amount*frm.doc.custom_package_amount_percentage/100
            frm.set_value("custom_package_amount_account", account_pay)
        }
    },
    custom_package_amount_account: function(frm){
        if(frm.doc.custom_package_amount_account){
            let cash_pay=frm.doc.custom_total_package_amount-frm.doc.custom_package_amount_account
            frm.set_value("custom_package_amount_cash", cash_pay)
        }
        if(frm.doc.custom_package_amount_account){
            let cash_percent_pay=frm.doc.custom_total_package_amount*(100-frm.doc.custom_package_amount_percentage)/100
            frm.set_value("custom_package_cash_percentage", cash_percent_pay)
        }
    },
    custom_total_airtickets_amount: function(frm){
        if(frm.doc.custom_total_airtickets_amount && frm.doc.custom_package_amount_account){
            let total_account_amount = frm.doc.custom_total_airtickets_amount + frm.doc.custom_package_amount_account
            frm.set_value("custom_net_payable_in_account", total_account_amount)
        }
        if(frm.doc.custom_total_airtickets_amount){
            let total_account_amount = frm.doc.custom_total_airtickets_amount + frm.doc.custom_package_amount_account
            frm.set_value("custom_net_payable_in_account", total_account_amount)
        }
    },
    custom_package_amount_cash: function(frm){
        if(frm.doc.custom_package_amount_cash){
            let total_cash=frm.doc.custom_package_amount_cash
            frm.set_value("custom_net_payable_in_cash",total_cash)
        }
    },
    custom_net_payable_in_account: function(frm){
        if(frm.doc.custom_net_payable_in_account && frm.doc.custom_net_payable_in_cash){
            let nettotal=frm.doc.custom_net_payable_in_account +frm.doc.custom_net_payable_in_cash
            frm.set_value("custom_net_total", nettotal)
        }
    },
    custom_net_payable_in_cash: function(frm){
        if(frm.doc.custom_net_payable_in_account && frm.doc.custom_net_payable_in_cash){
            let nettotal=frm.doc.custom_net_payable_in_account +frm.doc.custom_net_payable_in_cash
            frm.set_value("custom_net_total", nettotal)
        }
    },
    custom_package_amount_percentage: function(frm){
        if(frm.doc.custom_package_amount_percentage){
            let account_pay = frm.doc.custom_total_package_amount*frm.doc.custom_package_amount_percentage/100
            frm.set_value("custom_package_amount_account", account_pay)
            let cash_percent=100-frm.doc.custom_package_amount_percentage
            frm.set_value("custom_cash_percentage", cash_percent)
        }
    },
    custom_other_charges_total: function(frm){
        if(frm.doc.custom_other_charges_total){
            let amount = 0
            let total_pack=0
            {
                frm.doc.custom_package_details.forEach(rows => {
                    amount +=rows.amount
                    total_pack=amount+frm.doc.custom_other_charges_total
                    frm.set_value('custom_total_package_amount', total_pack)
                });
            }
        }
    }
})
frappe.ui.form.on("Airtickets", {
    amount: function(frm, cdt, cdn){
        let amount = 0
        let row = locals[cdt][cdn];
        {
            frm.doc.custom_airtickets_details_.forEach(rows => {
                amount +=rows.amount
                frm.set_value('custom_total_airtickets_amount', amount)
            });
        }
    }
})
frappe.ui.form.on("Packages", {
    amount: function(frm, cdt, cdn){
        let amount = 0
        let total_pack=0
        let row = locals[cdt][cdn];
        {
            frm.doc.custom_package_details.forEach(rows => {
                amount +=rows.amount+frm.doc.custom_other_charges_total
                total_pack=amount
                frm.set_value('custom_total_package_amount', total_pack)
            });
        }
    }
})
frappe.ui.form.on("Other Charge", {
   
    amount: function(frm, cdt, cdn){
        let row = locals[cdt][cdn];
        if(row.percent == 0.00 || row.percent == null){
            frappe.model.set_value(cdt, cdn, "total_amount", flt(row.amount));
        } else{
            frappe.model.set_value(cdt, cdn, "total_amount", flt((row.percent/100)*parseInt(row.amount)));
        }

    },
    percent:function(frm, cdt, cdn){
        let row = locals[cdt][cdn];
        if(row.percent == 0.00 || row.percent == null){
            frappe.model.set_value(cdt, cdn, "total_amount", flt(row.amount));
        } else{
            frappe.model.set_value(cdt, cdn, "total_amount", flt((row.percent/100)*parseInt(row.amount)));
        }

    },
    total_amount: function(frm, cdt, cdn){
        let amount = 0
        let row = locals[cdt][cdn];
        {
            frm.doc.custom_other_charges.forEach(rows => {
                amount +=rows.total_amount
                frm.set_value('custom_other_charges_total', amount)
            });
        }
    }
})