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
function html(frm){
	let html = frm.$wrapper.find('div[data-fieldname="hotel_html"]')[0]
    html.innerHTML=''
	var p=[]
	if(frm.doc.hotel_table.length > 0){
		var h_html = `
		<html>
			<table>
				<tr>
					<th>
						Options
					</th>
					`
					for(let i=0;i<frm.doc.hotel_table.length;i++){
						h_html += `		
								<td>
									<input type="text" value="${frm.doc.hotel_table[i].option}" id="option"+${i} name="option"+${1}>
								</td>
								`
					}
					h_html += `	
				</tr>
				<tr>
					<th>
						Hotel Name
					</th>
					`
					for(let i=0;i<frm.doc.hotel_table.length;i++){
						h_html += `		
								<td>
									<input type="text" value="${frm.doc.hotel_table[i].hotel_name}" id="hotel_name"+${i} name="hotel_name"+${i}>
								</td>
								`
					}
					h_html += `	
				</tr>
				<tr>
					<th>
						No of Nights
					</th>
					`
					for(let i=0;i<frm.doc.hotel_table.length;i++){
						h_html += `		
								<td>
									<input type="text" value="${frm.doc.hotel_table[i].no_of_nights}" id="no_of_nights"+${i} name="no_of_nights"+${i}>
								</td>
								`
					}
					h_html += `	
				</tr>
				<tr>
					<th>
						Room Category 
					</th>
					`
					for(let i=0;i<frm.doc.hotel_table.length;i++){
						h_html += `		
								<td>
									<input type="text" value="${frm.doc.hotel_table[i].room_category}" id="room_category"+${i} name="room_category"+${i}>
								</td>
								`
					}
					h_html += `	
				</tr>
				<tr>
					<th>
						Meal Preference 
					</th>
					`
					for(let i=0;i<frm.doc.hotel_table.length;i++){
						h_html += `		
								<td>
									<input type="text" value="${frm.doc.hotel_table[i].meal_preference}" id="meal_preference"+${i} name="meal_preference"+${i}>
								</td>
								`
					}
					h_html += `	
				</tr>
				<tr>
					<th>
						Supplier
					</th>
					`
					for(let i=0;i<frm.doc.hotel_table.length;i++){
						h_html += `		
								<td>
									<input type="text" value="${frm.doc.hotel_table[i].supplier}" id="supplier"+${i} name="supplier"+${i}>
								</td>
								`
					}
					h_html += `	
				</tr>
			<table>
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
	}
	form = new frappe.ui.FieldGroup({
		fields: p,
		body: html
	});
	form.make()
}