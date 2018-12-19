import datetime
import os

from pullenti.ner.ProcessorService import ProcessorService
from pullenti_wrapper.processor import Processor

import stats
from doc_info import Document
from extract_text import PlainText
from ner_natasha import NatashaExtractor
from ner_pullenti import extract_money_org, extract_main_info
from ner_pullenti_wrapper import wrapper_extractor
from xml_parser import ExtractXML, TagNames, ReturnValues

directory = '/home/yulia/Рабочий стол/digdes/Uploads'
file_counter = 0


start = datetime.datetime.now()

for files in os.listdir(directory):

    start_time = datetime.datetime.now()
    sub_dir = os.path.join(directory, files)
    # sub_dir = '/home/yulia/Рабочий стол/digdes/Uploads/00f'
    print("filename: " + sub_dir + "\n")

    p = PlainText(sub_dir)

    for file in p.xml_docs_map:

        file_time = datetime.datetime.now()

        print(file_counter, file)
        file_counter += 1

        text = p.extract_doc_text(file).decode('utf-8')

        # PULLENTI-WRAPPER'shortName'
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
        doc = Document(file)
        natasha = NatashaExtractor(text, file, doc)
        natasha.extract_compare_money()
        natasha.extract_compare_organizations()
        stats.times.append((datetime.datetime.now() - file_time))

        if file_counter > 9:
            break
    break


# file_counter -= len(ignore_arr)  # for NATASHA!

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
                            stats.avg_round_count(stats.recall_money))))
