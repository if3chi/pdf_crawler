
class PdfIsScannedError(Exception):
	"""Raised when the input file (PDF) content is Scanned"""

	def __init__(self, message="The File is Scanned"):
		self.message = message
		super().__init__(self.message)
