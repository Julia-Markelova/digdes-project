"""
here will be natasha named entity recognizing
"""
from extract_text import PlainText
from xml_parser import ExtractXML, TagNames
from doc_info import *
import datetime

import os
from natasha import (
    NamesExtractor,
    PersonExtractor,
    AddressExtractor,
    OrganisationExtractor,
    MoneyExtractor,
)


directory = '/home/yulia/Рабочий стол/digdes/Uploads'
ignore_arr = ['/home/yulia/Рабочий стол/digdes/Uploads/00b/aacda0c43805abdb599b7ce50cb33.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/16b76c3f92cbc79b77a66db99f03d.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/f0ea6af68e668dbfa4198a4363b89.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/9950ce5a38ee85b0e106db097b22d.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/2a9591c17e3aebaa98c5aacb1894f.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/65f211db67d202d6d9810b8b501c4.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/971e630fc295ed8361c99aab7b078.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/10c7f77e3f5752add9d1b6e3ad729.xml']
start = datetime.datetime.now()

file_counter = 0
empty_org_counter = 0
empty_money_counter = 0


docs = []

for files in os.listdir(directory):
    sub_dir = os.path.join(directory, files)
    # sub_dir = '/home/yulia/Рабочий стол/digdes/Uploads/00b'
    print("filename: " + sub_dir + "\n")

    p = PlainText(sub_dir)

    for file in p.xml_docs_map:

        # help to count empty matchers
        money = False
        organization = False

        print(file)
        print(file_counter)

        if file in ignore_arr:  # only for organisations -_-
            continue
        file_counter += 1
        text = p.extract_doc_text(file).decode('utf-8')  # docx format

        doc = DocumentInfo(file)

        # XML stuff
        # xml = ExtractXML(os.path.join(sub_dir, file))
        # xml.get_value(TagNames.ORGANISATION)
        # xml.get_value(TagNames.MONEY)
        # xml.get_value(TagNames.PARTNER)
        # xml.get_value(TagNames.ADDRESS)

        # MONEY
        extractor = MoneyExtractor()
        matches = extractor(text)

        for match in matches:
            value = MoneyInfo(match.fact.integer, match.fact.currency)
            doc.money.append(value)
            money = True
        if not money:
            empty_money_counter += 1

        # ORGANISATION
        extractor = OrganisationExtractor()
        matches = extractor(text)

        for match in matches:
            company = CompanyInfo(match.fact.name)
            doc.companies.add(company.company)
            organization = True
        if not organization:
            empty_org_counter += 1

        docs.append(doc)

        if file_counter > 4:
            break

    break

print("summ: {0}, empty_org: {1}, "
      "empty_money {2}, time {3}".format(file_counter, empty_org_counter,
                                         empty_money_counter,
                                         datetime.datetime.now() - start))

for i in docs:
    print(i.doc_name)
    for k in i.companies:
        print("comp: ", k)
    for k in i.money:
        print("money: ", k.value)
