// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// eslint-disable-next-line
{% include 'erpnext/public/js/controllers/buying.js' %};

frappe.ui.form.on('Material Request', {
	before_submit: function(frm) {
     $.each(frm.doc["items"],function(i, items)
	    {
             if(items.sales_order_item){
                frm.call({
				method: 'nextunity.nextunity.custom_sale_order.make_material_req',
				args: {
					name : items.sales_order_item
				},
				callback: function(r) {
					if(r.message) {
					console.log(r.message);
					}
				}
			});
             }
	    });
	},
});




// for backward compatibility: combine new and previous states
$.extend(cur_frm.cscript, new erpnext.buying.MaterialRequestController({frm: cur_frm}));

function set_schedule_date(frm) {
	if(frm.doc.schedule_date){
		erpnext.utils.copy_value_in_all_rows(frm.doc, frm.doc.doctype, frm.doc.name, "items", "schedule_date");
	}
}
