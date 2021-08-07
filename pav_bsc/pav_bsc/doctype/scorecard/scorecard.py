# -*- coding: utf-8 -*-
# Copyright (c) 2021, Farouk Muharram and contributors
# For license information, please see license.txt

from __future__ import unicode_literals, division
import frappe
from frappe.model.document import Document
from frappe import _, throw
from frappe.utils import flt

class Scorecard(Document):
	def validate(self):
		self.validate_parent_type()

	def after_insert(self):
		self.update_weight(0)
			
	def on_trash(self):
		self.update_weight(1)

	def validate_parent_type(self):
		if self.type == 'Plan':
			return
		parent = frappe.get_doc('Scorecard', self.parent_scorecard)
		if self.type == 'Measure' and parent.type != 'Objective':
			frappe.throw(_("Parent type must be Objective"))
		if self.type == 'Objective' and parent.type != 'Perspective':
			frappe.throw(_("Parent type must be Perspective"))
		if self.type == 'Perspective' and parent.type != 'Plan':
			frappe.throw(_("Parent type must be Plan"))

		
	def update_weight(self, count):
		if self.type == 'Perspective' or self.type == 'Objective':
			docs = frappe.db.sql("""select name from `tabScorecard` WHERE type = %s and parent_scorecard = %s""", 
			(self.type ,self.parent_scorecard), as_dict=1)
			length = len(docs) - count
			if not docs or length == 0:
				return
			weight = 100 / length
			for doc in docs:
				if doc.name != self.name:
					frappe.db.set_value("Scorecard", doc["name"], "weight", weight)
			self.weight = weight
			self.save()
		