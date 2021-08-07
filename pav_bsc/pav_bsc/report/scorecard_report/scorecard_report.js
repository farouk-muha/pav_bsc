// Copyright (c) 2016, Farouk Muharram and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Scorecard Report"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
	],
	"treeView": true,
	formatter: (value, row, column, data, default_formatter) => {
		value = default_formatter(value, row, column, data);
		if(column.fieldname == "actual"){
			value = `<div style="color:blue">${value}</div>`;
		}else if(column.fieldname == "red_flag"){
			value = `<div style="color:red">${value}</div>`;
		}else if(column.fieldname == "goal"){
			value = `<div style="color:green">${value}</div>`;
		}
		
		 if(column.fieldname == "score"){
			if(data.score > 7){
				value = `<div style="color:green">${value}</div>`;
			}else if(data.score < 4){
				value = `<div style="color:red">${value}</div>`;
			}else {
				value = `<div style="color:blue">${value}</div>`;
			}
		}
		return value;
	},	
}