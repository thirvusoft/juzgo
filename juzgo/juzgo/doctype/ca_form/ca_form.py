# Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document

class CAForm(Document):
	pass

@frappe.whitelist()
def table_preview():
    table_pre = frappe.get_doc("Passport Document", "Passport Document")
    layout_height = frappe.db.get_single_value("System Settings","layout_height") or "Auto"
    image_width = frappe.db.get_single_value("System Settings","image_width") or "250px"
    image_height = frappe.db.get_single_value("System Settings","image_height") or "Auto"
    html = '''
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
			.responsive1 td{
               border-right:1px solid black;
               border-left:1px solid black;
               border-top:1px solid black;
               border-bottom:1px solid black;
			}
			.responsive1 th{
               text-align : center;
               border-right:1px solid black;
               border-left:1px solid black;
               border-top:1px solid black;
               border-bottom:1px solid black;
			}
			.responsive2 td{
               border-right:1px solid black;
               border-left:1px solid black;
               border-top:1px solid black;
               border-bottom:1px solid black;
			}
			.responsive2 th{
               text-align : center;
               border-right:1px solid black;
               border-left:1px solid black;
               border-top:1px solid black;
               border-bottom:1px solid black;
			}
			.clearfix:after {
			content: "";
			display: table;
			clear: both;
			}
            </style>
        </head>
        <body>
            <div class="responsive1">
                <div class="gallery1">
                    <table style = "width: 80%">
                        <tr>
                            <th style = "width: 40%">Passport Document</th>
                            <th>Reference URL</th>
                        </tr>
    '''
    for i in table_pre.passport_document_table:
        # Use <td> for table data, not <div>
        html += f''' 
            <tr>
                <td>{i.document_details}</td>
                <td style = "color:blue"><a href ="{i.notes}" target="_blank">{i.notes}  </a></td>
            </tr>
        '''
    html += '''
                </table>
            </div>
        </div>
                        <br>
                <br>
                 <h5>Image Reference</h5>
    '''
   
              
               
   
    for m in table_pre.passport_image_doc_table:
        # Use <td> for table data, not <div>
        html += f''' 
        
     <div class="responsive">
                <div class="gallery">
                
            <a target="_blank" href="{m.image}">
					<img src="{m.image}" alt="No Image" >
					</a>
					<div class="desc">{m.description or ""}</div>
                                </div>
        </div>
        '''
    html = html +'''
     
        <div class="clearfix"></div>
        </body>
        </html>
    '''

    return html