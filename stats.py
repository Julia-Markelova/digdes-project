"""
module to save different statistics
"""
from functools import reduce

from string_stuff import abbreviation, normal_form

times = []
precision_organization = []
recall_organization = []
precision_money = []
recall_money = []


def strict_include(xml_set, document_set):
    """
    check if organisations from extractor are in xml-file
    :param xml_set: set with organisations from xml-file
    :param document_set: set with organisations which are extracted by parser
    :return: intersection of two sets
    """
    no_space_xml = set(map(lambda org_name:
                           abbreviation(normal_form(org_name)).replace(" ", ""), xml_set))
    no_space_doc = set(map(lambda org_name:
                           abbreviation(normal_form(org_name)).replace(" ", ""), document_set))
    return no_space_xml & no_space_doc


def include(xml_set, document_set):
    """
    check if substrings of extractors organisations are in xml-file
    check if substrings of xml-file organisations are in extractor's string
    :param xml_set: set with organisations from xml-file
    :param document_set: set with organisations which are extracted by parser
    :return: set of founded elements
    """
    no_space_xml = set(map(lambda org_name:
                           abbreviation(normal_form(org_name)).replace(" ", ""), xml_set))
    no_space_doc = set(map(lambda org_name:
                           abbreviation(normal_form(org_name)).replace(" ", ""), document_set))
    included_words_set = set()

    ignore_abbr = ['ао', 'оао', 'ооо', 'зао', 'сп', 'дюсш',
                   'фгб', 'окб', 'аэс', 'кп', 'акб', 'уфмс',
                   'тгт', 'ук', 'спс', 'фгбу', 'с', 'маоу',
                   'маоудо', 'культура', 'мадоу']
    for doc in no_space_doc:
        if doc in ignore_abbr:
            continue
        for xml in no_space_xml:
            if doc in xml:
                included_words_set.add(doc)
            elif xml in doc:
                included_words_set.add(doc)
    return included_words_set


def include_money(xml_set, document_set):
    """
    check if values from extractor are equals to xml
    :param xml_set: set with money (int) from xml-file
    :param document_set: set with money (int) from extractor
    :return: intersection of two sets
    """
    return xml_set & document_set


def avg_count(list_of_values):
    return reduce(lambda x, y: x + y, list_of_values) / len(list_of_values)


def f_value(precision, recall):
    return round(2 * precision * recall / (precision + recall) * 100, 2)


