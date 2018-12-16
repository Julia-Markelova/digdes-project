import xml.etree.cElementTree as eT
from enum import Enum
from doc_info import abbreviation, normal_form


class TagNames(Enum):
    ORGANISATION = 'shortName'
    INN = 'inn'
    KPP = 'kpp'
    ADDRESS = 'postalAddress'
    MONEY = 'initialSum'
    PARTNER = 'supplierInfo'


class ExtractXML:

    def __init__(self, filename):
        self.filename = filename
        self.tags = set()

    def get_value(self, tag_name):
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

            i = False
            for child in root:
                if 'body' in child.tag:
                    body = child.tag

                    for t in root.findall('./' + body + '//'):
                        # print(t.tag, t.text)
                        if tag_name == TagNames.MONEY:
                            if money11 in t.tag or money22 in t.tag or money33 in t.tag:
                                print("xml: ", t.text)
                                i = True
                        elif tag_name == TagNames.ORGANISATION:
                            if short_name in t.tag:
                                self.tags.add(abbreviation(normal_form(t.text)))
                                i = True
                            if full_name in t.tag:
                                self.tags.add(abbreviation(normal_form(t.text)))
                                i = True
                        elif tag_name == TagNames.ADDRESS:
                            if address in t.tag:
                                i = True
                        elif tag_name == TagNames.PARTNER:
                            if partner in t.tag:
                                print("partner: ", t.text)
                                i = True

                    if not i:
                        pass
                        # print("filename: " + self.filename)
                        # print(root.findall('.//'))
                        # print("-----------------------------NO-------"+tag_name.value+"----------------------")

        except IOError as e:
            print('\nERROR - cant find file: %s\n' % e)
