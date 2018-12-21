import datetime
import os
import sys
import logging.config

from pullenti.ner.ProcessorService import ProcessorService
from pullenti_wrapper.processor import Processor

import stats
from doc_info import Document
from extract_text import PlainText
from ner_natasha import NatashaExtractor, ignore_arr
from ner_pullenti import PullentiExtractor
from ner_pullenti_wrapper import wrapper_extractor
from xml_parser import ReturnValues


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})


logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def print_stats_money():
    print("\n\n---------------------MONEY-------------------------\n"
          "summ: {0}\n"
          "empty money: {1}, {2}%\n"
          "empty xml money: {3}\n"
          "in xml money: {4}, {5}%\n"
          "precision money: {6}%\n"
          "recall money: {7}%\n"
          "f-value money: {8}%\n"
          "time: {9}\n"
          "avg time per file: {10}\n"
          .format(file_counter,
                  stats.empty_money_counter,
                  stats.empty_money_counter / file_counter * 100,
                  stats.empty_money_xml,
                  stats.match_money_xml_counter,
                  stats.match_money_xml_counter / file_counter * 100,
                  stats.avg_round_count(stats.precision_money) * 100,
                  stats.avg_round_count(stats.recall_money) * 100,
                  stats.f_value(stats.avg_round_count(stats.precision_money),
                                stats.avg_round_count(stats.recall_money)),
                  datetime.datetime.now() - start,
                  stats.avg_count(stats.times),
                  ))


def print_stats_organization():
    print("\n\n----------------------ORGANIZATION------------------------\n"
          "summ: {0}\nempty org: {1}, {2}%\n"
          "empty xml org: {3}\n"
          "in xml org: {4}, {5}%\n"
          "in xml org strict {6}, {7}%\n"
          "precision org: {8}%\n"
          "recall org: {9}%\n"
          "f-value org: {10}%\n"
          "time: {11}\n"
          "avg time per file: {12}\n"
          .format(file_counter,
                  stats.empty_org_counter,
                  stats.empty_org_counter / file_counter * 100,
                  stats.empty_org_xml,
                  stats.match_org_xml_counter,
                  stats.match_org_xml_counter / file_counter * 100,
                  stats.strict_include_counter,
                  round(stats.strict_include_counter / file_counter * 100, 2),
                  stats.avg_round_count(stats.precision_organization) * 100,
                  stats.avg_round_count(stats.recall_organization) * 100,
                  stats.f_value(stats.avg_round_count(stats.precision_organization),
                                stats.avg_round_count(stats.recall_organization)),
                  datetime.datetime.now() - start,
                  stats.avg_count(stats.times),
                  ))


if len(sys.argv) > 1:
    directory = sys.argv[1]
else:
    logging.critical("No directory passed")
    exit(1)

file_counter = 0
dir_counter = 0

money = True

start = datetime.datetime.now()

for files in os.listdir(directory):

    start_time = datetime.datetime.now()
    sub_dir = os.path.join(directory, files)
    p = PlainText(sub_dir)

    logging.info("%d Directory %s\n", dir_counter, sub_dir)
    dir_counter += 1

    if dir_counter < 5:
        continue

    for file in p.xml_docs_map:

        file_time = datetime.datetime.now()

        logging.info("%d File %s", file_counter, file)
        file_counter += 1

        text = p.extract_doc_text(file)
        if text == ReturnValues.ERROR:
            logging.warning("Failed to parse text from file %s", file)
            file_counter -= 1
            continue
        else:
            text = text.decode('utf-8')

        # PULLENTI-WRAPPER
        # doc = Document(file)
        # wrapper_extractor(text, doc)

        # PULLENTI
        doc = Document(file)
        Processor([])
        processor = ProcessorService.create_processor()
        try:
            pullenti = PullentiExtractor(processor, text, doc)
            ret = pullenti.extract_compare_money_org()
            if ret == ReturnValues.ERROR:
                file_counter -= 1
                logging.warning("Failed to extract from %s", file)
        except Exception as e:
            logging.warning("Failed to extract from %s because %s", file, e)

        # pullenti.extract_main_info()
        # money = False

        # NATASHA
        # doc = Document(file)
        # natasha = NatashaExtractor(text, file, doc)
        # try:
        #     natasha.extract_compare_money()
        #     natasha.extract_compare_organizations()
        # except Exception:
        #     logging.warning("Natasha failed again\n")
        #     file_counter -= 1
        #     continue

        stats.times.append((datetime.datetime.now() - file_time))

    if dir_counter > 8:
        break

    print_stats_organization()
    print_stats_money() if money else "No info about money"

# file_counter -= len(ignore_arr)  # for NATASHA!
