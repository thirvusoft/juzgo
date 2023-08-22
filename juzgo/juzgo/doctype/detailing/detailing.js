// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt
var form

frappe.ui.form.on('Detailing', {
	refresh: function(frm) {
		if(!frm.is_new()){
            html(frm)
        }
	}
});
function contentchild(ele){
	if(ele.name == "copy"){
		if(ele.checked){
			console.log(ele.value)
			let hotel_name,no_of_nights,room_category,meal_preference,supplier
			cur_frm.doc.hotel_table.forEach(e => {
				if(e.hotel_id == ele.value){
					cur_frm.doc.hotel_table.forEach(copy =>{
						if(copy.option == "Opt 1"){
							hotel_name = copy.hotel_name
							no_of_nights = copy.no_of_nights
							room_category = copy.room_category
							meal_preference = copy.meal_preference
							supplier = copy.supplier
						}
					})
				}
			})
			frappe.model.set_value("Demo cc child table", ele.id, 'hotel_name', hotel_name);
			frappe.model.set_value("Demo cc child table", ele.id, 'no_of_nights', no_of_nights);
			frappe.model.set_value("Demo cc child table", ele.id, 'room_category',room_category );
			frappe.model.set_value("Demo cc child table", ele.id, 'meal_preference', meal_preference);
			frappe.model.set_value("Demo cc child table", ele.id, 'supplier', supplier);
			frappe.model.set_value("Demo cc child table", ele.id, ele.name, 1);
		}
		else{
			frappe.model.set_value("Demo cc child table", ele.id, 'hotel_name', '');
			frappe.model.set_value("Demo cc child table", ele.id, 'no_of_nights', '');
			frappe.model.set_value("Demo cc child table", ele.id, 'room_category', '');
			frappe.model.set_value("Demo cc child table", ele.id, 'meal_preference', '');
			frappe.model.set_value("Demo cc child table", ele.id, 'supplier', '');
			frappe.model.set_value("Demo cc child table", ele.id, ele.name, 0);
		}
		cur_frm.save()
	}else{
		frappe.model.set_value("Demo cc child table", ele.id, ele.name, ele.value);
	}
}
function add_hotel(){
	var h_id = Math.random().toString(36).substring(2,7);
	for (let i =1; i<6; i++){
		var row = cur_frm.add_child('hotel_table');
		row.option = "Opt "+i.toString();
		row.hotel_id = h_id;
	}
	refresh_field('hotel_table')
	cur_frm.save()
} 
function remove_hotel(hotel_id){
	var hotel_table = cur_frm.doc.hotel_table
	cur_frm.doc.hotel_table = []
	for (let i = 0; i < hotel_table.length; i++) {
		if(hotel_table[i].hotel_id !== hotel_id)
			cur_frm.doc.hotel_table.push(hotel_table[i])
	}
	if(cur_frm.doc.delete_rows == 1){
		cur_frm.set_value("delete_rows",0)
	} else {
		cur_frm.set_value("delete_rows",1)
	}
	cur_frm.refresh_field('hotel_table');
	cur_frm.save()
}
function copy_hotel(hotel_id){
	let hotel_name,no_of_nights,room_category,meal_preference,supplier
	cur_frm.doc.hotel_table.forEach(ele => {
		if(ele.hotel_id == hotel_id){
			cur_frm.doc.hotel_table.forEach(copy =>{
				if(copy.option == "Opt 1"){
					hotel_name = copy.hotel_name
					no_of_nights = copy.no_of_nights
					room_category = copy.room_category
					meal_preference = copy.meal_preference
					supplier = copy.supplier
				}
			})
		}
	})
	cur_frm.doc.hotel_table.forEach(ele => {
		if(ele.hotel_id == hotel_id){
			cur_frm.doc.hotel_table.forEach(copy =>{
				if(copy.option != "Opt 1"){
					frappe.model.set_value(ele.doctype, ele.name, 'hotel_name', hotel_name);
					frappe.model.set_value(ele.doctype, ele.name, 'no_of_nights', no_of_nights);
					frappe.model.set_value(ele.doctype, ele.name, 'room_category', room_category);
					frappe.model.set_value(ele.doctype, ele.name, 'meal_preference', meal_preference);
					frappe.model.set_value(ele.doctype, ele.name, 'supplier', supplier);
					frappe.model.set_value(ele.doctype, ele.name, 'copy', 1);
				}
			})
		}
	})
	cur_frm.save()
}
frappe.content = contentchild
frappe.add_hotel = add_hotel
frappe.remove_hotel = remove_hotel
frappe.copy_hotel = copy_hotel

// -------------------------------------------

