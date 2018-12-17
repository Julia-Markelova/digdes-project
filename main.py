import datetime
import os

import stats
from extract_text import PlainText
from ner_natasha import extract_organizations, extract_money
from xml_parser import ExtractXML, TagNames

directory = '/home/yulia/Рабочий стол/digdes/Uploads'
docs = []
file_counter = 0
empty_org_counter = 0
empty_money_counter = 0
empty_union_org_counter = 0
empty_union_money_counter = 0

start = datetime.datetime.now()

for files in os.listdir(directory):
    sub_dir = os.path.join(directory, files)
    print("filename: " + sub_dir + "\n")

    p = PlainText(sub_dir)

    for file in p.xml_docs_map:

        text = p.extract_doc_text(file).decode('utf-8')
        doc = extract_organizations(text, file, None)
        doc = extract_money(text, file, doc)
        docs.append(doc)

        print(file_counter, file)
        file_counter += 1


for document in docs:
    print(document.doc_name)
    xml = ExtractXML(document.doc_name)
    # xml.get_value(TagNames.ORGANISATION)
    # xml.get_value(TagNames.PARTNER)
    xml.get_value(TagNames.MONEY)
    # union = stats.strict_include(xml.org_tags, document.companies)
    # is_not_empty = bool(union)
    # if is_not_empty:
    #     print("union:", union)
    #
    # union = stats.include(xml.org_tags, document.companies)
    # is_not_empty = bool(union)
    # if is_not_empty:
    #     print("union: inc!", union)
    # else:
    #     empty_union_org_counter += 1

    union = stats.include_money(xml.money_tags, document.money)
    is_not_empty = bool(union)
    if is_not_empty:
        print("money", union)
    else:
        empty_union_money_counter += 1

    # print(xml.org_tags)
    print(xml.money_tags)

    for k in document.companies:
        print("comp: ", k)
    for k in document.money:
        print("money: ", k)

print("summ: {0}, empty_org: {1}, "
      "empty_money: {2}, "
      "not in xml %: {3},\n time: {4}".format(file_counter,
                                              empty_org_counter,
                                              empty_money_counter,
                                              empty_union_money_counter,
                                              datetime.datetime.now() - start))