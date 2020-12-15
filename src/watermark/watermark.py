# Adding a watermark to a single pdf file
# Refs:
# https://stackabuse.com/working-with-pdfs-in-python-adding-images-and-watermarks/
# http://www.blog.pythonlibrary.org/2018/06/07/an-intro-to-pypdf2/



from PyPDF2 import PdfFileWriter, PdfFileReader
from pdf2jpg import pdf2jpg 
from fpdf import FPDF
import os
from fpdf import FPDF
from PIL import Image
import shutil
import re
import uuid
import time
import threading

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)

def watermark(original_pdf, output_pdf, watermark_pdf):

    print("starting worker: {0}".format(threading.get_ident()))

    # intermediary pdf is the pdf doc which will contain
    # the merging between the original one and watermark
    tmp_pdf_name = 'intermediary_' + str(uuid.uuid1()) + '_.pdf'
    tmp_pdf_path = "{0}/{1}".format("/tmp", tmp_pdf_name)

    # jpegs output path - represents the jpegs files 
    # for each page from the intermediary pdf
    jpegs_dir = "{0}/{1}_{2}".format("/tmp", "jpegs", str(uuid.uuid1()))

    # watermark pdf is the pdf which will be merged in all pages
    watermark = PdfFileReader(watermark_pdf)
    watermark_page = watermark.getPage(0)

    # build intermediary pdf
    pdf = PdfFileReader(original_pdf)
    pdf_writer = PdfFileWriter()
 
    for page in range(pdf.getNumPages()):
        pdf_page = pdf.getPage(page)
        pdf_page.mergePage(watermark_page)
        pdf_writer.addPage(pdf_page)

    with open(tmp_pdf_path, 'wb') as fh:
        pdf_writer.write(fh)

    # convert each intermediary pdf page to jpeg
    pdf2jpg.convert_pdf2jpg(tmp_pdf_path, jpegs_dir, pages="ALL")

    # build output pdf from these images
    images_list = [i for i in os.listdir("{0}/{1}_{2}".format(jpegs_dir, tmp_pdf_name, "dir")) if i.endswith(".jpg")]
    sort_nicely(images_list)
    makePdf(output_pdf, images_list, "{0}/{1}_{2}".format(jpegs_dir, tmp_pdf_name, "dir"))

    os.remove(tmp_pdf_path)
    shutil.rmtree(jpegs_dir)

def makePdf(pdfFileName, listPages, dir=''):
    if (dir):
        dir += "/"

    cover = Image.open(dir + str(listPages[0]))
    width, height = cover.size

    pdf = FPDF(unit="pt", format=[width, height])

    for page in listPages:
        pdf.add_page()
        pdf.image(dir + str(page), 0, 0)

    pdf.output(pdfFileName + ".pdf", "F")
