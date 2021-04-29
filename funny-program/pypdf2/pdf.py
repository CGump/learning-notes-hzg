# -*- coding: utf-8 -*-
# ================================================================
#
#   Editor      : PyCharm
#   File name   : pdf.py
#   Author      : CGump
#   Email       : huangzhigang93@gmail.com
#   Created date: 2021/4/29 15:56
#
# ================================================================
from PyPDF2 import PdfFileReader, PdfFileWriter


def find_page(input_pdf="old.pdf",output_pdf="标示页.pdf", index=4):
    input_file = PdfFileReader(open(input_pdf, "rb"))
    output_file = PdfFileWriter()

    output_file.addPage(input_file.getPage(index))
    output_stream = open(output_pdf, "wb")
    output_file.write(output_stream)


def replace_pdf(pdf_file="new.pdf", insert_file="标示页.pdf", insert_index=3):
    pdf = PdfFileReader(open(pdf_file, "rb"))
    insert_page = PdfFileReader(open(insert_file, "rb"))

    output = PdfFileWriter()
    output_name = pdf_file.replace(".pdf", "_处理后.pdf")

    pages = pdf.getNumPages()
    for i in range(pages):
        if i == insert_index:
            output.addPage(insert_page.getPage(0))
            continue
        output.addPage(pdf.getPage(i))

    output_stream = open(output_name, "wb")
    output.write(output_stream)


if __name__ == '__main__':
    replace_pdf()
