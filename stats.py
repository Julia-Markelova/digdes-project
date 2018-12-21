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

empty_org_counter = 0
empty_money_counter = 0
empty_org_xml = 0
empty_money_xml = 0
match_org_xml_counter = 0
match_money_xml_counter = 0
strict_include_counter = 0


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
                           abbreviation(normal_form(org_name))
                           .replace(" ", "").replace("-", ""), xml_set))
    no_space_doc = set(map(lambda org_name:
                           abbreviation(normal_form(org_name))
                           .replace(" ", "").replace("-", ""), document_set))
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


def avg_round_count(list_of_values):
    """
    count average value of a list
    :param list_of_values: list of digits
    :return: rounded average value
    """
    if list_of_values:
        return round(reduce(lambda x, y: x + y, list_of_values) / len(list_of_values), 2)


def avg_count(list_of_values):
    """
    count average
    :param list_of_values: list of digits
    :return: average value
    """
    if list_of_values:
        return reduce(lambda x, y: x + y, list_of_values) / len(list_of_values)


def f_value(precision, recall):
    """
    count f-value to show how good Named Entities were extracted
    :param precision: (right founded answers) / (all founded answers)
    :param recall: (right founded answers) / (right answers)
    :return: f-value (in percent)
    """
    return round(2 * precision * recall / (precision + recall) * 100, 2)


