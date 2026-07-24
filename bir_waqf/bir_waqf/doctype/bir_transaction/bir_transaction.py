import frappe
from frappe.model.document import Document

class BirTransaction(Document):
	def validate(self):
		# Auto-clear critical exceptions if fields are corrected by user
		if self.has_exception:
			is_missing_id = self.transaction_id and self.transaction_id.startswith("MISSING-")
			has_valid_amount = self.total_amount and self.total_amount > 0
			
			basket_valid = True
			if self.is_basket and self.basket_projects:
				sub_sum = sum(p.sub_amount or 0.0 for p in self.basket_projects)
				if abs(sub_sum - self.total_amount) > 0.05:
					basket_valid = False

			if not is_missing_id and has_valid_amount and basket_valid:
				if not self.transfer_number:
					self.exception_reason = "رقم الحوالة/الصك مفقود (بانتظار المطابقة المصرفية)."
				else:
					self.has_exception = 0
					self.exception_reason = ""
