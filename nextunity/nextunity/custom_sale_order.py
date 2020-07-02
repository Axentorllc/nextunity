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
	print("*******************************************",sales_order)
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
		print("###########################################################",work_order.name)
		work_odr = work_order.name
		name = i.get("name")
		frappe.db.sql("""  update `tabSales Order Item` set work_order = %(work_odr)s where name = %(name)s """,{"work_odr":work_odr,"name":name})
	return [p.name for p in out]