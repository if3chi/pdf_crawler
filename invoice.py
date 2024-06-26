import re
import json


class Invoice:
    def __init__(self, text):
        self.text = text

    def __sanitize_data(self, data):

        goods_desc = []
        goods_qty = []
        unit_price = []
        total_price = []

        for line in data:
            line = list(filter(None, " ".join(line.split(", ")).split(" ")))

            total_price.append(line.pop(len(line) - 1).replace("O", "0"))

            u_price = (
                line.pop(len(line) - 1)
                .lower()
                .strip("/ctnCTN")
                .replace("so", "50")
                .replace("s", "5")
                .replace("O", "0")
            )

            if re.compile(r"\d,\d").match(u_price):
                total_price[-1] = u_price + total_price[-1]
                unit_price.append(line.pop(len(line) - 1).strip("/CTN"))
            else:
                unit_price.append(u_price.strip("/CTN"))

            qty = line.pop(len(line) - 1)

            if qty == "CTNS":
                goods_qty.append(line.pop(len(line) - 1).lower().strip("ctns"))
            else:
                goods_qty.append(
                    qty.lower().strip("ctns").replace("l", "1").replace("o", "0")
                )

            goods_desc.append(" ".join(line))

        return {
            "Description": goods_desc,
            "Quantity": goods_qty,
            "Unit Price": unit_price,
            "Total Amount": total_price,
        }

    def __get_consignee(self):
        pass

    def __get_invoice(self):

        desc_list = []
        table = re.compile(r"^\d.* ([a-zA-Z].* [\d,]+\.\d{2})")
        price = re.compile(r"^\d([0-9,]*\.[0-9]*)")

        for line in self.text.split("\n"):

            if price.match(line):
                desc_list[-1] += f" {line}"
                continue

            if table.match(line):
                desc_list.append(
                    " ".join(line.split(" ")[1:]).replace("|", "").replace("_", "")
                )

        return self.__sanitize_data(desc_list)

    def __get_invoice_number(self):

        invoice_num = "null"

        for line in self.text.splitlines():
            if re.compile(r"^INVOICE |INVOIGE ").findall(line):

                try:
                    invoice_num = list(filter(None, line.split(" ")))[1]
                    return invoice_num
                except Exception as e:
                    invoice_num = "null"

        return invoice_num

    def __get_invoice_date(self):

        return re.findall(r"\d{2}-\d{2}-\d{4}|\d{2}/\d{2}/\d{4}", self.text)[0]

    def __get_fob(self):

        fob = "null"

        for line in self.text.splitlines():
            if re.compile(r"^FOB|^[a-zA-Z].* FOB ").findall(line):

                try:
                    fob = list(filter(None, line.split(" ")))[-1]
                    return fob.strip('$')
                except Exception as e:
                    fob = "null"

        return fob
    
    def __get_freight(self):

        freight = "null"

        for line in self.text.splitlines():
            if re.compile(r"^FREIGHT|^[a-zA-Z].* FREIGHT ").findall(line):

                try:
                    freight = list(filter(None, line.split(" ")))[-1]
                    return freight.strip('$')
                except Exception as e:
                    freight = "null"

        return freight

    def __prep_data(self):
        return {
            "invoice date": self.__get_invoice_date(),
            "invoice number": self.__get_invoice_number(),
            "consignee": self.__get_consignee(),
            "Invoice Table": self.__get_invoice(),
            "FOB": self.__get_fob(),
            "Freight Charges": self.__get_freight(),
        }

    def get_result(self):
        return json.dumps(["Invoice Details", self.__prep_data()])
