import datetime
import os

from pullenti.ner.ProcessorService import ProcessorService
from pullenti_wrapper.processor import Processor

import stats
from doc_info import DocumentInfo
from extract_text import PlainText
from ner_natasha import extract_organizations, extract_money
from ner_pullenti import extract_money_org
from ner_pullenti_wrapper import wrapper_extractor
from xml_parser import ExtractXML, TagNames

directory = '/home/yulia/Рабочий стол/digdes/Uploads'
docs = []
file_counter = 0
empty_org_counter = 0
empty_money_counter = 0
empty_union_org_counter = 0
empty_union_money_counter = 0

start = datetime.datetime.now()


def check_xml_match_and_print(doc_):
    xml = ExtractXML(doc_.doc_name)
    xml.get_value(TagNames.ORGANISATION)
    xml.get_value(TagNames.PARTNER)

    print(xml.org_tags)

    for company in doc_.companies:
        print("comp: ", company)

    union = stats.strict_include(xml.org_tags, doc_.companies)
    is_not_empty_ = bool(union)
    if is_not_empty_:
        print("union:", union)

    union = stats.include(xml.org_tags, doc_.companies)
    is_not_empty_ = bool(union)
    if is_not_empty_:
        print("union: inc!", union)
    else:
        return False
    return True


def print_info_money(doc_):
    xml = ExtractXML(doc_.doc_name)
    xml.get_value(TagNames.MONEY)

    print(xml.money_tags)

    for k in doc_.money:
        print("money: ", k)

    union = stats.include_money(xml.money_tags, doc_.money)
    is_not_empty_ = bool(union)
    if is_not_empty_:
        print("money", union)
    else:
        return False
    return True


for files in os.listdir(directory):

    start_time = datetime.datetime.now()
    sub_dir = os.path.join(directory, files)
    print("filename: " + sub_dir + "\n")

    p = PlainText(sub_dir)

    for file in p.xml_docs_map:

        text = p.extract_doc_text(file).decode('utf-8')

        # PULLENTI-WRAPPER
        # doc = DocumentInfo(file)
        # wrapper_extractor(text, doc)
        #
        # is_not_empty = bool(doc.companies)
        # if is_not_empty:
        #     match = check_xml_match_and_print(doc)
        #     if not match:
        #         empty_union_org_counter += 1
        # else:
        #     empty_org_counter += 1
        #
        # is_not_empty = bool(doc.money)
        # if is_not_empty:
        #     match = print_info_money(doc)
        #     if not match:
        #         empty_union_money_counter += 1
        # else:
        #     empty_money_counter += 1

        # PULLENTI
        doc = DocumentInfo(file)
        Processor([])
        processor = ProcessorService.create_processor()
        extract_money_org(text, processor, doc)

        # NATASHA
        # doc = DocumentInfo(file)
        # doc = extract_organizations(text, file, doc)
        # doc = extract_money(text, doc)

        docs.append(doc)

        print(file_counter, file)
        file_counter += 1

        if file_counter > 9:
            break
    break

print("summ: {0}, empty_org: {1}, "
      "empty_money: {2}, "
      "not in xml money: {3},\nnot in xml org {4}, "
      "time: {5}".format(file_counter,
                         empty_org_counter,
                         empty_money_counter,
                         empty_union_money_counter,
                         empty_union_org_counter,
                         datetime.datetime.now() - start))
