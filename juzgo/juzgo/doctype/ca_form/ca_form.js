// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('CA Form', {
	temple: function(frm) {
		frappe.call({
			method: "juzgo.juzgo.doctype.ca_form.ca_form.temple_notes",
			args:{
				temple:frm.doc.temple
			},
			callback: function (r) {
				frm.set_df_property("temple_notes","options",r.message)
			},
		})
	},
	first_name:function(frm){
        if (frm.doc.first_name.length >= 3){
            frappe.call({
                method: "juzgo.juzgo.doctype.spots.spots.exist_list",
                args: {
                    "name": frm.doc.first_name,
                    "doctype": frm.doc.doctype,
                    "field": "first_name"
                },
                callback: function (r) {
                    if (r && r.message) {
                        frm.set_df_property(
                            "first_name",
                            "description",
                            ('This Spots Name already exists: {0}', [r.message.map(function (d) {
                                return repl('<a href="/app/ca-form/%(name)s">%(or_name)s</a>', { name: d['name'], or_name: d['first_name'] })
                            }).join(', ')]));
                    }
                },
            })
        } else {
            frm.set_df_property(
                "first_name",
                "description",
                "");
        }
    },
	validate: function(frm){
		add_pax(frm)
		diff_family(frm)
		if(frm.doc.diff_in_cwb<0){
			frappe.throw("Kindly Check CWB")
		}
		if(frm.doc.diff_in_cnb<0){
			frappe.throw("Kindly Check CNB")
		}
		if(frm.doc.diff_in_adult<0){
			frappe.throw("Kindly Check Adult")
		}
		if(frm.doc.diff_in_infants<0){
			frappe.throw("Kindly Check Infants")
		}
		let total_rooms =0
		if(frm.doc.room_preferences){
			for(let i=0;i<frm.doc.room_preferences.length;i++){
				if(frm.doc.room_preferences[i].family){
					total_rooms+=1
				}
			}
			frm.set_value("total_rooms",total_rooms)
		}
		room_preferences_remaining(frm)
	},
	refresh: function(frm) {
		frm.add_custom_button(__('Project'), function() {
			frappe.model.open_mapped_doc({
				method: "juzgo.juzgo.doctype.ca_form.ca_form.make_project",
				frm: cur_frm
			})
		}, "Create");
		frm.set_query("suggested_spots", function () {
			var list = []
			frm.doc.interested_destination.forEach(e => {
				list.push(e.interested_destination_name)
			});
			return {
				filters: {
					destination : ['in',list],
				},
			};
		});
		frm.set_query("temple", function () {
			return {
				filters: {
					is_temple : 1,
				},
			};
		});
		frappe.call({
			method: "juzgo.juzgo.doctype.ca_form.ca_form.temple_notes",
			args:{
				temple:frm.doc.temple
			},
			callback: function (r) {
				frm.set_df_property("temple_notes","options",r.message)
			},
		})
		frappe.call({
			method: "juzgo.juzgo.doctype.ca_form.ca_form.table_preview",
			callback: function (r) {
				frm.set_df_property("passport_doc","options",r.message[0])
				frm.set_df_property("passport_budget_html","options",r.message[1])
				frm.set_value("currency_ref_link",r.message[2])
			},
		})
		option_for_room_preferences(frm)
		room_preferences_remaining(frm)
	},
	nos_of_days: function(frm){
        frm.set_value("no_of_nights",frm.doc.nos_of_days-1)
        auto_end_date(frm)
    },
    no_of_nights: function(frm){
        frm.set_value("nos_of_days",frm.doc.no_of_nights+1)
        auto_end_date(frm)
    },
    travel_start_date: function(frm){
        auto_end_date(frm)
		if(frm.doc.travel_start_date){
			frm.set_value("from_date",frm.doc.travel_start_date)
		}
    },
	travel_end_date: function(frm){
		if(frm.doc.travel_end_date){
			frm.set_value("return_end_date",frm.doc.travel_end_date)
		}
    },
	no_of_childrens: function(frm){
        add_pax(frm)
    },
	child_without_bed: function(frm){
        add_pax(frm)
    },
	no_of_adult: function(frm){
        add_pax(frm)
    },
	no_of_infant: function(frm){
        add_pax(frm)
    },
	diff_in_cwb: function(frm){
        add_pax(frm)
    },
	diff_in_cnb: function(frm){
        add_pax(frm)
    },
	diff_in_adult: function(frm){
        add_pax(frm)
    },
	diff_in_infants: function(frm){
        add_pax(frm)
    },
	no_of_rooms: function(frm){
		if(frm.doc.no_of_rooms>0){
			add_room_preferences(frm,"",0,0,0,0,frm.doc.no_of_rooms)
			frm.set_value("no_of_rooms",0)
		}
	}
});
function option_for_room_preferences(frm){
	var option = []
	if(frm.doc.family_details_table){
		for(let i=0;i<frm.doc.family_details_table.length;i++){
			option.push(frm.doc.family_details_table[i].family);
		}
		// frm.doc.room_preferences.forEach(element => {
		// 	let row = locals[element.doctype][element.name]
		// 	let df = frappe.meta.get_docfield("Room Preferences","family", row.name);
		// 	df.options = option;
		// });
		frm.fields_dict.room_preferences.grid.update_docfield_property(
			'family',
			'options',
			option
			);
	}
	
}
frappe.ui.form.on('Room Preferences', {
	room_preferences_remove:function(frm){
		frm.set_value("total_rooms",frm.doc.room_preferences.length)
	},
	room_preferences_add:function(frm){
		option_for_room_preferences(frm)
	},
	family:function(frm){
		frm.set_value("total_rooms",frm.doc.room_preferences.length)
		room_preferences_remaining(frm)
	},
})
frappe.ui.form.on('Passport Family Table', {
	date_of_birth:function(frm,cdt,cdn){
		let row = locals[cdt][cdn]
        frappe.model.set_value(cdt,cdn,"age",new Date().getFullYear() - new Date(row.date_of_birth).getFullYear())
	},
})
function room_preferences_remaining(frm){
	frappe.call({
		method: "juzgo.juzgo.doctype.ca_form.ca_form.room_preferences_remaining",
		args:{
			room_preferences:frm.doc.room_preferences,
			family_details_table:frm.doc.family_details_table
		},
		callback: function (r) {
			frm.set_df_property("room_preferences_remaining","options",r.message)
		},
	})
}
frappe.ui.form.on('Family Details Table', {
	family_details_table_remove:function(frm){
		diff_family(frm)
	},
	family:function(frm,cdt,cdn){
		let row = locals[cdt][cdn]
		if(row.family){
			for(let i=0;i<frm.doc.family_details_table.length;i++){
				if(row.family.toLowerCase() == frm.doc.family_details_table[i].family.toLowerCase()){
					if (frm.doc.family_details_table[i].idx != row.idx)
					frappe.throw("This Family is already Exist in Row #"+frm.doc.family_details_table[i].idx)
				}
			}
		}
	},
	child_with_bed:function(frm){
		diff_family(frm)
	},
	child_no_bed:function(frm){
		diff_family(frm)
	},
	adult:function(frm){
		diff_family(frm)
	},
	no_of_infants:function(frm){
		diff_family(frm)
	},
	sharing_preferences:function(frm,cdt,cdn){
		let row = locals[cdt][cdn]
		if(row.sharing_preferences == "Not ready to share"){
			add_room_preferences(frm,row.family,row.adult,row.child_with_bed,row.child_no_bed,row.no_of_infants)
		}
	},
})
function add_room_preferences(frm,family,adult,child_with_bed,child_no_bed,no_of_infants,no_of_rooms=0){
	let not_fill = 1
	if(!frm.doc.room_preferences)return;
	for (let i=0;i<frm.doc.room_preferences.length;i++){
		if(frm.doc.room_preferences[i].family == family){
			not_fill = 0
		}
	}
	if(not_fill == 1 && no_of_rooms==0){
		var new_row = frm.add_child('room_preferences')
		new_row.family = family
		new_row.adult = adult
		new_row.child_nb = child_no_bed
		new_row.child_wbed = child_with_bed
		new_row.infants = no_of_infants
	}
	for (let i=0;i<no_of_rooms;i++){
		var new_row = frm.add_child('room_preferences')
		new_row.family = family
		new_row.adult = adult
		new_row.child_nb = child_no_bed
		new_row.child_wbed = child_with_bed
		new_row.infants = no_of_infants
	}
	frm.refresh_field('room_preferences');
}
function auto_end_date(frm){
    if(frm.doc.travel_start_date && frm.doc.no_of_nights){
        frm.set_value("travel_end_date",frappe.datetime.add_days(frm.doc.travel_start_date, frm.doc.no_of_nights))
		frm.set_value("return_end_date",frappe.datetime.add_days(frm.doc.travel_start_date, frm.doc.no_of_nights))
    } else {
        frm.set_value("travel_end_date","")
		frm.set_value("return_end_date","")
    } 
}
function add_pax(frm){
	frm.set_value("no_of_paxs",(frm.doc.no_of_childrens || 0) + (frm.doc.child_without_bed || 0) + (frm.doc.no_of_adult || 0) + (frm.doc.no_of_infant || 0))
}
function diff_family(frm){
	frm.set_value("diff_in_family",(frm.doc.no_of_familys || 0) - (frm.doc.family_details_table.length || 0))
	var diff_in_cwb = 0
	var diff_in_cnb = 0
	var diff_in_adult = 0
	var diff_in_infants = 0
	for (let i=0;i<frm.doc.family_details_table.length;i++){
		diff_in_cwb += frm.doc.family_details_table[i].child_with_bed || 0
		diff_in_cnb += frm.doc.family_details_table[i].child_no_bed || 0
		diff_in_adult += frm.doc.family_details_table[i].adult || 0
		diff_in_infants += frm.doc.family_details_table[i].no_of_infants || 0
	}
	frm.set_value("diff_in_cwb",(frm.doc.no_of_childrens || 0) - (diff_in_cwb || 0))
	frm.set_value("diff_in_cnb",(frm.doc.child_without_bed || 0) - (diff_in_cnb || 0))
	frm.set_value("diff_in_adult",(frm.doc.no_of_adult || 0) - (diff_in_adult || 0))
	frm.set_value("diff_in_infants",(frm.doc.no_of_infant || 0) - (diff_in_infants || 0))
	frm.set_value("diff_in_pax",((frm.doc.diff_in_cwb || 0) + (frm.doc.diff_in_cnb || 0) + (frm.doc.diff_in_adult || 0)))
	if(frm.doc.diff_in_cwb<0){
		frappe.msgprint("Kindly Check CWB")
	}
	if(frm.doc.diff_in_cnb<0){
		frappe.msgprint("Kindly Check CNB")
	}
	if(frm.doc.diff_in_adult<0){
		frappe.msgprint("Kindly Check Adult")
	}
	if(frm.doc.diff_in_infants<0){
		frappe.msgprint("Kindly Check Infants")
	}
}