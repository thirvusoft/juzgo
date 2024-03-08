// Copyright (c) 2024, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Worksheet', {
	onload: async function(frm){
		let opt1=""
		let opt2=""
		let opt3=""
		let opt4=""
		let opt5=""
		await frappe.call({
			method:"juzgo.juzgo.doctype.worksheet.worksheet.option_link",
			args:{doc:frm.doc},
			callback: function(r){
				opt1=r.message[0][0]
				opt2=r.message[1][0]
				opt3=r.message[2][0]
				opt4=r.message[3][0]
				opt5=r.message[4][0]
			}
		})
		let data=`<table style="font-size:14px; border:1px solid black;width:100%">
			<tr style="font-weight:bold; border:1px solid black; padding:5px;">
				<th style="border:1px solid black; padding:5px;">
				<center>
					Desc
				</center>
				</th>
				<th style="border:1px solid black; padding:5px;">
				<center>`
				if (opt1){
					data+=`<a href= "/app/worksheet-option/`+opt1+`" target="_blank"> Option 1</a>`
				}else{
					data+=`Option 1`
				}
				data +=`
				</center>
				</th>
				<th style="border:1px solid black; padding:5px;">
				<center>`
				if (opt2){
					data+=`<a href= "/app/worksheet-option/`+opt2+`" target="_blank"> Option 2</a>`
				}else{
					data+=`Option 2`
				}
				data +=`
				</center>
				</th>
				<th style="border:1px solid black; padding:5px;">
				<center>`
				if (opt3){
					data+=`<a href= "/app/worksheet-option/`+opt3+`" target="_blank"> Option 3</a>`
				}else{
					data+=`Option 3`
				}
				data +=`
				</center>
				</th>
				<th style="border:1px solid black; padding:5px;">
				<center>`
				if (opt4){
					data+=`<a href= "/app/worksheet-option/`+opt4+`" target="_blank"> Option 4</a>`
				}else{
					data+=`Option 4`
				}
				data +=`
				</center>
				</th>
				<th style="border:1px solid black; padding:5px;">
				<center>`
				if (opt5){
					data+=`<a href= "/app/worksheet-option/`+opt5+`" target="_blank"> Option 5</a>`
				}else{
					data+=`Option 5`
				}
				data +=`
				</center>
				</th>
			</tr>
			<tr style="font-weight:bold; border:1px solid black; padding:5px;">
				<th style="border:1px solid black; padding:5px;" colspan="6">
				<center>
					Inclusions
				</center>
				</th>
			</tr>`
				
			await frappe.call({
				method:"juzgo.juzgo.doctype.worksheet.worksheet.worksheet_inclusions",
				args:{doc:frm.doc},
				callback: function(r){
					if(r.message[0]){
						for(var i=0;r.message[1].length>i;i++){
							data += 			
							`
							<tr style="border:1px solid black; padding:5px;">
								<th style="border:1px solid black; padding:5px;font-weight:bold;">
								<center>
									`+Object.keys(r.message[0][i])[0]+`
								</center>
								</th>`
								
							for(var j=0;Object.values(r.message[0][i])[0].length>j;j++){
								data += 			
								`<td style="border:1px solid black; padding:5px;">
									`+ Object.values(r.message[0][i])[0][j].descriptions+`
								</td>`
							}
							data += 			
								`</tr>`
						}
					}
				}
			})
			await frappe.call({
				method:"juzgo.juzgo.doctype.worksheet.worksheet.optional_tours",
				args:{doc:frm.doc},
				callback: function(r){
					data += 			`
					<tr style="border:1px solid black; padding:5px;">
						<th style="border:1px solid black; padding:5px;font-weight:bold;">
						<center>
							Optional tours
						</center>
						</th>
						<td style="border:1px solid black; padding:5px;">
						`+ r.message[0]+`
						</td>
						<td style="border:1px solid black; padding:5px;">
						`+ r.message[1]+`
						</td>
						<td style="border:1px solid black; padding:5px;">
						`+ r.message[2]+`
						</td>
						<td style="border:1px solid black; padding:5px;">
						`+ r.message[3]+`
						</td>
						<td style="border:1px solid black; padding:5px;">
						`+ r.message[4]+`
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
						<th style="border:1px solid black; padding:5px;font-weight:bold;">
						<center>
							Complimentaries
						</center>
						</th>
						<td style="border:1px solid black; padding:5px;">
						`+ r.message[0]+`
						</td>
						<td style="border:1px solid black; padding:5px;">
						`+ r.message[1]+`
						</td>
						<td style="border:1px solid black; padding:5px;">
						`+ r.message[2]+`
						</td>
						<td style="border:1px solid black; padding:5px;">
						`+ r.message[3]+`
						</td>
						<td style="border:1px solid black; padding:5px;">
						`+ r.message[4]+`
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
						<th style="border:1px solid black; padding:5px;font-weight:bold;">
						<center>
							Miscellaneous
						</center>
						</th>
						<td style="border:1px solid black; padding:5px;">
						`+ r.message[0]+`
						</td>
						<td style="border:1px solid black; padding:5px;">
						`+ r.message[1]+`
						</td>
						<td style="border:1px solid black; padding:5px;">
						`+ r.message[2]+`
						</td>
						<td style="border:1px solid black; padding:5px;">
						`+ r.message[3]+`
						</td>
						<td style="border:1px solid black; padding:5px;">
						`+ r.message[4]+`
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
				method:"juzgo.juzgo.doctype.worksheet.worksheet.worksheet_cost_calculations",
				args:{doc:frm.doc},
				callback: function(r){
					if(r.message[0]){
						for(var i=0;r.message[1].length>i;i++){
							data += 			
							`
							<tr style="border:1px solid black; padding:5px;font-weight:bold;">
								<th style="border:1px solid black; padding:5px;">
								<center>
									`+Object.keys(r.message[0][i])[0]+`
								</center>
								</th>`
								
							for(var j=0;Object.values(r.message[0][i])[0].length>j;j++){
								data += 			
								`<td style="border:1px solid black; padding:5px;">
									<center>
									`+ Object.values(r.message[0][i])[0][j].cost+`
									</center>
								</td>`
							}
							data += 			
								`</tr>`
						}
					}
				}
			})
		data += `</table>`
		frm.get_field("html").$wrapper.html( data);
	},
	refresh: function(frm) {
		frm.set_query('complimentaries',"complimentaries", function(doc){
            return {
                filters:{
                    'item_group':"Complimentaries",
                }
            }
        })

	}
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