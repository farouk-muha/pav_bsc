# Copyright (c) 2013, Farouk Muharram and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _

def execute(filters=None):
	if not filters:
		return [], []
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_data(filters):
	scorecard = frappe.db.sql("""SELECT s.name, s.scorecard_name, type, s.describe, s.parent_scorecard, s.weight, s.data_type,
	l.scorecard, l.calendar, l.date, l.actual, l.red_flag, l.goal, l.score
	FROM `tabScorecard` s
	LEFT JOIN `tabScorecard Log` l on s.name = l.scorecard and l.date between %(from_date)s and %(to_date)s
	WHERE 
	s.company = %(company)s
	""", filters, as_dict=True)

	alltree = {}
	count = 0
	for plan in scorecard:
		if plan.type == 'Plan':
			count += 1
			count_plan = count
			alltree[count] = {}
			alltree[count].setdefault(count)
			alltree[count]['name']=plan.name
			alltree[count]['scorecard_name']=plan.scorecard_name
			alltree[count]['type']=plan.type
			alltree[count]['describe']=plan.describe
			alltree[count]['weight']=plan.weight
			alltree[count]['calendar']=plan.calendar
			alltree[count]['date']=plan.date
			alltree[count]['data_type']=plan.data_type
			alltree[count]['actual']=0
			alltree[count]['red_flag']=0
			alltree[count]['goal']=0
			alltree[count]['score']=0
			alltree[count]['parent']=None
			alltree[count]['indent']=0
		else:
			continue
		per_list = []
		for per in scorecard:
			if per.parent_scorecard == plan.name:
				count += 1
				count_per = count
				per_list.append(count)
				alltree[count] = {}
				alltree[count].setdefault(count)
				alltree[count]['name']=per.name
				alltree[count]['scorecard_name']=per.scorecard_name
				alltree[count]['type']=per.type
				alltree[count]['describe']=per.describe
				alltree[count]['weight']=per.weight
				alltree[count]['calendar']=per.calendar
				alltree[count]['date']=per.date
				alltree[count]['data_type']=plan.data_type
				alltree[count]['actual']=0
				alltree[count]['red_flag']=0
				alltree[count]['goal']=0
				alltree[count]['score']=0
				alltree[count]['parent']=plan.name
				alltree[count]['indent']=1
				if per.score:
					per += obj.score
			else:
				continue

			obj_list = []
			for obj in scorecard:
				if obj.parent_scorecard == per.name:
					count += 1
					count_obj = count
					obj_list.append(count)
					alltree[count] = {}
					alltree[count].setdefault(count)
					alltree[count]['name']=obj.name
					alltree[count]['scorecard_name']=obj.scorecard_name
					alltree[count]['type']=obj.type
					alltree[count]['describe']=obj.describe
					alltree[count]['weight']=obj.weight
					alltree[count]['calendar']=obj.calendar
					alltree[count]['date']=obj.date
					alltree[count]['data_type']=plan.data_type
					alltree[count]['actual']=0
					alltree[count]['red_flag']=0
					alltree[count]['goal']=0
					alltree[count]['score']=0
					alltree[count]['parent']=per.name
					alltree[count]['indent']=2
					if obj.score:
						score += obj.score
				else:
					continue

				meas_list = []
				for meas in scorecard:
					if meas.parent_scorecard == obj.name:
						count += 1
						meas_list.append(count)
						alltree[count] = {}
						alltree[count].setdefault(count)
						alltree[count]['name']=meas.name
						alltree[count]['scorecard_name']=meas.scorecard_name
						alltree[count]['type']=meas.type
						alltree[count]['describe']=meas.describe
						alltree[count]['weight']=meas.weight
						alltree[count]['calendar']=meas.calendar
						alltree[count]['date']=meas.date
						alltree[count]['data_type']=plan.data_type
						alltree[count]['actual']=meas.actual if meas.actual else 0
						alltree[count]['red_flag']=meas.red_flag if meas.red_flag else 0
						alltree[count]['goal']=meas.goal if meas.goal else 0
						alltree[count]['score']=meas.score if meas.score else 0
						alltree[count]['parent']=obj.name
						alltree[count]['indent']=3
					else:
						continue

				#claculate obj
				score = 0
				for i in meas_list:
					alltree[count_obj]['goal'] += alltree[i]['goal']
					alltree[count_obj]['red_flag'] += alltree[i]['red_flag']
					alltree[count_obj]['actual'] += alltree[i]['actual']
					score += alltree[i]['score']
				list_len = len(meas_list)
				if len(meas_list) > 0:
					alltree[count_obj]['score']= flt(score / list_len)

			#claculate per
			score = 0
			list_len = len(meas_list)
			weight_sum = 0
			for i in obj_list:
				alltree[count_per]['goal'] += alltree[i]['goal']
				alltree[count_per]['red_flag'] += alltree[i]['red_flag']
				alltree[count_per]['actual'] += alltree[i]['actual']
				weight_sum += alltree[i]['weight']
			for i in obj_list:
				score += alltree[i]['score'] * frappe.utils.safe_div(alltree[i]['weight'], weight_sum)
			alltree[count_per]['score']= score

		#claculate plan
		score = 0
		list_len = len(meas_list)
		weight_sum = 0
		for i in per_list:
			alltree[count_plan]['goal'] += alltree[i]['goal']
			alltree[count_plan]['red_flag'] += alltree[i]['red_flag']
			alltree[count_plan]['actual'] += alltree[i]['actual']
			weight_sum += alltree[i]['weight']
		for i in per_list:
			score += alltree[i]['score'] * frappe.utils.safe_div(alltree[i]['weight'], weight_sum)
		alltree[count_plan]['score']= score

	data = []
	for t in sorted(alltree):

		tree = alltree.get(t)
		row = {
			"name": tree.get('name',''),
			"scorecard_name": tree.get('scorecard_name',''),
			"type": tree.get('type',''),
			"describe": tree.get('describe',''),
			"calendar": tree.get('calendar',''),
			"date": tree.get('date',''),
			"data_type": tree.get('data_type',''),
			"weight": tree.get('weight',''),
			"actual": tree.get('actual',''),
			"red_flag": tree.get('red_flag',''),
			"goal": tree.get('goal',''),
			"score": tree.get('score',''),
			"parent": tree.get('parent',''),
			"indent": tree.get('indent',''),
		}
		data.append(row)
	return data

def get_columns():
	return [
		{
			"fieldname": "subject",
			"label": _("Scorecard"),
			"fieldtype": "Link",
			"options": "Scorecard",
			"width": 100,
		},
		{
			"fieldname": "scorecard_name",
			"label": _("Scorecard Name"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "type",
			"label": _("Type"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "describe",
			"label": _("Describtion"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "calendar",
			"label": _("Calendar"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "date",
			"label": _("Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "weight",
			"label": _("Weight"),
			"fieldtype": "Float",
			"width": 100
		},
		{
			"fieldname": "data_type",
			"label": _("Data Type"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "actual",
			"label": _("Actual"),
			"fieldtype": "Float",
			"width": 100
		},
		{
			"fieldname": "red_flag",
			"label": _("Red Flag"),
			"fieldtype": "Float",
			"width": 100
		},
		{
			"fieldname": "goal",
			"label": _("Goal"),
			"fieldtype": "Float",
			"width": 100
		},
				{
			"fieldname": "score",
			"label": _("Score"),
			"fieldtype": "Float",
			"width": 100
		},
	]