from pullenti_wrapper.processor import Processor, ORGANIZATION, MONEY

from ner_stuff import Extractor


class PullentiWrapperExtractor(Extractor):

    def wrapper_extract_compare_org_money(self):
        """
        extract money and organizations from the text and compare them with the xml-file
        """
        processor = Processor([ORGANIZATION, MONEY])
        result = processor(self.text)
        for match in result.walk():
            if match.referent.label == 'ORGANIZATION':
                for slot in match.referent.slots:
                    if slot.key == 'NAME':
                        self.doc.companies.add(str(slot.value))
            if match.referent.label == 'MONEY':
                for slot in match.referent.slots:
                    if slot.key == 'VALUE':
                        self.doc.money.add(int(slot.value))
        self.__compare_organizations_with_xml__(None)
        self.__compare_money_with_xml__()
