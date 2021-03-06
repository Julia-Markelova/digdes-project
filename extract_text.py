"""
Extract plain text from doc/docx
"""

import textract
import os
import re
import logging.config
import sys

from xml_parser import ReturnValues


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})


logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


class PlainText:

    def __init__(self, sub_dir):
        """
        xml_docs_map: map with xml and files doc/docx. There is full path of the file doc/docx.
        :param sub_dir: dir where all xml and doc/docx live.
        """
        # map: xml -> filename
        self.xml_docs_map = {}
        self.sub_dir = sub_dir
        self.init_maps()

    def init_maps(self):
        """
        Save to map names of xml file and its doc/docx file. Extension will be defined while saving.
        """
        files = os.listdir(self.sub_dir)
        for file in files:
            if re.search(".docx?$", file):
                xml_file = os.path.join(self.sub_dir, file.split(".")[0])
                xml_file += ".xml"
                self.xml_docs_map[xml_file] = os.path.join(self.sub_dir, file)

    def extract_doc_text(self, filename):
        """
        extract text from doc/docx files
        :param filename: file from which extract text
        :return: str
        """
        try:
            text = textract.process(self.xml_docs_map[filename])
            if not text:
                text = ReturnValues.ERROR
            return text
        except Exception as e:
            logging.warning("Failed to extract text from %s because %s", filename, e)
            return ReturnValues.ERROR
