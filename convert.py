import os
import time
import uuid
import ocrmypdf

PATH = 'tmp'

def ocrpdf(pdf_file):

    print("Converting PDF: OCR")

    if not os.path.exists(PATH):
        os.makedirs(PATH, 0o777)

    save_path = f"{PATH}/{uuid.uuid5(uuid.NAMESPACE_DNS, str(time.time()))}.pdf"

    ocrmypdf.ocr(pdf_file, save_path, output_type="pdf", deskew=True, force_ocr=True, jbig2_lossy=True)

    return save_path
