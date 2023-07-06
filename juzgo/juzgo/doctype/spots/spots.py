# Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document

class Spots(Document):
	pass
@frappe.whitelist()
def img_preview(table=None,image=None,des=None,menu=None):
	if table:
		layout_height = frappe.db.get_single_value("System Settings","layout_height") or "Auto"
		image_width = frappe.db.get_single_value("System Settings","image_width") or "250px"
		image_height = frappe.db.get_single_value("System Settings","image_height") or "Auto"
		table = json.loads(table)
		html=''
		html='''
			<html>
			<head>
			<style>
			div.gallery {
			border: 1px solid #ccc;
			}

			div.gallery:hover {
			border: 1px solid #777;
			box-shadow: 0 22px 26px 0 rgba(0,0,0,0.24),0 27px 60px 0 rgba(0,0,0,0.19);
			}

			div.gallery img {
			width:'''+image_width+''';
			height:'''+image_height+''';
			}

			div.desc {
			padding: 5px;
			width: '''+image_width+''';
			height: 50px;
			text-align: center;
			overflow:scroll;
			}

			* {
			box-sizing: border-box;
			}

			.responsive {
			padding: 0 6px 6px;
			height:'''+layout_height+''';
			float: left;
			}

			

			.clearfix:after {
			content: "";
			display: table;
			clear: both;
			}
			</style>
			</head>
			<body>
			<h5>Image Preview</h5>
			'''
		if len(table) == 0:
			html = html+ f''' <p style="font-size:12;color:red">No Image</p> '''
		for i in table:
			html = html+ f''' 
				<div class="responsive">
				<div class="gallery">
					<a target="_blank" href="{i.get(image)}">
					<img src="{i.get(image)}" alt="No Image" >
					</a>
					<div class="desc">{"Menu :- "+i.get(menu)+"<br>Description :- " if i.get(menu) else ""}{i.get(des)}</div>
				</div>
				</div>
			'''
		html = html + '''
			<div class="clearfix"></div>
			</body>
			</html>
		'''
			
		return html
	
@frappe.whitelist()
def exist_list(name,doctype,field):
    master_name=frappe.db.get_all(doctype, filters={field:["Like", "%"+name+"%"]}, fields=["name",field])
    return master_name