"""
Extract plain text from doc/docx
"""

import textract
import magic
import os
import re
import natasha


class PlainText:

    def __init__(self, sub_dir):
        """
        xml_doc_map: map with xml and files .doc. There is full path of the file .doc
        xml_docx_map: map with xml and files .docx. There is full path of the file .docx
        :param sub_dir: dir where all xml and doc/docx live.
        """
        # map: xml -> filename
        self.xml_doc_map = {}
        self.xml_docx_map = {}
        self.sub_dir = sub_dir
        self.init_maps()

    def init_maps(self):
        """
        Save to map xml file and its doc/docx file. Extension will be defined while saving.
        """

        files = os.listdir(self.sub_dir)
        for file in files:
            if re.search(".xml$", file):
                filename = os.path.join(self.sub_dir, file.split(".")[0])
                if re.match("Composite", magic.from_file(filename)):
                    self.xml_doc_map[file] = filename
                elif re.match("Microsoft", magic.from_file(filename)):
                    self.xml_docx_map[file] = filename

    # TODO: delete this shit
    def example(self):
        subdir = '/home/yulia/Рабочий стол/digdes/Uploads/000'
        file_doc = os.path.join(subdir, '0cd32161147aea247b0124e69335c')
        file_docx = os.path.join(subdir, '774af7d9b22a619a268b5438a75e9')

        print("doc", magic.from_file(file_doc), "\n")
        print("docx", magic.from_file(file_docx), "\n")

        doc_text = textract.process(self.xml_doc_map['0cd32161147aea247b0124e69335c.xml'],
                                    extension='doc')
        print(doc_text.decode('utf-8'))

    def named_entity(self):
        doc_text = textract.process(self.xml_doc_map['0cd32161147aea247b0124e69335c.xml'],
                                    extension='doc')
        extractor = natasha.MoneyExtractor()
        matches = extractor(doc_text.decode('utf-8'))
        for match in matches:
            print(match.span, match.fact)


p = PlainText('/home/yulia/Рабочий стол/digdes/Uploads/000')
p.named_entity()
