// Copyright (c) 2024, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Worksheet', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Worksheet Options', {
	view_edit: function(frm,cdt,cdn) {
		let row = locals[cdt][cdn]
		if (!row.options)frappe.throw("Kindly Select Worksheet Option...", frappe.MandatoryError)
		window.open("/app/worksheet-option/"+row.options, '_blank')
	},
	duplicate: function(frm,cdt,cdn){
		let row = locals[cdt][cdn]
	
		if (!row.options)frappe.throw("Kindly Select Worksheet Option...", frappe.MandatoryError)
		frm.call({
			method:"juzgo.juzgo.doctype.worksheet.worksheet.duplicate",
			args:{
				option: row.options
			},
			callback: function(r){
				let child = frm.add_child("worksheet_options");
				child.options = r.message.name
				refresh_field("worksheet_options")
				frm.save()
				window.open("/app/worksheet-option/"+r.message.name, '_blank')
			}
		})
	}
});

frappe.ui.form.on('Optional Tours Worksheet', {
	optional_tours_remove: function(frm,cdt,cdn) {
		cal_optional_tours(frm,cdt,cdn)
	},
	currency: function(frm,cdt,cdn) {
		cal_optional_tours(frm,cdt,cdn)
	},
	adult: function(frm,cdt,cdn) {
		cal_optional_tours(frm,cdt,cdn)
	},
	child: function(frm,cdt,cdn) {
		cal_optional_tours(frm,cdt,cdn)
	},
	option_1: function(frm,cdt,cdn) {
		cal_optional_tours(frm,cdt,cdn)
	},
	option_2: function(frm,cdt,cdn) {
		cal_optional_tours(frm,cdt,cdn)
	},
	option_3: function(frm,cdt,cdn) {
		cal_optional_tours(frm,cdt,cdn)
	},
	option_4: function(frm,cdt,cdn) {
		cal_optional_tours(frm,cdt,cdn)
	},
	option_5: function(frm,cdt,cdn) {
		cal_optional_tours(frm,cdt,cdn)
	},
});

async function cal_optional_tours(frm,cdt,cdn){
	let doc = frm.doc
	doc["option_1_adult"] = doc["option_2_adult"] = doc["option_3_adult"] = doc["option_4_adult"] = doc["option_5_adult"] = doc["option_1_child"] = doc["option_2_child"] = doc["option_3_child"] = doc["option_4_child"] = doc["option_5_child"] = 0
    let currency ={"INR":1}
        
	doc["currency"].forEach( i =>{
		currency[i["currency"]] = i["workout_based_on"]
	})
	
	doc["optional_tours"].forEach( i =>{
		if (i["option_1"]){
			doc["option_1_adult"] = doc["option_1_adult"]+ (i["adult"] * currency[i["currency"]])
            doc["option_1_child"] = doc["option_1_child"]+ (i["child"] * currency[i["currency"]])
		}
        if (i["option_2"]){
			doc["option_2_adult"] = doc["option_2_adult"]+ (i["adult"] * currency[i["currency"]])
            doc["option_2_child"] = doc["option_2_child"]+ (i["child"] * currency[i["currency"]])
		}
        if (i["option_3"]){
			doc["option_3_adult"] = doc["option_3_adult"]+ (i["adult"] * currency[i["currency"]])
            doc["option_3_child"] = doc["option_3_child"]+ (i["child"] * currency[i["currency"]])
		}
        if (i["option_4"]){
			doc["option_4_adult"] = doc["option_4_adult"]+ (i["adult"] * currency[i["currency"]])
            doc["option_4_child"] = doc["option_4_child"]+ (i["child"] * currency[i["currency"]])
		}
        if (i["option_5"]){
			doc["option_5_adult"] = doc["option_5_adult"]+ (i["adult"] * currency[i["currency"]])
            doc["option_5_child"] = doc["option_5_child"]+ (i["child"] * currency[i["currency"]])
		}
	})
	frm.set_value("option_1_adult",doc["option_1_adult"])
	refresh_field("option_1_adult")
	frm.set_value("option_1_child",doc["option_1_child"])
	refresh_field("option_1_child")
	frm.set_value("option_2_adult",doc["option_2_adult"])
	refresh_field("option_2_adult")
	frm.set_value("option_2_child",doc["option_2_child"])
	refresh_field("option_2_child")
	frm.set_value("option_3_adult",doc["option_3_adult"])
	refresh_field("option_3_adult")
	frm.set_value("option_3_child",doc["option_3_child"])
	refresh_field("option_3_child")
	frm.set_value("option_4_adult",doc["option_4_adult"])
	refresh_field("option_4_adult")
	frm.set_value("option_4_child",doc["option_4_child"])
	refresh_field("option_4_child")
	frm.set_value("option_5_adult",doc["option_5_adult"])
	refresh_field("option_5_adult")
	frm.set_value("option_5_child",doc["option_5_child"])
	refresh_field("option_5_child")
}

frappe.ui.form.on('Complimentaries Worksheet', {
	complimentaries_remove: function(frm,cdt,cdn) {
		cal_complimentaries(frm,cdt,cdn)
	},
	cost_price: function(frm,cdt,cdn) {
		cal_complimentaries(frm,cdt,cdn)
	},
});

function cal_complimentaries(frm,cdt,cdn){
	let doc = frm.doc
    let total_cost_price = 0
	doc.complimentaries.forEach( i =>{
		total_cost_price += i.cost_price
	})
	frm.set_value("total_cost_price",total_cost_price)
	refresh_field("total_cost_price")
}