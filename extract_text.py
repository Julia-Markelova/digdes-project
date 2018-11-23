"""
Extract plain text from doc/docx
"""

import textract
import magic
import os
import re


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

    def extract_doc_text(self, filename):
        return textract.process(self.xml_doc_map[filename],
                                extension='doc')

    def extract_docx_text(self, filename):
        return textract.process(self.xml_doc_map[filename],
                                extension='docx')
