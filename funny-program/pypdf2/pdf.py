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


def find_page(input_pdf="old.pdf", output_pdf="标示页.pdf", index=4):
    """
    抽取出pdf中的某一页
    :param input_pdf: 被抽取的pdf文件
    :param output_pdf: 抽取出来的页面输出的pdf文件名
    :param index: 所需要抽取的索引位置
    :return:
    """
    input_file = PdfFileReader(open(input_pdf, "rb"))
    output_file = PdfFileWriter()

    output_file.addPage(input_file.getPage(index))
    output_stream = open(output_pdf, "wb")
    output_file.write(output_stream)


def replace_pdf(pdf_file, insert_file, insert_index):
    """
    将pdf_file中某一页替换成insert_file中的单页
    :param pdf_file: 要替换的pdf文件地址
    :param insert_file: 要插入的file页面pdf文件地址
    :param insert_index: 要插入的索引位置，0开始
    :return:
    """
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
    replace_pdf(pdf_file="20210428_112705_xjS231_SXX1_K5_K6.pdf",
                insert_file="标示页.pdf",
                insert_index=3)
