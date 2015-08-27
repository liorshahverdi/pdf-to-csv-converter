import requests, PyPDF2

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

# Open the pdf file and print the number of pages to stdout
pdf_obj = open(new_pdf_filename, 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_obj)
print 'Number of pages: %d' % (pdf_reader.numPages)
pages = []
for i in range(pdf_reader.numPages):
	nextPgObj = pdf_reader.getPage(i)
	pages.append(nextPgObj.extractText())
print pages