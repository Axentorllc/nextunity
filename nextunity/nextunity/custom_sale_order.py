from __future__ import unicode_literals
import frappe
import json
import frappe.utils
from frappe import _

form_grid_templates = {
	"items": "templates/form_grid/item_grid.html"
}

@frappe.whitelist()
def make_work_orders(items, sales_order, company, project=None):
	'''Make Work Orders against the given Sales Order for the given `items`'''
	items = json.loads(items).get('items')
	out = []

	for i in items:
		if not i.get("bom"):
			frappe.throw(_("Please select BOM against item {0}").format(i.get("item_code")))
		if not i.get("pending_qty"):
			frappe.throw(_("Please select Qty against item {0}").format(i.get("item_code")))

		work_order = frappe.get_doc(dict(
			doctype='Work Order',
			production_item=i['item_code'],
			bom_no=i.get('bom'),
			qty=i['pending_qty'],
			company=company,
			sales_order=sales_order,
			sales_order_item=i['sales_order_item'],
			project=project,
			fg_warehouse=i['warehouse'],
			description=i['description']
		)).insert()
		work_order.set_work_order_operations()
		work_order.save()
		out.append(work_order)
		work_odr = work_order.name
		name = i.get("name")
		pre_record = frappe.db.sql("""  select work_order from `tabSales Order Item`where name = %(name)s """,
					  { "name": name})
		if pre_record[0][0] == "None":
			final_record = work_odr
			frappe.db.sql("""  update `tabSales Order Item` set work_order = %(final_record)s where name = %(name)s """,
						  {"final_record": final_record, "name": name})
		else:
			final_record = pre_record[0][0] +","+"  "+ work_odr
			frappe.db.sql("""  update `tabSales Order Item` set work_order = %(final_record)s where name = %(name)s """,{"final_record":final_record,"name":name})
	return [p.name for p in out]

@frappe.whitelist()
def make_material_req(name):
	pre_result = frappe.db.sql(""" select material_request from `tabSales Order Item` where name = %(name)s """,{"name":name})
	if pre_result[0][0] == "None":
		mat_req =  frappe.db.sql(""" select parent from `tabMaterial Request Item` where sales_order_item = %(name)s """,{"name":name})
		mat_req_id = mat_req[0][0]
		obj = frappe.get_doc("Sales Order Item",name)
		obj.material_request =  mat_req_id
		obj.save()
		obj.submit()
	else:
		mat_req = frappe.db.sql(""" select parent from `tabMaterial Request Item` where sales_order_item = %(name)s """,
								{"name": name})
		mat_req_id = pre_result[0][0]+","+"  "+ mat_req[0][0]
		obj = frappe.get_doc("Sales Order Item", name)
		obj.material_request = mat_req_id
		obj.save()
		obj.submit()



