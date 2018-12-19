import datetime
import os

from pullenti.ner.ProcessorService import ProcessorService
from pullenti_wrapper.processor import Processor

import stats
from doc_info import DocumentInfo
from extract_text import PlainText
from ner_natasha import extract_organizations, extract_money
from ner_pullenti import extract_money_org, extract_main_info
from ner_pullenti_wrapper import wrapper_extractor
from xml_parser import ExtractXML, TagNames

directory = '/home/yulia/Рабочий стол/digdes/Uploads'
docs = []
file_counter = 0
empty_org_counter = 0
empty_money_counter = 0
union_org_counter = 0
union_money_counter = 0

start = datetime.datetime.now()


def check_xml_match_and_print(doc_):
    xml = ExtractXML(doc_.doc_name)
    org = xml.get_value(TagNames.ORGANISATION)
    partner = xml.get_value(TagNames.PARTNER)

    if org or partner:
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
            stats.precision_organization.append(len(union) / len(doc_.companies))
            stats.recall_organization.append(len(union) / len(xml.org_tags))
        else:
            return False
        return True

    return False


def print_info_money(doc_):
    xml = ExtractXML(doc_.doc_name)
    money = xml.get_value(TagNames.MONEY)

    if money:
        print(xml.money_tags)

        for k in doc_.money:
            print("money: ", k)

        union = stats.include_money(xml.money_tags, doc_.money)
        is_not_empty_ = bool(union)
        if is_not_empty_:
            print("money", union)
            stats.precision_money.append(len(union) / len(doc_.money))
            stats.recall_money.append(len(union) / len(xml.money_tags))
        else:
            return False
        return True

    return False


for files in os.listdir(directory):

    start_time = datetime.datetime.now()
    sub_dir = os.path.join(directory, files)
    sub_dir = '/home/yulia/Рабочий стол/digdes/Uploads/00f'
    print("filename: " + sub_dir + "\n")

    p = PlainText(sub_dir)

    for file in p.xml_docs_map:

        print(file_counter, file)
        file_counter += 1

        file_time = datetime.datetime.now()

        text = p.extract_doc_text(file).decode('utf-8')

        # PULLENTI-WRAPPER
        # doc = DocumentInfo(file)
        # wrapper_extractor(text, doc)

        # PULLENTI
        # doc = DocumentInfo(file)
        # Processor([])
        # processor = ProcessorService.create_processor()
        # extract_money_org(text, processor, doc)
        # extract_main_info(text, processor, doc)
        # print(doc.company_client.company, doc.company_client.person,
        #       doc.company_doer.company, doc.company_doer.person)

        # NATASHA
        doc = DocumentInfo(file)
        doc = extract_organizations(text, file, doc)
        doc = extract_money(text, doc)

        is_not_empty = bool(doc.companies)
        if is_not_empty:
            match = check_xml_match_and_print(doc)
            union_org_counter += 1 if match else 0
        else:
            empty_org_counter += 1

        is_not_empty = bool(doc.money)
        if is_not_empty:
            match = print_info_money(doc)
            union_money_counter += 1 if match else 0
        else:
            empty_money_counter += 1

        docs.append(doc)

        stats.times.append((datetime.datetime.now() - file_time))

        # if file_counter > 9:
        #     break
    break

print("\n\n----------------------------------------------\n"
      "summ: {0}\nempty org: {1}, {8}%\n"
      "empty money: {2}, {9}%\n"
      "in xml money: {3}, {10}%\n"
      "in xml org: {4}, {11}%\n"
      "precision org: {5}%\n"
      "precision money: {12}%\n"
      "recall org: {13}%\n"
      "recall money: {14}%\n"
      "f-value org: {15}%\n"
      "f-value money: {16}%\n"
      "time: {6}\n"
      "avg time per file: {7}\n"
      .format(file_counter,
              empty_org_counter,
              empty_money_counter,
              union_money_counter,
              union_org_counter,
              round(stats.avg_count(stats.precision_organization) * 100, 2),
              datetime.datetime.now() - start,
              stats.avg_count(stats.times),
              empty_org_counter / file_counter * 100,
              empty_money_counter / file_counter * 100,
              union_money_counter / file_counter * 100,
              union_org_counter / file_counter * 100,
              round(stats.avg_count(stats.precision_money) * 100, 2),
              round(stats.avg_count(stats.recall_organization) * 100, 2),
              round(stats.avg_count(stats.recall_money) * 100, 2),
              stats.f_value(stats.avg_count(stats.precision_organization),
                            stats.avg_count(stats.recall_organization)),
              stats.f_value(stats.avg_count(stats.precision_money),
                            stats.avg_count(stats.recall_money))))
