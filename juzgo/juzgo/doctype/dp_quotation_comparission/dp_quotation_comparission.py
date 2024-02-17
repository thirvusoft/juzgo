# Copyright (c) 2024, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DPQuotationcomparission(Document):
	def validate(self):
		if self.detailing_page:
			detailing_page = frappe.get_doc("Detailing Page",self.detailing_page)
			hotel_list = []
			spots_list = []
			for j in detailing_page.hotels:
				if j.hotel_name not in hotel_list and j.hotel_name != '':
					hotel_list.append(j.hotel_name)
			for j in detailing_page.spots:
				if j.spots not in spots_list and j.spots != '':
					spots_list.append(j.spots)
			if detailing_page.supplier:
				for i in detailing_page.supplier:
					if i.hotels and len(self.hotel) == 0:
						for j in hotel_list:
							self.append("hotel",dict(
								supplier = i.supplier,
								hotel = j
							))
					if i.spots and len(self.spots) == 0:
						for j in spots_list:
							self.append("spots",dict(
								supplier = i.supplier,
								spots = j
							))