function spotchild(ele){
	console.log(ele.name,ele.id)
	if(ele.name == "copy"){
		if(ele.checked){
			let basic_spots
			cur_frm.doc.basic_spots.forEach(e => {
				if(e.spots_id == ele.value){
					cur_frm.doc.basic_spots.forEach(copy =>{
						if(copy.option == "Opt 1"){
							basic_spots = copy.basic_spots
						}
					})
				}
			})
			frappe.model.set_value("Detailing Basic Spots", ele.id, 'basic_spots', basic_spots);
			frappe.model.set_value("Detailing Basic Spots", ele.id, ele.name, 1);
		}
		else{
			frappe.model.set_value("Detailing Basic Spots", ele.id, 'basic_spots', '');
			frappe.model.set_value("Detailing Basic Spots", ele.id, ele.name, 0);
		}
		cur_frm.save()
	}else{
		frappe.model.set_value("Detailing Basic Spots", ele.id, ele.name, ele.value);
	}
}
function add_spot(){
	var h_id = Math.random().toString(36).substring(2,7);
	for (let i =1; i<6; i++){
		var row = cur_frm.add_child('basic_spots');
		row.option = "Opt "+i.toString();
		row.spots_id = h_id;
	}
	refresh_field('basic_spots')
	cur_frm.save()
} 
function remove_spot(spots_id){
	var basic_spots = cur_frm.doc.basic_spots
	cur_frm.doc.basic_spots = []
	for (let i = 0; i < basic_spots.length; i++) {
		if(basic_spots[i].spots_id !== spots_id)
			cur_frm.doc.basic_spots.push(basic_spots[i])
	}
	if(cur_frm.doc.delete_rows == 1){
		cur_frm.set_value("delete_rows",0)
	} else {
		cur_frm.set_value("delete_rows",1)
	}
	cur_frm.refresh_field('basic_spots');
	cur_frm.save()
}
function copy_spot(spots_id){
	let basic_spots
	cur_frm.doc.basic_spots.forEach(ele => {
		if(ele.spots_id == spots_id){
			cur_frm.doc.basic_spots.forEach(copy =>{
				if(copy.option == "Opt 1"){
					basic_spots = copy.basic_spots
				}
			})
		}
	})
	cur_frm.doc.basic_spots.forEach(ele => {
		if(ele.spots_id == spots_id){
			cur_frm.doc.hotel_table.forEach(copy =>{
				if(copy.option != "Opt 1"){
					frappe.model.set_value(ele.doctype, ele.name, 'basic_spots', basic_spots);
					frappe.model.set_value(ele.doctype, ele.name, 'copy', 1);
				}
			})
		}
	})
	cur_frm.save()
}
frappe.spotchild = spotchild
frappe.add_spots = add_spot
frappe.remove_spots = remove_spot
frappe.copy_spots = copy_spot

// -------------------------------------------

function vehiclechild(ele){
	if(ele.name == "copy"){
		if(ele.checked){
			let vehicle
			cur_frm.doc.vehicle.forEach(e => {
				if(e.vehicle_id == ele.value){
					cur_frm.doc.vehicle.forEach(copy =>{
						if(copy.option == "Opt 1"){
							vehicle = copy.vehicle
						}
					})
				}
			})
			frappe.model.set_value("Vehicle in Detailing", ele.id, 'vehicle', vehicle);
			frappe.model.set_value("Vehicle in Detailing", ele.id, ele.name, 1);
		}
		else{
			frappe.model.set_value("Vehicle in Detailing", ele.id, 'vehicle', '');
			frappe.model.set_value("Vehicle in Detailing", ele.id, ele.name, 0);
		}
		cur_frm.save()
	}else{
		frappe.model.set_value("Vehicle in Detailing", ele.id, ele.name, ele.value);
	}
}
function add_vehicle(){
	var h_id = Math.random().toString(36).substring(2,7);
	for (let i =1; i<6; i++){
		var row = cur_frm.add_child('vehicle');
		row.option = "Opt "+i.toString();
		row.vehicle_id = h_id;
	}
	refresh_field('vehicle')
	cur_frm.save()
} 
function remove_vehicle(vehicle_id){
	var vehicle = cur_frm.doc.vehicle
	cur_frm.doc.vehicle = []
	for (let i = 0; i < vehicle.length; i++) {
		if(vehicle[i].vehicle_id !== vehicle_id)
			cur_frm.doc.vehicle.push(vehicle[i])
	}
	if(cur_frm.doc.delete_rows == 1){
		cur_frm.set_value("delete_rows",0)
	} else {
		cur_frm.set_value("delete_rows",1)
	}
	cur_frm.refresh_field('vehicle');
	cur_frm.save()
}
function copy_vehicle(vehicle_id){
	let vehicle
	cur_frm.doc.vehicle.forEach(ele => {
		if(ele.vehicle_id == vehicle_id){
			cur_frm.doc.vehicle.forEach(copy =>{
				if(copy.option == "Opt 1"){
					vehicle = copy.vehicle
				}
			})
		}
	})
	cur_frm.doc.vehicle.forEach(ele => {
		if(ele.vehicle_id == vehicle_id){
			cur_frm.doc.hotel_table.forEach(copy =>{
				if(copy.option != "Opt 1"){
					frappe.model.set_value(ele.doctype, ele.name, 'vehicle', vehicle);
					frappe.model.set_value(ele.doctype, ele.name, 'copy', 1);
				}
			})
		}
	})
	cur_frm.save()
}
frappe.vehiclechild = vehiclechild
frappe.add_vehicle = add_vehicle
frappe.remove_vehicle = remove_vehicle
frappe.copy_vehicle = copy_vehicle

