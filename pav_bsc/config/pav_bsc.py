from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Scorecard"),
			"items": [
				{
					"type": "doctype",
					"name": "Scorecard",
					"description":_("Scorecard"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Scorecard Log",
					"description":_("Scorecard Log"),
					"onboard": 1,
				},
				{
					"type": "report",
					"name": "Scorecard Report",
					"doctype": "Scorecard",
					"is_query_report": True
				},
			]
		},
		
	]