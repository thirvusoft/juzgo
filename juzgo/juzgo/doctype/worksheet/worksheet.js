// Copyright (c) 2024, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Worksheet', {
	onload: async function(frm){
		let data=`<table style="font-size:14px; border:1px solid black;width:100%">

			<tr style="font-weight:bold; border:1px solid black; padding:5px;">
				<td style="border:1px solid black; padding:5px;">
				<center>
					Desc
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					Option 1
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					Option 2
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					Option 3
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					Option 4
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					Option 5
				</center>
				</td>
			</tr>
			<tr style="font-weight:bold; border:1px solid black; padding:5px;">
				<td style="border:1px solid black; padding:5px;">
				<center>
					Inclusions
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
				</center>
			</td>
			</tr>
			`
			await frappe.call({
				method:"juzgo.juzgo.doctype.worksheet.worksheet.accomadation",
				args:{doc:frm.doc},
				callback: function(r){
					data += 			`
					<tr style="border:1px solid black; padding:5px;">
						<td style="border:1px solid black; padding:5px;">
						<center>
							Accommodation Details
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[0]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[1]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[2]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[3]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[4]+`
						</center>
						</td>

					`
				}
			})
			await frappe.call({
				method:"juzgo.juzgo.doctype.worksheet.worksheet.sighting_details",
				args:{doc:frm.doc},
				callback: function(r){
					data += 			`
					<tr style="border:1px solid black; padding:5px;">
						<td style="border:1px solid black; padding:5px;">
						<center>
							Sightseeing Details
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[0]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[1]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[2]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[3]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[4]+`
						</center>
						</td>

					`
				}
			})
			await frappe.call({
				method:"juzgo.juzgo.doctype.worksheet.worksheet.vehicle_details",
				args:{doc:frm.doc},
				callback: function(r){
					data += 			`
					<tr style="border:1px solid black; padding:5px;">
						<td style="border:1px solid black; padding:5px;">
						<center>
							Vehicle Details
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[0]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[1]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[2]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[3]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[4]+`
						</center>
						</td>

					`
				}
			})
			await frappe.call({
				method:"juzgo.juzgo.doctype.worksheet.worksheet.optional_tours",
				args:{doc:frm.doc},
				callback: function(r){
					data += 			`
					<tr style="border:1px solid black; padding:5px;">
						<td style="border:1px solid black; padding:5px;">
						<center>
							Optional tours
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[0]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[1]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[2]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[3]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[4]+`
						</center>
						</td>

					`
				}
			})
			await frappe.call({
				method:"juzgo.juzgo.doctype.worksheet.worksheet.complementory",
				args:{doc:frm.doc},
				callback: function(r){
					data += 			`
					<tr style="border:1px solid black; padding:5px;">
						<td style="border:1px solid black; padding:5px;">
						<center>
							Complimentaries
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[0]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[1]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[2]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[3]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[4]+`
						</center>
						</td>

					`
				}
			})
			await frappe.call({
				method:"juzgo.juzgo.doctype.worksheet.worksheet.miscellenous_details",
				args:{doc:frm.doc},
				callback: function(r){
					data += 			`
					<tr style="border:1px solid black; padding:5px;">
						<td style="border:1px solid black; padding:5px;">
						<center>
							Miscellaneous
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[0]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[1]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[2]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[3]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[4]+`
						</center>
						</td>

					`
				}
			})
			data +=
			`<tr style="font-weight:bold; border:1px solid black; padding:5px;">
				<td style="border:1px solid black; padding:5px;" colspan="6">
					<center>
						Net Selling Prices
					</center>
				</td>
			</tr>`
			await frappe.call({
				method:"juzgo.juzgo.doctype.worksheet.worksheet.adult_double",
				args:{doc:frm.doc},
				callback: function(r){
					data += 			`
					<tr style="border:1px solid black; padding:5px;">
						<td style="border:1px solid black; padding:5px;">
						<center>
							Adult Double
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[0]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[1]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[2]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[3]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[4]+`
						</center>
						</td>

					`
				}
			})
			await frappe.call({
				method:"juzgo.juzgo.doctype.worksheet.worksheet.adult_single",
				args:{doc:frm.doc},
				callback: function(r){
					data += 			`
					<tr style="border:1px solid black; padding:5px;">
						<td style="border:1px solid black; padding:5px;">
						<center>
							Adult Single
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[0]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[1]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[2]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[3]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[4]+`
						</center>
						</td>

					`
				}
			})
			await frappe.call({
				method:"juzgo.juzgo.doctype.worksheet.worksheet.adult_triple",
				args:{doc:frm.doc},
				callback: function(r){
					data += 			`
					<tr style="border:1px solid black; padding:5px;">
						<td style="border:1px solid black; padding:5px;">
						<center>
							Adult Triple
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[0]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[1]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[2]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[3]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[4]+`
						</center>
						</td>

					`
				}
			})
			await frappe.call({
				method:"juzgo.juzgo.doctype.worksheet.worksheet.cnb",
				args:{doc:frm.doc},
				callback: function(r){
					data += 			`
					<tr style="border:1px solid black; padding:5px;">
						<td style="border:1px solid black; padding:5px;">
						<center>
							CNB
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[0]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[1]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[2]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[3]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[4]+`
						</center>
						</td>

					`
				}
			})
			await frappe.call({
				method:"juzgo.juzgo.doctype.worksheet.worksheet.cwb",
				args:{doc:frm.doc},
				callback: function(r){
					data += 			`
					<tr style="border:1px solid black; padding:5px;">
						<td style="border:1px solid black; padding:5px;">
						<center>
							CWB
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[0]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[1]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[2]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[3]+`
						</center>
						</td>
						<td style="border:1px solid black; padding:5px;">
						<center>
						`+ r.message[4]+`
						</center>
						</td>

					`
				}
			})
		data += `</table>`
		frm.get_field("html").$wrapper.html( data);
	}
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
	option_1: function(frm,cdt,cdn) {
		cal_complimentaries(frm,cdt,cdn)
	},
	option_2: function(frm,cdt,cdn) {
		cal_complimentaries(frm,cdt,cdn)
	},
	option_3: function(frm,cdt,cdn) {
		cal_complimentaries(frm,cdt,cdn)
	},
	option_4: function(frm,cdt,cdn) {
		cal_complimentaries(frm,cdt,cdn)
	},
	option_5: function(frm,cdt,cdn) {
		cal_complimentaries(frm,cdt,cdn)
	},
});

function cal_complimentaries(frm,cdt,cdn){
	let doc = frm.doc
    let total_cost_price = 0
	var option_1 = 0 
	var option_2 = 0 
	var option_3 = 0 
	var option_4 = 0 
	var option_5 = 0
	doc.complimentaries.forEach( i =>{
		total_cost_price += i.cost_price
		if(i.option_1){
			option_1 += i.cost_price
		}
		if(i.option_2){
			option_2 += i.cost_price
		}
		if(i.option_3){
			option_3 += i.cost_price
		}
		if(i.option_4){
			option_4 += i.cost_price
		}
		if(i.option_5){
			option_5 += i.cost_price
		}
	})

	frm.set_value("total_cost_price",total_cost_price)
	refresh_field("total_cost_price")
	frm.set_value("complimentarie_option_1",option_1)
	refresh_field("complimentarie_option_1")
	frm.set_value("complimentarie_option_2",option_2)
	refresh_field("complimentarie_option_2")
	frm.set_value("complimentarie_option_3",option_3)
	refresh_field("complimentarie_option_3")
	frm.set_value("complimentarie_option_4",option_4)
	refresh_field("complimentarie_option_4")
	frm.set_value("complimentarie_option_5",option_5)
	refresh_field("complimentarie_option_5")
}