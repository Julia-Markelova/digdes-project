"""
here is natasha named entity recognition
"""
from doc_info import *
from natasha import (
    NamesExtractor,
    PersonExtractor,
    AddressExtractor,
    OrganisationExtractor,
    MoneyExtractor,
)

ignore_arr = ['/home/yulia/Рабочий стол/digdes/Uploads/00b/aacda0c43805abdb599b7ce50cb33.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/16b76c3f92cbc79b77a66db99f03d.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/f0ea6af68e668dbfa4198a4363b89.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/9950ce5a38ee85b0e106db097b22d.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/2a9591c17e3aebaa98c5aacb1894f.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/65f211db67d202d6d9810b8b501c4.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/971e630fc295ed8361c99aab7b078.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/10c7f77e3f5752add9d1b6e3ad729.xml']


def extract_organizations(text: 'string', file: 'filename', doc: 'DocumentInfo')-> 'DocumentInfo':
    """
    extract info about organisations from a given text and save it to a given doc.
    Check if file is not in ignore list (there files which calls RecursionError)
    :param text: (string) plain text
    :param file: (string) full filename
    :param doc: DocumentInfo obj
    :return: DocumentInfo obj with a set of organisations
    """
    if file in ignore_arr:  # only for organisations -_-
        return

    extractor = OrganisationExtractor()
    matches = extractor(text)

    for match in matches:
        doc.companies.add(match.fact.name)

    return doc


def extract_money(text, doc):

    extractor = MoneyExtractor()
    matches = extractor(text)

    for match in matches:
        value = MoneyInfo(match.fact.integer, match.fact.currency)
        doc.money.add(value.value)

    return doc


def extract_address(text):
    # ADDRESS
    extractor = AddressExtractor()
    matches = extractor(text)
    spans = [_.span for _ in matches]   # !
    address = text[spans[0][0]:spans[0][1]]
    print(address)
