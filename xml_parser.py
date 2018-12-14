import xml.etree.cElementTree as eT
# tag_name shortName inn kpp postalAddress money
from enum import Enum


class TagNames(Enum):
    ORGANISATION = 'shortName'
    INN = 'inn'
    KPP = 'kpp'
    ADDRESS = 'postalAddress'
    MONEY = 'initialSum'


class ExtractXML:

    def __init__(self, filename):
        self.filename = filename

    def get_value(self, tag_name):
        try:
            tree = eT.ElementTree(file=self.filename)
            root = tree.getroot()

            body = '{http://zakupki.gov.ru/223fz/purchase/1}body'
            body2 = '{http://zakupki.gov.ru/223fz/purchasePlan/1}body'
            money11 = 'initialSum'
            money22 = 'sum'
            money33 = 'ContractPrice'
            address = '{http://zakupki.gov.ru/223fz/types/1}postalAddress'
            short_name = '{http://zakupki.gov.ru/223fz/types/1}shortName'

            i = False
            for t in root.findall('./' + body + '//'):
                # print(t.tag, t.text)
                if money11 in t.tag or money22 in t.tag or money33 in t.tag:
                    i = True

            if not i:
                for t in root.findall('./' + body2 + '//'):
                    # print(t.tag, t.text)
                    if money11 in t.tag or money22 in t.tag or money33 in t.tag:
                        i = True
            if not i:
                print("filename: " + self.filename)
                # print(root.findall('.//'))
                print("-----------------------------NO-----------------------------------")

        except IOError as e:
            print('\nERROR - cant find file: %s\n' % e)

