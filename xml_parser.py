import xml.etree.cElementTree as eT
from enum import Enum, auto
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


class TagNames(Enum):
    ORGANISATION = auto()
    INN = auto()
    KPP = auto()
    ADDRESS = auto()
    MONEY = auto()
    PARTNER = auto()


class ReturnValues(Enum):
    FOUND = auto()
    NOT_FOUND = auto()
    ERROR = auto()
    XML_NOT_FOUND = auto()


class ExtractXML:

    def __init__(self, filename):
        self.filename = filename
        self.org_tags = set()
        self.money_tags = set()

    def get_value(self, tag_name):
        """
        extract info from xml-file
        :param tag_name: type of value (TagName)
        :return: ReturnValues
        """
        return_value = ReturnValues.XML_NOT_FOUND
        try:
            tree = eT.ElementTree(file=self.filename)
            root = tree.getroot()

            money11 = 'initialSum'
            money22 = 'sum'
            money33 = 'ContractPrice'
            address = 'postalAddress'
            short_name = 'shortName'
            full_name = 'fullName'
            partner = 'supplierInfo'

            for child in root:
                if 'body' in child.tag:
                    body = child.tag

                    for t in root.findall('./' + body + '//'):
                        if tag_name == TagNames.MONEY:
                            if money11 in t.tag or money22 in t.tag or money33 in t.tag:
                                try:
                                    if ',' in t.text:
                                        self.money_tags.add(int(t.text.split(',')[0]))
                                    if '.' in t.text:
                                        self.money_tags.add(int(t.text.split('.')[0]))
                                    else:
                                        self.money_tags.add(int(t.text))
                                except ValueError:
                                    continue
                                return_value = ReturnValues.FOUND
                        elif tag_name == TagNames.ORGANISATION:
                            if short_name in t.tag:
                                self.org_tags.add(t.text)
                                return_value = ReturnValues.FOUND
                            if full_name in t.tag:
                                self.org_tags.add(t.text)
                                return_value = ReturnValues.FOUND
                        elif tag_name == TagNames.PARTNER:
                            if partner in t.tag:
                                self.org_tags.add(t.text)
                                return_value = ReturnValues.FOUND
                        elif tag_name == TagNames.ADDRESS:
                            if address in t.tag:
                                return_value = ReturnValues.FOUND

        except IOError as e:
            logging.WARN('\nERROR - cant find file: %s\n' % e)
            return_value = ReturnValues.ERROR

        return return_value
