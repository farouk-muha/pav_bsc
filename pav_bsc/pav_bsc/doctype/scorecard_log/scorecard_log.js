// Copyright (c) 2021, Farouk Muharram and contributors
// For license information, please see license.txt

frappe.ui.form.on('Scorecard Log', {
	refresh: function(frm) {
		frm.set_query("scorecard", function() {
			return {
			   filters: { type: 'Measure'}
		   }
		});
	},
	actual: function(frm) {
		frm.events.calucate_score(frm);
	},
	red_flag: function(frm) {
		frm.events.calucate_score(frm);
	},
	goal: function(frm) {
		frm.events.calucate_score(frm);
	},
	calucate_score: function(frm){
		if(!frm.doc.goal || !frm.doc.red_flag ||!frm.doc.actual)
			return;
		var goal = flt((frm.doc.goal - frm.doc.red_flag), 2);
		var actual = flt((frm.doc.actual - frm.doc.red_flag), 2);
		var percent = flt(((actual / goal) * 10), 2);
		var score;
		if(percent <= 0){
			score = 1;
		}else if(percent > 10){
			score = 10;
		}else{
			score = percent;
		}
		frm.set_value('score', score);
	}
});
