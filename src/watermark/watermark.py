from PyPDF2 import PdfWriter, PdfReader
from pdf2jpg import pdf2jpg
from fpdf import FPDF
import os
from PIL import Image
import shutil
import re
import uuid
import threading


def tryint(s):
    try:
        return int(s)
    except Exception:
        return s


def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [tryint(c) for c in re.split('([0-9]+)', s)]


def sort_nicely(list):
    """ Sort the given list in the way that humans expect.
    """
    list.sort(key=alphanum_key)


def watermark(original_pdf, output_pdf, watermark_pdf):
    """
    Take the original pdf and do the following:
        - merge it with watermark pdf into an intermediary pdf
        - export the intermediary pdf to jpeg
        - build another pdf file from jpegs -> watermark + readonly
    Refs:
        - https://stackabuse.com/working-with-pdfs-in-python-adding-images-and-watermarks
        - http://www.blog.pythonlibrary.org/2018/06/07/an-intro-to-pypdf2
    """

    print("starting worker: {0}".format(threading.get_ident()))

    tmp_pdf_name = 'intermediary_' + str(uuid.uuid1()) + '_.pdf'
    tmp_pdf_path = "{0}/{1}".format("/tmp", tmp_pdf_name)
    jpegs_dir = "{0}/{1}_{2}".format("/tmp", "jpegs", str(uuid.uuid1()))

    try:
        watermark = PdfReader(watermark_pdf)
        watermark_page = watermark.pages[0]
        pdf = PdfReader(original_pdf)
        pdf_writer = PdfWriter()

        for page in range(len(pdf.pages)):
            pdf_page = pdf.pages[page]
            pdf_page.merge_page(watermark_page)
            pdf_writer.add_page(pdf_page)

        with open(tmp_pdf_path, 'wb') as fh:
            pdf_writer.write(fh)

        pdf2jpg.convert_pdf2jpg(tmp_pdf_path, jpegs_dir, pages="ALL")

        images_list = [i for i in os.listdir("{0}/{1}_{2}".format(jpegs_dir, tmp_pdf_name, "dir")) if i.endswith(".jpg")]
        sort_nicely(images_list)
        makePdf(output_pdf, images_list, "{0}/{1}_{2}".format(jpegs_dir, tmp_pdf_name, "dir"))

        os.remove(tmp_pdf_path)
        shutil.rmtree(jpegs_dir)
    except Exception as e:
        print(f"Error watermarking file {original_pdf} with {watermark_pdf}. <{e}>")

def makePdf(pdfFileName, listPages, dir=''):
    if (dir):
        dir += "/"

    try:
        cover = Image.open(dir + str(listPages[0]))
        width, height = cover.size

        pdf = FPDF(unit="pt", format=[width, height])

        for page in listPages:
            pdf.add_page()
            pdf.image(dir + str(page), 0, 0)

        pdf.output(pdfFileName + ".pdf", "F")
    except Exception as e:
        print(f"Error creating pdf {pdfFileName}. <{e}>")
