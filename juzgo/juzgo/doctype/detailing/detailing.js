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
						if(copy.option == "Option 1"){
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
		row.option = "Option "+i.toString();
		row.hotel_id = h_id;
	}
	refresh_field('hotel_table')
	cur_frm.save()
} 
function remove_hotel(hotel_id){
	var row_to_det = []
	cur_frm.doc.hotel_table.forEach(ele => {
		if(ele.hotel_id == hotel_id)
			row_to_det.push(ele.name)
	})
	if(row_to_det){
		for(let i=row_to_det.length;i>0;i--){
			cur_frm.fields_dict.hotel_table.grid.grid_rows_by_docname[row_to_det[i-1]].remove()
		}
	}
	cur_frm.save()
}
function copy_hotel(hotel_id){
	let hotel_name,no_of_nights,room_category,meal_preference,supplier
	cur_frm.doc.hotel_table.forEach(ele => {
		if(ele.hotel_id == hotel_id){
			cur_frm.doc.hotel_table.forEach(copy =>{
				if(copy.option == "Option 1"){
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
				if(copy.option != "Option 1"){
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
						if(copy.option == "Option 1"){
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
		row.option = "Option "+i.toString();
		row.spots_id = h_id;
	}
	refresh_field('basic_spots')
	cur_frm.save()
} 
function remove_spot(spots_id){
	var row_to_det = []
	cur_frm.doc.basic_spots.forEach(ele => {
		if(ele.spots_id == spots_id)
			row_to_det.push(ele.name)
	})
	if(row_to_det){
		for(let i=row_to_det.length;i>0;i--){
			cur_frm.fields_dict.basic_spots.grid.grid_rows_by_docname[row_to_det[i-1]].remove()
		}
	}
	cur_frm.save()
}
function copy_spot(spots_id){
	let basic_spots
	cur_frm.doc.basic_spots.forEach(ele => {
		if(ele.spots_id == spots_id){
			cur_frm.doc.basic_spots.forEach(copy =>{
				if(copy.option == "Option 1"){
					basic_spots = copy.basic_spots
				}
			})
		}
	})
	cur_frm.doc.basic_spots.forEach(ele => {
		if(ele.spots_id == spots_id){
			cur_frm.doc.hotel_table.forEach(copy =>{
				if(copy.option != "Option 1"){
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
	// if(frm.doc.hotel_table.length > 0){

		var h_html = `
		<html>
			`
		hotel_id_list.forEach(hotel_id=>{
		h_html +=`
				<table>
					<tr>
						<th>
							Options
						</th>
						`
						for(let i=0;i<frm.doc.hotel_table.length;i++){
							if(frm.doc.hotel_table[i].hotel_id ==  hotel_id){
								h_html += `		
									<td>
										<div style="text-align:center">
										${frm.doc.hotel_table[i].option != "Option 1"?frm.doc.hotel_table[i].copy == 1?'<input type="checkbox" value='+frm.doc.hotel_table[i].hotel_id+' id='+frm.doc.hotel_table[i].name+' name="copy" onchange="frappe.content(this)" checked >':'<input type="checkbox" value='+frm.doc.hotel_table[i].hotel_id+' id='+frm.doc.hotel_table[i].name+' name="copy" onchange="frappe.content(this)" >':''}
										${frm.doc.hotel_table[i].option}</div>
									</td>
									`
								}
							}
						h_html += `	
					</tr>
					<tr>
						<th>
							Hotel Name
						</th>
						`
						for(let i=0;i<frm.doc.hotel_table.length;i++){
							if(frm.doc.hotel_table[i].hotel_id ==  hotel_id){
								h_html += `		
										<td>
											<input type="text" list="hotellist" value="${frm.doc.hotel_table[i].hotel_name || ''}" id=${frm.doc.hotel_table[i].name} name="hotel_name" onchange="frappe.content(this)"><a href='/app/hotel-details/new-hotel-details-1' target='_blank'><i>${frappe.utils.icon("small-add")}</i></a>
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
					<tr>
						<th>
							No of Nights
						</th>
						`
						for(let i=0;i<frm.doc.hotel_table.length;i++){
							if(frm.doc.hotel_table[i].hotel_id ==  hotel_id){
								h_html += `		
										<td>
											<input type="text" value="${frm.doc.hotel_table[i].no_of_nights || ''}" id=${frm.doc.hotel_table[i].name} name="no_of_nights" onchange="frappe.content(this)">
										</td>
									`
								}
							}
						h_html += `	
					</tr>
					<tr>
						<th>
							Room Category 
						</th>
						`
						for(let i=0;i<frm.doc.hotel_table.length;i++){
							if(frm.doc.hotel_table[i].hotel_id ==  hotel_id){
								h_html += `		
										<td>
											<input type="text" value="${frm.doc.hotel_table[i].room_category || ''}" id=${frm.doc.hotel_table[i].name} name="room_category" onchange="frappe.content(this)">
										</td>
									`
								}
		
							}
						h_html += `	
					</tr>
					<tr>
						<th>
							Meal Preference 
						</th>
						`
						for(let i=0;i<frm.doc.hotel_table.length;i++){
							if(frm.doc.hotel_table[i].hotel_id ==  hotel_id){
								h_html += `		
										<td>
											<input type="text" value="${frm.doc.hotel_table[i].meal_preference || ''}" id=${frm.doc.hotel_table[i].name} name="meal_preference" onchange="frappe.content(this)">
										</td>
									`
								}
							}
						h_html += `	
					</tr>
					<tr>
						<th>
							Supplier
						</th>
						`
						for(let i=0;i<frm.doc.hotel_table.length;i++){
							if(frm.doc.hotel_table[i].hotel_id ==  hotel_id){
								h_html += `		
										<td>
											<input type="text" list="supplierlist" value="${frm.doc.hotel_table[i].supplier || ''}" id=${frm.doc.hotel_table[i].name} name="supplier" onchange="frappe.content(this)"> <a href='/app/supplier/new-supplier-1' target='_blank'><i>${frappe.utils.icon("small-add")}</i></a>
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
				<table>
				<button type="button" onclick="frappe.remove_hotel('${hotel_id}')">Remove Hotel</button>
				<button type="button" onclick="frappe.copy_hotel('${hotel_id}')">Copy All</button>
				`
			})
			h_html+=`
			<button type="button" onclick="frappe.add_hotel()">Add Hotel</button>
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
				<table>
					<tr>
						<th>
							Options
						</th>
						`
						for(let i=0;i<frm.doc.basic_spots.length;i++){
							if(frm.doc.basic_spots[i].spots_id ==  spots_id){
								s_html += `		
									<td>
										<div style="text-align:center">
										${frm.doc.basic_spots[i].option != "Option 1"?frm.doc.basic_spots[i].copy == 1?'<input type="checkbox" value='+frm.doc.basic_spots[i].spots_id+' id='+frm.doc.basic_spots[i].name+' name="copy" onchange="frappe.spotchild(this)" checked >':'<input type="checkbox" value='+frm.doc.basic_spots[i].spots_id+' id='+frm.doc.basic_spots[i].name+' name="copy" onchange="frappe.spotchild(this)" >':''}
										${frm.doc.basic_spots[i].option}</div>
									</td>
									`
								}
							}
						s_html += `	
					</tr>
					<tr>
						<th>
							Spots
						</th>
						`
						for(let i=0;i<frm.doc.basic_spots.length;i++){
							if(frm.doc.basic_spots[i].spots_id ==  spots_id){
								s_html += `		
										<td>
											<input type="text" list="spotlist" value="${frm.doc.basic_spots[i].basic_spots || ''}" id=${frm.doc.basic_spots[i].name} name="basic_spots" onchange="frappe.spotchild(this)"><a href='/app/spots/new-spots-1' target='_blank'><i>${frappe.utils.icon("small-add")}</i></a>
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
				<table>
				<button type="button" onclick="frappe.remove_spots('${spots_id}')">Remove Spots</button>
				<button type="button" onclick="frappe.copy_spots('${spots_id}')">Copy All</button>
				`
			})
			s_html+=`
			<button type="button" onclick="frappe.add_spots()">Add Spots</button>
		</html>
		`

		p.push({
			fieldtype: 'Section Break',
			fieldname: 's_sb',
			collapsible: 1,
			label:"Hotel Details"
		})
		p.push({
			fieldtype: 'HTML',
			fieldname: 's_html',
			options :s_html
		})
	// }
	form = new frappe.ui.FieldGroup({
		fields: p,
		body: html
	});
	form.make()
}