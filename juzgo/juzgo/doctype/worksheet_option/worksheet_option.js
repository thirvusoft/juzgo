// Copyright (c) 2024, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt
var currency = {}
var map_field_currency = {}
frappe.ui.form.on('Worksheet Option', {
	refresh: function(frm) {
		if (frm.doc.worksheet){
			fetch_worksheet(frm)
			fetch_worksheet_details(frm)
		}
	},
	worksheet: function(frm) {
		fetch_worksheet(frm)
		fetch_worksheet_details(frm)
	},
	reduce_foc_cost_in_inr: function(frm){
		frm.set_value("final_total_amount",((frm.doc.total_in_inr || 0) - (frm.doc.reduce_foc_cost_in_inr || 0)))
	},
	total_in_inr: function(frm){
		frm.set_value("final_total_amount",((frm.doc.total_in_inr || 0) - (frm.doc.reduce_foc_cost_in_inr || 0)))
	},
	total_no_of_pax: function(frm){
		frm.set_value("amount_per_pax",((frm.doc.final_total_amount || 0) / (frm.doc.total_no_of_pax || 1)))
	},
	final_total_amount: function(frm){
		frm.set_value("amount_per_pax",((frm.doc.final_total_amount || 0) / (frm.doc.total_no_of_pax || 1)))
	},
	amount_per_pax: function(frm){
		frm.doc.cost_calculations.forEach( ele =>{
			frappe.model.set_value(ele.doctype,ele.name,"tour_manager_share",frm.doc.amount_per_pax || 0)
		})
	}
});

function fetch_worksheet(frm){
	frm.call({
		method:"juzgo.juzgo.doctype.worksheet_option.worksheet_option.fetch_default_value",
		args:{
			doc: frm.doc
		},
		callback: function(r){
			if(frm.doc.cost_calculations.length == 0){
				r.message[0].forEach( ele =>{
					let child = frm.add_child("cost_calculations");
					child.details = ele
				})
				refresh_field("cost_calculations")
			}
			if(frm.doc.tour_manager_share.length == 0){
				r.message[1].forEach( ele =>{
					let child = frm.add_child("tour_manager_share");
					child.share_item = ele
				})
				refresh_field("tour_manager_share")
			}
			if(frm.doc.inclusions_worksheet.length == 0){
				r.message[2].forEach( ele =>{
					let child = frm.add_child("inclusions_worksheet");
					child.details = ele.details
					child.descriptions = ele.descriptions
				})
				refresh_field("inclusions_worksheet")
			}
			let s_no = 1
			currency = r.message[3]
			for(var key in r.message[3]) {
				frm.fields_dict.cost_calculations.grid.update_docfield_property('cost_'+s_no,'label',key);
				// frm.fields_dict.cost_calculations.grid.update_docfield_property('cost_'+s_no,'options',key);
				map_field_currency['cost_'+s_no] = key
				s_no++
			}
			  
			if(frm.doc.__unsaved)frm.save()
		}
	})
}

function fetch_worksheet_details(frm){
	frm.call({
		method:"juzgo.juzgo.doctype.worksheet_option.worksheet_option.fetch_worksheet_details",
		args:{
			doc: frm.doc
		},
		callback: function(r){
			if(r.message){
				r.message.forEach( ele =>{
					frappe.model.set_value(ele.doctype,ele.name,"optional_tours_in_inr",ele.optional_tours_in_inr)
					frappe.model.set_value(ele.doctype,ele.name,"complimentaries_in_inr",ele.complimentaries_in_inr)
				})
			}
			  
			if(frm.doc.__unsaved)frm.save()
		}
	})
}

frappe.ui.form.on('Cost Calculations', {
	cost_1: function(frm,cdt,cdn){
		cost_cal(frm,cdt,cdn)
	},
	cost_2: function(frm,cdt,cdn){
		cost_cal(frm,cdt,cdn)
	},
	cost_3: function(frm,cdt,cdn){
		cost_cal(frm,cdt,cdn)
	},
	cost_4: function(frm,cdt,cdn){
		cost_cal(frm,cdt,cdn)
	},
	cost_5: function(frm,cdt,cdn){
		cost_cal(frm,cdt,cdn)
	},
	cost_6: function(frm,cdt,cdn){
		cost_cal(frm,cdt,cdn)
	},
	total_in_inr: function(frm,cdt,cdn){
		cp_in_inr_cal(frm,cdt,cdn)
	},
	optional_tours_in_inr: function(frm,cdt,cdn){
		cp_in_inr_cal(frm,cdt,cdn)
	},
	complimentaries_in_inr: function(frm,cdt,cdn){
		cp_in_inr_cal(frm,cdt,cdn)
	},
	miscellaneous_in_inr: function(frm,cdt,cdn){
		cp_in_inr_cal(frm,cdt,cdn)
	},
	tour_manager_share: function(frm,cdt,cdn){
		cp_in_inr_cal(frm,cdt,cdn)
	},
	cp_in_inr: function(frm,cdt,cdn){
		sp_in_inr_cal(frm,cdt,cdn)
	},
	margins: function(frm,cdt,cdn){
		sp_in_inr_cal(frm,cdt,cdn)
	},
});

function cost_cal(frm,cdt,cdn){
	var row = locals[cdt][cdn]
	var total_cost = 0
	for(let i=1;i<=6;i++){
		total_cost += ((row['cost_'+i] || 0) * (currency[map_field_currency['cost_'+i]] || 0))
	}
	frappe.model.set_value(cdt,cdn,"total_in_inr",total_cost)
}

function cp_in_inr_cal(frm,cdt,cdn){
	var row = locals[cdt][cdn]
	var total_cp  = (row.total_in_inr || 0)+(row.optional_tours_in_inr || 0)+(row.complimentaries_in_inr || 0)+(row.miscellaneous_in_inr || 0)
	frappe.model.set_value(cdt,cdn,"cp_in_inr",total_cp)
}

function sp_in_inr_cal(frm,cdt,cdn){
	var row = locals[cdt][cdn]
	var total_sp  = (row.cp_in_inr || 0)+(row.margins || 0)
	frappe.model.set_value(cdt,cdn,"sp_in_inr",total_sp)
}

frappe.ui.form.on('Tour Manager Share Worksheet', {
	tour_manager_share_remove: function(frm,cdt,cdn) {
		cal_tour_manager_share(frm,cdt,cdn)
	},
	amount_in_inr: function(frm,cdt,cdn) {
		cal_tour_manager_share(frm,cdt,cdn)
	},
});

function cal_tour_manager_share(frm,cdt,cdn){
	let doc = frm.doc
    let total_price = 0

	doc.tour_manager_share.forEach( i =>{
		total_price += i.amount_in_inr
	})

	frm.set_value("total_in_inr",total_price)
	refresh_field("total_in_inr")
}