# ! /usr/bin/python3.7
# Adding a watermark to a single-page PDF

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

input_file = "Course Introduction.pdf"
output_file = "example-drafted"
watermark_file = "watermark.pdf"
outputpath = "jpgs"


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

def watermark(input_pdf, output_pdf, watermark_pdf):

    watermark = PdfFileReader(watermark_pdf)
    watermark_page = watermark.getPage(0)
    intermediar_pdf = 'intermediar.pdf' 
 
    pdf = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()
 
    for page in range(pdf.getNumPages()):
        pdf_page = pdf.getPage(page)
        pdf_page.mergePage(watermark_page)
        pdf_writer.addPage(pdf_page)

 
    with open(intermediar_pdf, 'wb') as fh:
        pdf_writer.write(fh)
    
    pdf2jpg.convert_pdf2jpg(intermediar_pdf, outputpath, pages="ALL")

    images_list = [i for i in os.listdir('jpgs/' + intermediar_pdf + '_dir') if i.endswith(".jpg")]
    sort_nicely(images_list)
    makePdf(output_pdf, images_list, 'jpgs/' + intermediar_pdf + '_dir/')

    os.remove(intermediar_pdf)
    shutil.rmtree('jpgs')

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


if __name__ == '__main__':
    watermark(input_pdf=input_file, 
              output_pdf=output_file,
              watermark_pdf=watermark_file)
