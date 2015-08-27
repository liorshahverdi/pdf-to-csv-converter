import requests
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

# write pdf to a file
url = 'http://www.prb.org/pdf14/2014-world-population-data-sheet_eng.pdf'
res = requests.get(url)
res.raise_for_status()
new_pdf_filename = 'population_data_sheet.pdf'
new_pdf = open(new_pdf_filename, 'wb')
for chnk in res.iter_content(100000):
	new_pdf.write(chnk)
new_pdf.close()
print 'pdf has been downloaded.'

file_text = convert_pdf_to_txt('population_data_sheet.pdf')
ftl = file_text.split()

newfile = open('out.txt', 'wb')
for x in ftl:
	newfile.write(x)
	newfile.write('\n')
print 'Done.'