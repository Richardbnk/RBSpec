"""
# Developer: Richard Raphael Banak
# Objective: Functions for simplify PDF scraping
# Creation date: 2021-12-16
"""

# -*- coding: utf-8 -*-

from .process import log
from PyPDF2 import PdfFileReader, PdfFileWriter

def read_pdf(file_path):
  global pdf_reader
  pdf_reader = PdfFileReader(file_path)
  return pdf_reader


def close_pdf_reader(file_path):
  global pdf_reader
  pdf_reader = None


def get_number_of_pages():
    return pdf_reader.getNumPages()
  
  
def get_page(page_number):
    return pdf_reader.getPage(page_number)
  
  
def get_page_text(page_number):
    return pdf_reader.getPage(page_number).extractText()
  
  
def clean_text_list(str_list):
    while "" in str_list:
        str_list.remove("")
    return str_list
  
  
def export_pdf_pages(page_list, file_path):
    pdf_writer = PdfFileWriter()

    for page_number in page_list:
        pdf_writer.addPage(pdf_reader.getPage(page_number))

    with open(file_path, "wb") as f:
        pdf_writer.write(f)
        f.close()

    pdf_writer = None
    
    log.info("File exported: {file_name}".format(file_name=file_path))
