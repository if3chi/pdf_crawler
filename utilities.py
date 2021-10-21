import os
import pdfplumber as pdf
import convert
from errors import PdfIsScannedError


def prep_file(pdf_file=""):

    text = ""

    print("\nProcessing Document")

    try:

        with pdf.open(pdf_file) as f:

            for n in range(len(f.pages)):
                page = f.pages[n]
                text = page.extract_text(x_tolerance=4, y_tolerance=4)

            if text == None:
                raise PdfIsScannedError

    except FileNotFoundError as e:
        print(e)

    except PdfIsScannedError as err:
        print(f"\n**{err.message}**\nAttempting OCR")

        ocrpdf = convert.ocrpdf(pdf_file)

        with pdf.open(ocrpdf) as f:

            for n in range(len(f.pages)):
                page = f.pages[n]
                text = page.extract_text(x_tolerance=4, y_tolerance=4)

        os.remove(ocrpdf)

    return text


def bill_of_laiden(read_file):
    return read_file


def print_duration(start, end, message):

    tot_time = end - start

    print(
        f"\n** {message}",
        str(int((tot_time / 3600)))
        + ":"
        + str(int((tot_time % 3600) / 60))
        + ":"
        + str(int((tot_time % 3600) % 60)),
        "**\n",
    )
