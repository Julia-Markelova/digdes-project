import datetime
import os

from pullenti.ner.ProcessorService import ProcessorService
from pullenti_wrapper.processor import Processor

import stats
from doc_info import Document
from extract_text import PlainText
from ner_natasha import NatashaExtractor, ignore_arr
from ner_pullenti import PullentiExtractor, companies
from ner_pullenti_wrapper import wrapper_extractor
from xml_parser import ReturnValues


def print_stats():
    print("\n\n----------------------------------------------\n"
          "summ: {0}\nempty org: {1}, {8}%\n"
          "empty money: {2}, {9}%\n"
          "empty xml org: {19}\n"
          "empty xml money: {20}\n"
          "in xml money: {3}, {10}%\n"
          "in xml org: {4}, {11}%\n"
          "in xml org strict {17}, {18}%\n"
          "precision org: {5}%\n"
          "precision money: {12}%\n"
          "recall org: {13}%\n"
          "recall money: {14}%\n"
          "f-value org: {15}%\n"
          "f-value money: {16}%\n"
          "time: {6}\n"
          "avg time per file: {7}\n"
          .format(file_counter,
                  stats.empty_org_counter,
                  stats.empty_money_counter,
                  stats.match_money_xml_counter,
                  stats.match_org_xml_counter,
                  stats.avg_round_count(stats.precision_organization) * 100,
                  datetime.datetime.now() - start,
                  stats.avg_count(stats.times),
                  stats.empty_org_counter / file_counter * 100,
                  stats.empty_money_counter / file_counter * 100,
                  stats.match_money_xml_counter / file_counter * 100,
                  stats.match_org_xml_counter / file_counter * 100,
                  stats.avg_round_count(stats.precision_money) * 100,
                  stats.avg_round_count(stats.recall_organization) * 100,
                  stats.avg_round_count(stats.recall_money) * 100,
                  stats.f_value(stats.avg_round_count(stats.precision_organization),
                                stats.avg_round_count(stats.recall_organization)),
                  stats.f_value(stats.avg_round_count(stats.precision_money),
                                stats.avg_round_count(stats.recall_money)),
                  stats.strict_include_counter,
                  round(stats.strict_include_counter / file_counter * 100, 2),
                  stats.empty_org_xml,
                  stats.empty_money_xml))


directory = '/home/yulia/Рабочий стол/digdes/Uploads'
file_counter = 0
doc_counter = 0

start = datetime.datetime.now()

for files in os.listdir(directory):

    start_time = datetime.datetime.now()
    sub_dir = os.path.join(directory, files)
    # sub_dir = '/home/yulia/Рабочий стол/digdes/Uploads/00f'

    print("filename: " + sub_dir + "\n")
    doc_counter += 1
    p = PlainText(sub_dir)

    if doc_counter < 4:
        continue

    for file in p.xml_docs_map:

        file_time = datetime.datetime.now()

        print(file_counter, file)
        file_counter += 1

        text = p.extract_doc_text(file).decode('utf-8')
        if text == ReturnValues.ERROR:
            print("text parse error---------------------------------")
            file_counter -= 1
            continue

        # PULLENTI-WRAPPER
        # doc = Document(file)
        # wrapper_extractor(text, doc)

        # PULLENTI
        doc = Document(file)
        Processor([])
        processor = ProcessorService.create_processor()
        pullenti = PullentiExtractor(processor, text, doc)
        ret = pullenti.extract_compare_money_org()
        if ret == ReturnValues.ERROR:
            file_counter -= 1
            print("Attribute error----------------------------------------\n")

        # pullenti.extract_main_info()
        # for company in companies:
        #     print(company)
        # print(doc.company_client.company, doc.company_client.person,
        #       doc.company_doer.company, doc.company_doer.person)

        # NATASHA
        # doc = Document(file)
        # natasha = NatashaExtractor(text, file, doc)
        # try:
        #     natasha.extract_compare_money()
        #     natasha.extract_compare_organizations()
        # except Exception:
        #     print("Natasha failed again\n")
        #     file_counter -= 1
        #     continue

        stats.times.append((datetime.datetime.now() - file_time))

    print(doc_counter)

    if doc_counter > 8:
        break

    print_stats()

# file_counter -= len(ignore_arr)  # for NATASHA!

print_stats()
