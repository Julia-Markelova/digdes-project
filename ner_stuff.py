"""
module consists of base-class for all extractors with default functions
"""

import stats
from xml_parser import ExtractXML, TagNames, ReturnValues

import logging.config
import sys


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


class Extractor:

    def __init__(self, text, doc):
        self.text = text
        self.doc = doc

    def __compare_money_with_xml__(self):
        """
        compare extracted money with the right value from xml-file and count stats
        """
        is_not_empty = bool(self.doc.money)
        if is_not_empty:
            match = self.__check_match_xml_doc_money__()
            stats.match_money_xml_counter += 1 if match == ReturnValues.FOUND else 0
            stats.empty_money_xml += 1 if match == ReturnValues.XML_NOT_FOUND else 0
        else:
            stats.empty_money_counter += 1

    def __compare_organizations_with_xml__(self, organizations_set):
        if not organizations_set:
            organizations_set = self.doc.companies
        is_not_empty = bool(organizations_set)
        if is_not_empty:
            match = self.__check_xml_org_match_and_print__(organizations_set)
            stats.match_org_xml_counter += 1 if match == ReturnValues.FOUND else 0
            stats.empty_org_xml += 1 if match == ReturnValues.XML_NOT_FOUND else 0
        else:
            stats.empty_org_counter += 1

    def __check_xml_org_match_and_print__(self, organizations_set):
        xml = ExtractXML(self.doc.doc_name)
        organization = xml.get_value(TagNames.ORGANISATION)
        partner = xml.get_value(TagNames.PARTNER)

        if organization == ReturnValues.XML_NOT_FOUND and partner == ReturnValues.XML_NOT_FOUND:
            return ReturnValues.XML_NOT_FOUND
        if organization == ReturnValues.ERROR:
            return ReturnValues.XML_NOT_FOUND

        logging.info("Organizations from XML: %s", xml.org_tags)
        union = stats.strict_include(xml.org_tags, organizations_set)
        is_not_empty_ = bool(union)
        if is_not_empty_:
            logging.info("Found strict match: %s", union)
            stats.strict_include_counter += 1
        union = stats.include(xml.org_tags, organizations_set)
        is_not_empty_ = bool(union)
        if is_not_empty_:
            logging.info("All matches: %s", union)
            stats.precision_organization.append(len(union) / len(organizations_set))
            stats.recall_organization.append(len(union) / len(xml.org_tags))
            return ReturnValues.FOUND
        else:
            return ReturnValues.NOT_FOUND

    def __check_match_xml_doc_money__(self):
        xml = ExtractXML(self.doc.doc_name)
        money = xml.get_value(TagNames.MONEY)

        if money == ReturnValues.XML_NOT_FOUND or money == ReturnValues.ERROR:
            return money

        logging.info("Money from XML: %s", xml.money_tags)
        union = stats.include_money(xml.money_tags, self.doc.money)
        is_not_empty_ = bool(union)
        if is_not_empty_:
            logging.info("Found money matched with xml: %s", union)
            stats.precision_money.append(len(union) / len(self.doc.money))
            stats.recall_money.append(len(union) / len(xml.money_tags))
            return ReturnValues.FOUND
        else:
            return ReturnValues.NOT_FOUND