// ---------------------------------
function restaurantchild(ele){
	if(ele.name == "copy"){
		if(ele.checked){
			let restaurant
			cur_frm.doc.restaurant.forEach(e => {
				if(e.restaurant_id == ele.value){
					cur_frm.doc.restaurant.forEach(copy =>{
						if(copy.option == "Opt 1"){
							restaurant = copy.restaurant
						}
					})
				}
			})
			frappe.model.set_value("Restaurant in Detailing", ele.id, 'restaurant', restaurant);
			frappe.model.set_value("Restaurant in Detailing", ele.id, ele.name, 1);
		}
		else{
			frappe.model.set_value("Restaurant in Detailing", ele.id, 'restaurant', '');
			frappe.model.set_value("Restaurant in Detailing", ele.id, ele.name, 0);
		}
		cur_frm.save()
	}else{
		frappe.model.set_value("Restaurant in Detailing", ele.id, ele.name, ele.value);
	}
}
function add_restaurant(){
	var h_id = Math.random().toString(36).substring(2,7);
	for (let i =1; i<6; i++){
		var row = cur_frm.add_child('restaurant');
		row.option = "Opt "+i.toString();
		row.restaurant_id = h_id;
	}
	refresh_field('restaurant')
	cur_frm.save()
} 
function remove_restaurant(restaurant_id){
	var restaurant = cur_frm.doc.restaurant
	cur_frm.doc.restaurant = []
	for (let i = 0; i < restaurant.length; i++) {
		if(restaurant[i].restaurant_id !== restaurant_id)
			cur_frm.doc.restaurant.push(restaurant[i])
	}
	if(cur_frm.doc.delete_rows == 1){
		cur_frm.set_value("delete_rows",0)
	} else {
		cur_frm.set_value("delete_rows",1)
	}
	cur_frm.refresh_field('restaurant');
	cur_frm.save()
}
function copy_restaurant(restaurant_id){
	let restaurant
	cur_frm.doc.restaurant.forEach(ele => {
		if(ele.restaurant_id == restaurant_id){
			cur_frm.doc.restaurant.forEach(copy =>{
				if(copy.option == "Opt 1"){
					restaurant = copy.restaurant
				}
			})
		}
	})
	cur_frm.doc.restaurant.forEach(ele => {
		if(ele.restaurant_id == restaurant_id){
			cur_frm.doc.hotel_table.forEach(copy =>{
				if(copy.option != "Opt 1"){
					frappe.model.set_value(ele.doctype, ele.name, 'restaurant', restaurant);
					frappe.model.set_value(ele.doctype, ele.name, 'copy', 1);
				}
			})
		}
	})
	cur_frm.save()
}
frappe.restaurantchild = restaurantchild
frappe.add_restaurant = add_restaurant
frappe.remove_restaurant = remove_restaurant
frappe.copy_restaurant = copy_restaurant

//-------------------------------------------
function buschild(ele){
	if(ele.name == "copy"){
		if(ele.checked){
			let bus
			cur_frm.doc.bus.forEach(e => {
				if(e.bus_id == ele.value){
					cur_frm.doc.bus.forEach(copy =>{
						if(copy.option == "opt 1"){
							bus = copy.bus
						}
					})
				}
			})
			frappe.model.set_value("Bus in Detailing", ele.id, 'bus', bus);
			frappe.model.set_value("Bus in Detailing", ele.id, ele.name, 1);
		}
		else{
			frappe.model.set_value("Bus in Detailing", ele.id, 'bus', '');
			frappe.model.set_value("Bus in Detailing", ele.id, ele.name, 0);
		}
		cur_frm.save()
	}else{
		frappe.model.set_value("Bus in Detailing", ele.id, ele.name, ele.value);
	}
}
function add_bus(){
	var h_id = Math.random().toString(36).substring(2,7);
	for (let i =1; i<6; i++){
		var row = cur_frm.add_child('bus');
		row.option = "Option "+i.toString();
		row.bus_id = h_id;
	}
	refresh_field('bus')
	cur_frm.save()
} 
function remove_bus(bus_id){
	var bus = cur_frm.doc.bus
	cur_frm.doc.bus = []
	for (let i = 0; i < bus.length; i++) {
		if(bus[i].bus_id !== bus_id)
			cur_frm.doc.bus.push(bus[i])
	}
	if(cur_frm.doc.delete_rows == 1){
		cur_frm.set_value("delete_rows",0)
	} else {
		cur_frm.set_value("delete_rows",1)
	}
	cur_frm.refresh_field('bus');
	cur_frm.save()
}
function copy_bus(bus_id){
	let bus
	cur_frm.doc.bus.forEach(ele => {
		if(ele.bus_id == bus_id){
			cur_frm.doc.bus.forEach(copy =>{
				if(copy.option == "opt 1"){
					bus = copy.bus
				}
			})
		}
	})
	cur_frm.doc.bus.forEach(ele => {
		if(ele.bus_id == bus_id){
			cur_frm.doc.hotel_table.forEach(copy =>{
				if(copy.option != "opt 1"){
					frappe.model.set_value(ele.doctype, ele.name, 'bus', bus);
					frappe.model.set_value(ele.doctype, ele.name, 'copy', 1);
				}
			})
		}
	})
	cur_frm.save()
}
frappe.buschild = buschild
frappe.add_bus = add_bus
frappe.remove_bus = remove_bus
frappe.copy_bus = copy_bus

//-------------------------------------------
function cruisechild(ele){
	if(ele.name == "copy"){
		if(ele.checked){
			let cruise
			cur_frm.doc.cruise.forEach(e => {
				if(e.cruise_id == ele.value){
					cur_frm.doc.cruise.forEach(copy =>{
						if(copy.option == "opt 1"){
							cruise = copy.cruise
						}
					})
				}
			})
			frappe.model.set_value("Cruise in Detailing", ele.id, 'cruise', cruise);
			frappe.model.set_value("Cruise in Detailing", ele.id, ele.name, 1);
		}
		else{
			frappe.model.set_value("Cruise in Detailing", ele.id, 'cruise', '');
			frappe.model.set_value("Cruise in Detailing", ele.id, ele.name, 0);
		}
		cur_frm.save()
	}else{
		frappe.model.set_value("Cruise in Detailing", ele.id, ele.name, ele.value);
	}
}
function add_cruise(){
	var h_id = Math.random().toString(36).substring(2,7);
	for (let i =1; i<6; i++){
		var row = cur_frm.add_child('cruise');
		row.option = "Opt "+i.toString();
		row.cruise_id = h_id;
	}
	refresh_field('cruise')
	cur_frm.save()
} 
function remove_cruise(cruise_id){
	var cruise = cur_frm.doc.cruise
	cur_frm.doc.cruise = []
	for (let i = 0; i < cruise.length; i++) {
		if(cruise[i].cruise_id !== cruise_id)
			cur_frm.doc.cruise.push(cruise[i])
	}
	if(cur_frm.doc.delete_rows == 1){
		cur_frm.set_value("delete_rows",0)
	} else {
		cur_frm.set_value("delete_rows",1)
	}
	cur_frm.refresh_field('cruise');
	cur_frm.save()
}
function copy_cruise(cruise_id){
	let cruise
	cur_frm.doc.cruise.forEach(ele => {
		if(ele.cruise_id == cruise_id){
			cur_frm.doc.cruise.forEach(copy =>{
				if(copy.option == "Opt 1"){
					cruise = copy.cruise
				}
			})
		}
	})
	cur_frm.doc.cruise.forEach(ele => {
		if(ele.cruise_id == cruise_id){
			cur_frm.doc.hotel_table.forEach(copy =>{
				if(copy.option != "Opt 1"){
					frappe.model.set_value(ele.doctype, ele.name, 'cruise', cruise);
					frappe.model.set_value(ele.doctype, ele.name, 'copy', 1);
				}
			})
		}
	})
	cur_frm.save()
}
frappe.cruisechild = cruisechild
frappe.add_cruise = add_cruise
frappe.remove_cruise = remove_cruise
frappe.copy_cruise = copy_cruise

