# -*- coding: utf-8 -*-
# Copyright (c) 2021, Farouk Muharram and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _, throw

class ScorecardLog(Document):
	def validate(self):
		self.validate_date()

	def validate_date(self):
		from datetime import datetime
		date = datetime.strptime(self.date, '%Y-%m-%d')
		log = frappe.db.sql("""select name, date from `tabScorecard Log`
		WHERE scorecard =  %s and MONTH(date) = %s  and YEAR(date) = %s""",(self.scorecard, date.month, date.year))
		if log:
				frappe.throw(_("There is log for the same scorecard and date!"))