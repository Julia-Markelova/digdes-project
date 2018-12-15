"""
here will be natasha named entity recognizing
"""
from extract_text import PlainText
from xml_parser import ExtractXML, TagNames
import os
from natasha import (
    NamesExtractor,
    PersonExtractor,
    AddressExtractor,
    OrganisationExtractor,
    MoneyExtractor,
    MoneyRateExtractor,
    MoneyRangeExtractor,
)

sub_dir = '/home/yulia/Рабочий стол/digdes/Uploads/003'

p = PlainText(sub_dir)


for file in p.xml_doc_map:
    # print("filename: " + file + "\n")
    xml = ExtractXML(os.path.join(sub_dir, file))
    xml.get_value(TagNames.ORGANISATION)
    xml.get_value(TagNames.MONEY)
    xml.get_value(TagNames.PARTNER)
    xml.get_value(TagNames.ADDRESS)
    #text = p.extract_doc_text(file).decode('utf-8')
    #print(text)
    # extractor = MoneyExtractor()
    # matches = extractor(text)
    # for match in matches:
    #     print(match.fact)
    # extractor = NamesExtractor()
    # matches = extractor(text)
    # for match in matches:
    #     print(match.fact)
    # extractor = OrganisationExtractor()
    # matches = extractor(text)
    # for match in matches:
    #     print(match.fact)
    #break



