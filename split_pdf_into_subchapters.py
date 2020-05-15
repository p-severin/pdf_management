import logging
from pathlib import Path

from PyPDF2 import PdfFileReader, PdfFileWriter, generic

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

parent_dir = Path('/home/patryk/Documents')
file_to_read = parent_dir / 'Materialy_do_egzaminu_2016-1.pdf'
# file_to_read = parent_dir / 'advanced_guide_to_python_programming.pdf'

dir_to_save_chapters = parent_dir / file_to_read.stem
dir_to_save_chapters.mkdir(exist_ok=True)

chapters = []


def flatten(A):
    rt = []
    for i in A:
        if isinstance(i, list):
            rt.extend(flatten(i))
        else:
            rt.append(i)
    return rt


file_stream = open(file_to_read, 'rb')
pdf_content = PdfFileReader(file_stream)
outlines = pdf_content.getOutlines()

for i, item in enumerate(outlines):
    if type(item) is generic.Destination and type(outlines[i + 1]) is list:
        title = item.title
        title = '_'.join(title.strip().replace('/', '_').split(' '))
        max_number_of_characters = 100
        if len(title) > max_number_of_characters:
            title = title[:max_number_of_characters]
        outlines[i + 1].insert(0, item)
        content = outlines[i + 1]
        chapters.append((
            title, content
        ))

for chapter in chapters:

    subchapters = flatten(chapter[1])
    file_to_write = dir_to_save_chapters / f'{chapter[0]}.pdf'

    pdf_writer = PdfFileWriter()
    start_page = pdf_content.getDestinationPageNumber(subchapters[0])
    end_page = pdf_content.getDestinationPageNumber(subchapters[-1])

    for i in range(start_page, end_page + 1):
        pdf_writer.addPage(pdf_content.getPage(i))
    with open(file_to_write, 'wb') as f:
        pdf_writer.write(f)

file_stream.close()
