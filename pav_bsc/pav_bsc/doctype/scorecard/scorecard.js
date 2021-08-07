// Copyright (c) 2021, Farouk Muharram and contributors
// For license information, please see license.txt

frappe.ui.form.on('Scorecard', {
	refresh: function(frm) {
	    frm.events.chk_type(frm);
		frm.set_query("parent_scorecard", function() {
			var type = frm.doc.type;
			var filter;
			if(type == "Perspective"){
			   filter = { type: 'Plan'}
			 }else if(type == "Objective"){
			  filter = { type: 'Perspective'}
			}else if(type == "Measure"){
			   filter = { type: 'Objective'}
			}else{
				filter = { type: ''}
			}
			return {
			   filters: filter
		   }
		});
	},
	type: function(frm) {
		frappe.call({
			method: "get_data",
			doc: frm.doc,
			callback: function(r) {
				console.log(r.message);
			}
			});

	    frm.events.chk_type(frm);
	},

	chk_type: function(frm) {
			if(frm.doc.type == "Plan"){
				frm.set_df_property("parent_scorecard", "reqd", 0);
			 }else{
				frm.set_df_property("parent_scorecard", "reqd", 1);
			}
	}
});
