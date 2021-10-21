import pdfplumber
import pandas as pd
from utilities import bill_of_laiden, print_duration as run_time, prep_file
import time
from invoice import Invoice
import json

B_O_LAIDEN = 1
INVOICE = 2


def process_text(file_type, text):

    print("Reading Document Info")

    result = []

    if file_type == B_O_LAIDEN:

        print("\n**Bill of Laiden**")

        result = bill_of_laiden(text)

    if file_type == INVOICE:
        print("\n**Invoice**")

        result = Invoice(text).get_result()

    return result


def get_pdf(key, name):

    switch = {B_O_LAIDEN: "BL", INVOICE: "Invoices"}

    return key, f"testFiles/{switch.get(key)}/{name}.pdf"


def main():

    print("Starting Document Process..")

    start_time = time.time()

    # key, file_path = get_pdf(B_O_LAIDEN, 2)

    key, file_path = get_pdf(INVOICE, 2)

    text = prep_file(file_path)

    result = process_text(key, text)

    print(json.dumps(json.loads(result), indent=2, sort_keys=False))

    end_time = time.time()

    run_time(start_time, end_time, "Process Finished")


if __name__ == "__main__":
    main()
