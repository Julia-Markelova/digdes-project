import datetime
import os
import sys
import logging.config
import argparse

from pullenti.ner.ProcessorService import ProcessorService
from pullenti_wrapper.processor import Processor

import stats
from doc_info import Document
from extract_text import PlainText
from ner_natasha import NatashaExtractor
from ner_pullenti import PullentiExtractor
from ner_pullenti_wrapper import PullentiWrapperExtractor
from xml_parser import ReturnValues

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

extractor = 'natasha'


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


def extract_natasha(file_, text_, doc_):
    # NATASHA
    natasha = NatashaExtractor(text_, file_, doc_)
    try:
        natasha.extract_compare_money()
        natasha.extract_compare_organizations()
    except Exception as e:
        logging.warning("Natasha failed because %s", e)
        return ReturnValues.ERROR
    return ReturnValues.FOUND


def extract_pullenti(file_, text_, doc_, processor_):

    try:
        pullenti = PullentiExtractor(processor_, text_, doc_)
        ret_ = pullenti.extract_compare_money_org()
        if ret_ == ReturnValues.ERROR:
            logging.warning("Failed to extract from %s", file_)
            return ReturnValues.ERROR
    except Exception as e:
        logging.warning("Failed to extract from %s because %s", file_, e)
        return ReturnValues.ERROR
    return ReturnValues.FOUND


def extract_wrapper(text_, doc_, file_):
    try:
        pullenti_wrapper = PullentiWrapperExtractor(text_, doc_)
        pullenti_wrapper.wrapper_extract_compare_org_money()
    except Exception as e:
        logging.warning("Pullenti wrapper failed at %s because %s", file_, e)
        return ReturnValues.ERROR
    return ReturnValues.FOUND


def extract_organizations(processor_, text_, doc_, file_):
    pullenti = PullentiExtractor(processor_, text_, doc_)
    try:
        pullenti.extract_compare_main_info()
    except Exception as e:
        logging.warning("Can not extract info from %s because %s", file_, e)
        return ReturnValues.ERROR
    return ReturnValues.FOUND


parser = argparse.ArgumentParser(description='Extract organizations and money from texts')
group = parser.add_mutually_exclusive_group()
parser.add_argument('dir',
                    help='directory with directories which contain doc/docx files with xml-files')
group.add_argument('-e', '--extractor', nargs=1, help='name of extractor',
                   choices=['pullenti', 'pullenti-wrapper', 'natasha'])
group.add_argument('-oo', '--only_organizations', action='store_true',
                   help='extract only organizations)')

args = parser.parse_args()
if args.dir:
    directory = str(args.dir)
    print(directory)

if args.extractor:
    extractor = str(args.extractor[0])
    print(extractor)
elif args.only_organizations:
    extractor = 'oo'
    print(extractor)

file_counter = 0
dir_counter = 0
Processor([])
processor = ProcessorService.create_processor()

money = True

start = datetime.datetime.now()

for files in os.listdir(directory):

    start_time = datetime.datetime.now()
    sub_dir = os.path.join(directory, files)
    p = PlainText(sub_dir)
    ret = 0

    logging.info("%d Directory %s", dir_counter, sub_dir)
    dir_counter += 1

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

        doc = Document(file)

        if extractor == 'pullenti-wrapper':
            ret = extract_wrapper(text, doc, file)
        elif extractor == 'natasha':
            ret = extract_natasha(file, text, doc)
        elif extractor == 'pullenti':
            ret = extract_pullenti(file, text, doc, processor)
        elif extractor == 'oo':
            ret = extract_organizations(processor, text, doc, file)

        if ret == ReturnValues.ERROR:
            file_counter -= 1
            continue

        stats.times.append((datetime.datetime.now() - file_time))

    print_stats_organization()
    try:
        print_stats_money()
    except Exception:
        pass