async function html(frm){
	let html = frm.$wrapper.find('div[data-fieldname="hotel_html"]')[0]
    html.innerHTML=''
	var hotel_list = []
	frm.doc.hotel_table.forEach(ele => {
		hotel_list.push(ele.hotel_id)
	})
	var hotel_id_list = [...new Set(hotel_list)]
// --------------------
	var spots_list = []
	frm.doc.basic_spots.forEach(ele => {
		spots_list.push(ele.spots_id)
	})
	var spots_id_list = [...new Set(spots_list)]
	
// --------------------
	var vehicle_list = []
	frm.doc.vehicle.forEach(ele => {
		vehicle_list.push(ele.vehicle_id)
	})
	var vehicle_id_list = [...new Set(vehicle_list)]

// --------------------
var restaurant_list = []
frm.doc.restaurant.forEach(ele => {
	restaurant_list.push(ele.restaurant_id)
})
var restaurant_id_list = [...new Set(restaurant_list)]

// --------------------
var bus_list = []
frm.doc.bus.forEach(ele => {
	bus_list.push(ele.bus_id)
})
var bus_id_list = [...new Set(bus_list)]

// --------------------
var cruise_list = []
frm.doc.cruise.forEach(ele => {
	cruise_list.push(ele.cruise_id)
})
var cruise_id_list = [...new Set(cruise_list)]
	
// ------------------------
	var p=[]
	var lists =[]
	var a = await frappe.db.get_list("Hotel Details")
	a.forEach(d=>{
		lists.push(d.name)
	})
	var supplierlist =[]
	var a = await frappe.db.get_list("Supplier")
	a.forEach(d=>{
		supplierlist.push(d.name)
	})
	var spots_lists = []
	var a = await frappe.db.get_list("Spots")
	a.forEach(d=>{
		spots_lists.push(d.name)
	})
	var vehicle_lists = []
	var a = await frappe.db.get_list("Vehicle")
	a.forEach(d=>{
		vehicle_lists.push(d.name)
	})

	var restaurant_lists = []
	var a = await frappe.db.get_list("Restaurant")
	a.forEach(d=>{
		restaurant_lists.push(d.name)
	})

	var bus_lists = []
	var a = await frappe.db.get_list("Bus")
	a.forEach(d=>{
		bus_lists.push(d.name)
	})

	var cruise_lists = []
	var a = await frappe.db.get_list("Cruise")
	a.forEach(d=>{
		cruise_lists.push(d.name)
	})
	// if(frm.doc.hotel_table.length > 0){

		var h_html = `
		<html>
			<style>
				.tablediv{
					float:left;
					width:99%;
				}
				.sidebut{
					float:right;
					width:1%;
					margin-top:6px;
				}
				.addbut{
					clear: both;
					margin:5px;
					text-align: center;  
					width:90%;
				}
				.rows{
					width:100%;
					margin-top:11px;
					border-radius: 5px;
				}
				.trclass{
					border:1px solid black;
				}
				.tdclass{
					border:1px solid black;
				}
				.thclass{
					border:1px solid black;
					background-color:#b3b3b3;
					color:#ffffff;
					font-size:14px;
				}
				.thclass a{
					color:#ffffff;
					padding-right:5px;
				}
				.inputclass{
					width:100%;
					min-height: 37px;
					max-height: 100%;
				}
				.addbutton{
					background-color: #40bf40;
					color: white;
					font-size: 12px;
					font-weight: Bold;
					padding: 6px 12px;
					border: none;
					cursor: pointer;
					border-radius: 5px;
					text-align: center;
					margin: 5px;
					width:70%;
				}
				.rebutton{
					background-color: #ff4d4d;
					color: white;
					font-size: 12px;
					padding: 6px 12px;
					border: none;
					cursor: pointer;
					border-radius: 5px;
					text-align: center;
					margin:2px;
				}
				.copybutton{
					background-color: #b3b300;
					color: white;
					font-size: 12px;
					padding: 6px 12px;
					border: none;
					cursor: pointer;
					border-radius: 5px;
					text-align: center;
					margin:2px;
				}
				.addbutton:hover {
					box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24),0 17px 50px 0 rgba(0,0,0,0.19);
				}
				.rebutton:hover {
					box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24),0 17px 50px 0 rgba(0,0,0,0.19);
				}
				.copybutton:hover {
					box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24),0 17px 50px 0 rgba(0,0,0,0.19);
				}
			</style>
			`
		hotel_id_list.forEach(hotel_id=>{
		h_html +=`
				<div style="width:100%;">
					<div class="tablediv">
						<table class="rows">
							<tr class="trclass">
								<th class="thclass">
									Options
								</th>
								`
								for(let i=0;i<frm.doc.hotel_table.length;i++){
									if(frm.doc.hotel_table[i].hotel_id ==  hotel_id){
										h_html += `		
											<td class="thclass">
												<div style="text-align:center;">
												${frm.doc.hotel_table[i].option}
												${frm.doc.hotel_table[i].option != "Opt 1"?frm.doc.hotel_table[i].copy == 1?'<span style="font-size:11px;font-weight:Bold;color:#b3ffec;">copied(opt1)</span>':'<span style="font-size:11px;font-weight:Bold;color:#ffff80;">To copy(opt1)</span>':''}
												${frm.doc.hotel_table[i].option != "Opt 1"?frm.doc.hotel_table[i].copy == 1?'<input style="background-color:#ffff" type="checkbox" value='+frm.doc.hotel_table[i].hotel_id+' id='+frm.doc.hotel_table[i].name+' name="copy" onchange="frappe.content(this)" checked >':'<input style="background-color:#ffff" type="checkbox" value='+frm.doc.hotel_table[i].hotel_id+' id='+frm.doc.hotel_table[i].name+' name="copy" onchange="frappe.content(this)" >':''}
												</div>
											</td>
											`
										}
									}
								h_html += `	
							</tr>
							<tr class="trclass">
								<th class="thclass">
									<a href='/app/hotel-details/' target='_blank'>Hotel Name</a><a href='/app/hotel-details/new-hotel-details-1' target='_blank'><i>${frappe.utils.icon("small-add")}</i></a>
								</th>
								`
								for(let i=0;i<frm.doc.hotel_table.length;i++){
									if(frm.doc.hotel_table[i].hotel_id ==  hotel_id){
										h_html += `		
												<td class="tdclass">
													<input class="inputclass" type="text" list="hotellist" value="${frm.doc.hotel_table[i].hotel_name || ''}" id=${frm.doc.hotel_table[i].name} name="hotel_name" onchange="frappe.content(this)">
													<datalist id="hotellist">
														<option> </option>
														`
														for (var h = 0; h < lists.length; h++) {
															h_html += '<option value="' + lists[h] + '"> '+lists[h]+' </option>';
														}
														h_html+=`
													</datalist> 
												</td>
											`
										}
									}
								h_html += `	
							</tr>
							<tr class="trclass">
								<th class="thclass">
									No of Nights
								</th>
								`
								for(let i=0;i<frm.doc.hotel_table.length;i++){
									if(frm.doc.hotel_table[i].hotel_id ==  hotel_id){
										h_html += `		
												<td class="tdclass">
													<input class="inputclass" type="text" value="${frm.doc.hotel_table[i].no_of_nights || ''}" id=${frm.doc.hotel_table[i].name} name="no_of_nights" onchange="frappe.content(this)">
												</td>
											`
										}
									}
								h_html += `	
							</tr>
							<tr class="trclass">
								<th class="thclass">
									Room Category 
								</th>
								`
								for(let i=0;i<frm.doc.hotel_table.length;i++){
									if(frm.doc.hotel_table[i].hotel_id ==  hotel_id){
										h_html += `		
												<td class="tdclass">
													<input class="inputclass" type="text" value="${frm.doc.hotel_table[i].room_category || ''}" id=${frm.doc.hotel_table[i].name} name="room_category" onchange="frappe.content(this)">
												</td>
											`
										}
				
									}
								h_html += `	
							</tr>
							<tr class="trclass">
								<th class="thclass">
									Meal Preference 
								</th>
								`
								for(let i=0;i<frm.doc.hotel_table.length;i++){
									if(frm.doc.hotel_table[i].hotel_id ==  hotel_id){
										h_html += `		
												<td class="tdclass">
													<input class="inputclass" type="text" value="${frm.doc.hotel_table[i].meal_preference || ''}" id=${frm.doc.hotel_table[i].name} name="meal_preference" onchange="frappe.content(this)">
												</td>
											`
										}
									}
								h_html += `	
							</tr>
							<tr class="trclass">
								<th class="thclass">
									<a href='/app/supplier/' target='_blank'>Supplier</a><a href='/app/supplier/new-supplier-1' target='_blank'><i>${frappe.utils.icon("small-add")}</i></a>
								</th>
								`
								for(let i=0;i<frm.doc.hotel_table.length;i++){
									if(frm.doc.hotel_table[i].hotel_id ==  hotel_id){
										h_html += `		
												<td class="tdclass">
													<input class="inputclass" type="text" list="supplierlist" value="${frm.doc.hotel_table[i].supplier || ''}" id=${frm.doc.hotel_table[i].name} name="supplier" onchange="frappe.content(this)"> 
													<datalist id="supplierlist">
														<option> </option>
														`
														for (var h = 0; h < supplierlist.length; h++) {
															h_html += '<option value="' + supplierlist[h] + '"> </option>';
														}
														h_html+=`
													</datalist> 
												</td>
											`
										}
									}
								h_html += `	
							</tr>
						</table>
					</div>
				</div>
				<div class="sidebut">
					<button class="copybutton" type="button" onclick="frappe.copy_hotel('${hotel_id}')"><i>${frappe.utils.icon("duplicate")}</i></button>
					<button class="rebutton" type="button" onclick="frappe.remove_hotel('${hotel_id}')"><i>${frappe.utils.icon("delete")}</i></button>
				</div>
				`
			})
			h_html+=`
			<div class="addbut">
				<button class="addbutton" type="button" onclick="frappe.add_hotel()">Add Hotel</button>
			</div>
		</html>
		`
		p.push({
			fieldtype: 'Section Break',
			fieldname: 'h_sb',
			collapsible: 1,
			label:"Hotel Details"
		})
		p.push({
			fieldtype: 'HTML',
			fieldname: 'h_html',
			options :h_html
		})
		

		var s_html = `
		<html>
			`
		spots_id_list.forEach(spots_id=>{
		s_html +=`
				<div style="width:100%;">
					<div class="tablediv">
						<table class="rows">
							<tr class="trclass">
								<th class="thclass">
									Options
								</th>
								`
								for(let i=0;i<frm.doc.basic_spots.length;i++){
									if(frm.doc.basic_spots[i].spots_id ==  spots_id){
										s_html += `		
											<td class="thclass">
												<div style="text-align:center">
												${frm.doc.basic_spots[i].option}
												${frm.doc.basic_spots[i].option != "Opt 1"?frm.doc.basic_spots[i].copy == 1?'<span style="font-size:11px;font-weight:Bold;color:#b3ffec;">copied(opt1)</span>':'<span style="font-size:11px;font-weight:Bold;color:#ffff80;">To copy(opt1)</span>':''}
												${frm.doc.basic_spots[i].option != "Opt 1"?frm.doc.basic_spots[i].copy == 1?'<input type="checkbox" value='+frm.doc.basic_spots[i].spots_id+' id='+frm.doc.basic_spots[i].name+' name="copy" onchange="frappe.spotchild(this)" checked >':'<input style="background-color:#ffff" type="checkbox" value='+frm.doc.basic_spots[i].spots_id+' id='+frm.doc.basic_spots[i].name+' name="copy" onchange="frappe.spotchild(this)" >':''}
												</div>
											</td>
											`
										}
									}
								s_html += `	
							</tr>
							<tr class="trclass">
								<th class="thclass">
								<a href='/app/spots/' target='_blank'>Spots</a><a href='/app/spots/new-spots-1' target='_blank'><i>${frappe.utils.icon("small-add")}</i></a>
								</th>
								`
								for(let i=0;i<frm.doc.basic_spots.length;i++){
									if(frm.doc.basic_spots[i].spots_id ==  spots_id){
										s_html += `		
												<td class="tdclass">
													<input class="inputclass" type="text" list="spotlist" value="${frm.doc.basic_spots[i].basic_spots || ''}" id=${frm.doc.basic_spots[i].name} name="basic_spots" onchange="frappe.spotchild(this)">
													<datalist id="spotlist">
														<option> </option>
														`
														for (var h = 0; h < spots_lists.length; h++) {
															s_html += '<option value="' + spots_lists[h] + '"> '+spots_lists[h]+' </option>';
														}
														s_html+=`
													</datalist> 
												</td>
											`
										}
									}
								s_html += `	
							</tr>
						</table>
					</div>
					<div class="sidebut">
						<button class="copybutton"  type="button" onclick="frappe.copy_spots('${spots_id}')"><i>${frappe.utils.icon("duplicate")}</i></button>
						<button class="rebutton" type="button" onclick="frappe.remove_spots('${spots_id}')">${frappe.utils.icon("delete")}</button>
					</div>
				</div>
				`
			})
			s_html+=`
			<div class="addbut">
				<button class="addbutton" type="button" onclick="frappe.add_spots()">Add Spots</button>
			</div>
		</html>
		`

		p.push({
			fieldtype: 'Section Break',
			fieldname: 's_sb',
			collapsible: 1,
			label:"Spots Details"
		})
		p.push({
			fieldtype: 'HTML',
			fieldname: 's_html',
			options :s_html
		})


		var r_html = `
		<html>
			`
		restaurant_id_list.forEach(restaurant_id=>{
			r_html +=`
					<div style="width:100%;">
						<div class="tablediv">
							<table class="rows">
								<tr class="trclass">
									<th class="thclass">
										Options
									</th>
									`
									for(let i=0;i<frm.doc.restaurant.length;i++){
										if(frm.doc.restaurant[i].restaurant_id ==  restaurant_id){
											r_html += `		
												<td class="thclass">
													<div style="text-align:center">
													<div style="text-align:center">
													${frm.doc.restaurant[i].option}
													${frm.doc.restaurant[i].option != "Opt 1"?frm.doc.restaurant[i].copy == 1?'<span style="font-size:11px;font-weight:Bold;color:#b3ffec;">copied(opt1)</span>':'<span style="font-size:11px;font-weight:Bold;color:#ffff80;">To copy(opt1)</span>':''}
													${frm.doc.restaurant[i].option != "Opt 1"?frm.doc.restaurant[i].copy == 1?'<input type="checkbox" value='+frm.doc.restaurant[i].restaurant_id+' id='+frm.doc.restaurant[i].name+' name="copy" onchange="frappe.restaurantchild(this)" checked >':'<input style="background-color:#ffff" type="checkbox" value='+frm.doc.restaurant[i].restaurant_id+' id='+frm.doc.restaurant[i].name+' name="copy" onchange="frappe.restaurantchild(this)" >':''}
													</div>
												</td>
												`
											}
										}
									r_html += `	
								</tr>
								<tr class="trclass">
									<th class="thclass">
									<a href='/app/restaurant/' target='_blank'>Restaurant</a><a href='/app/restaurant/new-restaurant-1' target='_blank'><i>${frappe.utils.icon("small-add")}</i></a>
									</th>
									`
									for(let i=0;i<frm.doc.restaurant.length;i++){
										if(frm.doc.restaurant[i].restaurant_id ==  restaurant_id){
											r_html += `		
													<td class="tdclass">
														<input class="inputclass" type="text" list="restaurantlist" value="${frm.doc.restaurant[i].restaurant || ''}" id=${frm.doc.restaurant[i].name} name="restaurant" onchange="frappe.restaurantchild(this)">
														<datalist id="restaurantlist">
															<option> </option>
															`
															for (var h = 0; h < restaurant_lists.length; h++) {
																r_html += '<option value="' + restaurant_lists[h] + '"> '+restaurant_lists[h]+' </option>';
															}
															r_html+=`
														</datalist> 
													</td>
												`
											}
										}
									r_html += `	
								</tr>
							</table>
						</div>
						<div class="sidebut">
							<button class="copybutton"  type="button" onclick="frappe.copy_restaurant('${restaurant_id}')"><i>${frappe.utils.icon("duplicate")}</i></button>
							<button class="rebutton" type="button" onclick="frappe.remove_restaurant('${restaurant_id}')">${frappe.utils.icon("delete")}</button>
						</div>
					</div>
					`
				})
				r_html+=`
				<div class="addbut">
					<button class="addbutton" type="button" onclick="frappe.add_restaurant()">Add Restaurant</button>
				</div>
			</html>
			`

		p.push({
			fieldtype: 'Section Break',
			fieldname: 'r_sb',
			collapsible: 1,
			label:"Restaurant Details"
		})
		p.push({
			fieldtype: 'HTML',
			fieldname: 'r_html',
			options :r_html
		})
		
		var v_html = `
		<html>
			`
		vehicle_id_list.forEach(vehicle_id=>{
			v_html +=`
					<div style="width:100%;">
						<div class="tablediv">
							<table class="rows">
								<tr class="trclass">
									<th class="thclass">
										Options
									</th>
									`
									for(let i=0;i<frm.doc.vehicle.length;i++){
										if(frm.doc.vehicle[i].vehicle_id ==  vehicle_id){
											v_html += `		
												<td class="thclass">
													<div style="text-align:center">
													${frm.doc.vehicle[i].option}
													${frm.doc.vehicle[i].option != "Opt 1"?frm.doc.vehicle[i].copy == 1?'<span style="font-size:11px;font-weight:Bold;color:#b3ffec;">copied(opt1)</span>':'<span style="font-size:11px;font-weight:Bold;color:#ffff80;">To copy(opt1)</span>':''}
													${frm.doc.vehicle[i].option != "Opt 1"?frm.doc.vehicle[i].copy == 1?'<input type="checkbox" value='+frm.doc.vehicle[i].vehicle_id+' id='+frm.doc.vehicle[i].name+' name="copy" onchange="frappe.vehiclechild(this)" checked >':'<input style="background-color:#ffff" type="checkbox" value='+frm.doc.vehicle[i].vehicle_id+' id='+frm.doc.vehicle[i].name+' name="copy" onchange="frappe.vehiclechild(this)" >':''}
													</div>
													
												</td>
												`
											}
										}
									v_html += `	
								</tr>
								<tr class="trclass">
									<th class="thclass">
									<a href='/app/vehicle/' target='_blank'>Vehicle</a><a href='/app/vehicle/new-vehicle-1' target='_blank'><i>${frappe.utils.icon("small-add")}</i></a>
									</th>
									`
									for(let i=0;i<frm.doc.vehicle.length;i++){
										if(frm.doc.vehicle[i].vehicle_id ==  vehicle_id){
											v_html += `		
													<td class="tdclass">
														<input class="inputclass" type="text" list="Vehiclelist" value="${frm.doc.vehicle[i].vehicle || ''}" id=${frm.doc.vehicle[i].name} name="vehicle" onchange="frappe.vehiclechild(this)">
														<datalist id="Vehiclelist">
															<option> </option>
															`
															for (var h = 0; h < vehicle_lists.length; h++) {
																v_html += '<option value="' + vehicle_lists[h] + '"> '+vehicle_lists[h]+' </option>';
															}
															v_html+=`
														</datalist> 
													</td>
												`
											}
										}
									v_html += `	
								</tr>
							</table>
						</div>
						<div class="sidebut">
							<button class="copybutton"  type="button" onclick="frappe.copy_vehicle('${vehicle_id}')"><i>${frappe.utils.icon("duplicate")}</i></button>
							<button class="rebutton" type="button" onclick="frappe.remove_vehicle('${vehicle_id}')">${frappe.utils.icon("delete")}</button>
						</div>
					</div>
					`
				})
				v_html+=`
				<div class="addbut">
					<button class="addbutton" type="button" onclick="frappe.add_vehicle()">Add Vehicle</button>
				</div>
			</html>
			`

		p.push({
			fieldtype: 'Section Break',
			fieldname: 'v_sb',
			collapsible: 1,
			label:"Vehicle Details"
		})
		p.push({
			fieldtype: 'HTML',
			fieldname: 'v_html',
			options :v_html
		})

		var c_html = `
		<html>
			`
		cruise_id_list.forEach(cruise_id=>{
			c_html +=`
					<div style="width:100%;">
						<div class="tablediv">
							<table class="rows">
								<tr class="trclass">
									<th class="thclass">
										Options
									</th>
									`
									for(let i=0;i<frm.doc.cruise.length;i++){
										if(frm.doc.cruise[i].cruise_id ==  cruise_id){
											c_html += `		
												<td class="thclass">
													<div style="text-align:center">
													${frm.doc.cruise[i].option}
													${frm.doc.cruise[i].option != "Opt 1"?frm.doc.cruise[i].copy == 1?'<span style="font-size:11px;font-weight:Bold;color:#b3ffec;">copied(opt1)</span>':'<span style="font-size:11px;font-weight:Bold;color:#ffff80;">To copy(opt1)</span>':''}
													${frm.doc.cruise[i].option != "Opt 1"?frm.doc.cruise[i].copy == 1?'<input type="checkbox" value='+frm.doc.cruise[i].cruise_id+' id='+frm.doc.cruise[i].name+' name="copy" onchange="frappe.cruisechild(this)" checked >':'<input style="background-color:#ffff" type="checkbox" value='+frm.doc.cruise[i].cruise_id+' id='+frm.doc.cruise[i].name+' name="copy" onchange="frappe.cruisechild(this)" >':''}
													</div>
													
												</td>
												`
											}
										}
									c_html += `	
								</tr>
								<tr class="trclass">
									<th class="thclass">
									<a href='/app/cruise/' target='_blank'>Cruise</a><a href='/app/cruise/new-cruise-1' target='_blank'><i>${frappe.utils.icon("small-add")}</i></a>
									</th>
									`
									for(let i=0;i<frm.doc.cruise.length;i++){
										if(frm.doc.cruise[i].cruise_id ==  cruise_id){
											c_html += `		
													<td class="tdclass">
														<input class="inputclass" type="text" list="Cruiselist" value="${frm.doc.cruise[i].cruise || ''}" id=${frm.doc.cruise[i].name} name="cruise" onchange="frappe.cruisechild(this)">
														<datalist id="Cruiselist">
															<option> </option>
															`
															for (var h = 0; h < cruise_lists.length; h++) {
																c_html += '<option value="' + cruise_lists[h] + '"> '+cruise_lists[h]+' </option>';
															}
															c_html+=`
														</datalist> 
													</td>
												`
											}
										}
									c_html += `	
								</tr>
							</table>
						</div>
						<div class="sidebut">
							<button class="copybutton"  type="button" onclick="frappe.copy_cruise('${cruise_id}')"><i>${frappe.utils.icon("duplicate")}</i></button>
							<button class="rebutton" type="button" onclick="frappe.remove_cruise('${cruise_id}')">${frappe.utils.icon("delete")}</button>
						</div>
					</div>
					`
				})
				c_html+=`
				<div class="addbut">
					<button class="addbutton" type="button" onclick="frappe.add_cruise()">Add Cruise</button>
				</div>
			</html>
			`
		
		p.push({
			fieldtype: 'Section Break',
			fieldname: 'v_sb',
			collapsible: 1,
			label:"Cruise Details"
		})
		p.push({
			fieldtype: 'HTML',
			fieldname: 'c_html',
			options :c_html
		})

		var b_html = `
		<html>
			`
		bus_id_list.forEach(bus_id=>{
			b_html +=`
					<div style="width:100%;">
						<div class="tablediv">
							<table class="rows">
								<tr class="trclass">
									<th class="thclass">
										Options
									</th>
									`
									for(let i=0;i<frm.doc.bus.length;i++){
										if(frm.doc.bus[i].bus_id ==  bus_id){
											b_html += `		
												<td class="thclass">
													<div style="text-align:center">
													${frm.doc.bus[i].option}
													${frm.doc.bus[i].option != "Opt 1"?frm.doc.bus[i].copy == 1?'<span style="font-size:11px;font-weight:Bold;color:#b3ffec;">copied(opt1)</span>':'<span style="font-size:11px;font-weight:Bold;color:#ffff80;">To copy(opt1)</span>':''}
													${frm.doc.bus[i].option != "Opt 1"?frm.doc.bus[i].copy == 1?'<input type="checkbox" value='+frm.doc.bus[i].bus_id+' id='+frm.doc.bus[i].name+' name="copy" onchange="frappe.buschild(this)" checked >':'<input style="background-color:#ffff" type="checkbox" value='+frm.doc.bus[i].bus_id+' id='+frm.doc.bus[i].name+' name="copy" onchange="frappe.buschild(this)" >':''}
													</div>
													
												</td>
												`
											}
										}
									b_html += `	
								</tr>
								<tr class="trclass">
									<th class="thclass">
									<a href='/app/bus/' target='_blank'>Bus</a><a href='/app/bus/new-bus-1' target='_blank'><i>${frappe.utils.icon("small-add")}</i></a>
									</th>
									`
									for(let i=0;i<frm.doc.bus.length;i++){
										if(frm.doc.bus[i].bus_id ==  bus_id){
											b_html += `		
													<td class="tdclass">
														<input class="inputclass" type="text" list="Buslist" value="${frm.doc.bus[i].bus || ''}" id=${frm.doc.bus[i].name} name="bus" onchange="frappe.buschild(this)">
														<datalist id="Buslist">
															<option> </option>
															`
															for (var h = 0; h < bus_lists.length; h++) {
																b_html += '<option value="' + bus_lists[h] + '"> '+bus_lists[h]+' </option>';
															}
															b_html+=`
														</datalist> 
													</td>
												`
											}
										}
									b_html += `	
								</tr>
							</table>
						</div>
						<div class="sidebut">
							<button class="copybutton"  type="button" onclick="frappe.copy_bus('${bus_id}')"><i>${frappe.utils.icon("duplicate")}</i></button>
							<button class="rebutton" type="button" onclick="frappe.remove_bus('${bus_id}')">${frappe.utils.icon("delete")}</button>
						</div>
					</div>
					`
				})
				b_html+=`
				<div class="addbut">
					<button class="addbutton" type="button" onclick="frappe.add_bus()">Add Bus</button>
				</div>
			</html>
			`
		
		p.push({
			fieldtype: 'Section Break',
			fieldname: 'v_sb',
			collapsible: 1,
			label:"Bus Details"
		})
		p.push({
			fieldtype: 'HTML',
			fieldname: 'b_html',
			options :b_html
		})
		

		
	// }
	form = new frappe.ui.FieldGroup({
		fields: p,
		body: html
	});
	form.make()
}