"""
Pullenti recognition is here
"""
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection

from doc_info import Company
from ner_stuff import Extractor
from string_stuff import cut_text

companies = []


class PullentiExtractor(Extractor):

    def __init__(self, processor, text, doc):
        super().__init__(text, doc)
        self.processor = processor

    def extract_compare_money_org(self):
        result = self.processor.process(SourceOfAnalysis(self.text))

        for entity in result.entities:
            self.doc.money.add(entity.value) if entity.type_name == 'MONEY' else None
            if entity.type_name == 'ORGANIZATION':
                for name in entity.names:
                    self.doc.companies.add(str(name))
        self.__compare_organizations_with_xml__()
        self.__compare_money_with_xml__()

    def extract_main_info(self):
        result = self.processor.process(SourceOfAnalysis(self.text))

        token = result.first_token
        begin = 0
        empty_client = True
        empty_doer = True
        company1 = False
        company2 = False
        person1 = False
        person2 = False

        company_1 = Company()
        company_2 = Company()

        while token:
            term = ClientDoer(token)
            client_token = term.find_client_token()

            if client_token and empty_client:
                part = cut_text(self.text, begin, client_token.end_char)
                company1 = self.__extract_client_doer__(part, company_1)

                if company2 and not person2:
                    person2 = self.__extract_persons__(part, company_2)
                elif company1 and not person1:
                    person1 = self.__extract_persons__(part, company_1)
                    if not person1 or company_1.person == company_2.person:
                        part = cut_text(self.text, client_token.end_char,
                                        client_token.end_char + 200)
                        self.__extract_persons__(part, company_1)
                        person1 = True

                begin = client_token.end_char
                empty_client = False

            term = ClientDoer(token)
            doer_token = term.find_doer_token()

            if doer_token and empty_doer:
                part = cut_text(self.text, begin, doer_token.end_char)
                if begin == 0:
                    begin = doer_token.end_char

                company2 = self.__extract_client_doer__(part, company_2)

                if company1 and not person1:
                    person1 = self.__extract_persons__(part, company_1)
                elif company2 and not person2:
                    person2 = self.__extract_persons__(part, company_2)
                    if not person2 or company_1.person == company_2.person:
                        part = cut_text(self.text, doer_token.end_char,
                                        doer_token.end_char + 200)
                        self.__extract_persons__(part, company_2)
                        person2 = True

                empty_doer = False

            if not empty_doer and not empty_client:
                companies.append(company_1)
                companies.append(company_2)
                break
            token = token.next0_

    def __extract_client_doer__(self, part, company):
        result = self.processor.process(SourceOfAnalysis(part))
        print(part, "\n")
        find = False
        for entity in result.entities:
            if entity.type_name == 'ORGANIZATION':
                company.companies.add(str(entity))
                find = True
                print("ORGANIZATION: ", entity)

        return find

    def __extract_persons__(self, part, company):
        result = self.processor.process(SourceOfAnalysis(part))
        find = False
        for entity in result.entities:
            if entity.type_name == 'PERSON':
                company.person = str(entity)
                print("PERSON: ", entity)
                find = True

        return find


class ClientDoer:
    """
    Need to add client's and doer's names into pullenti dict
    """

    def __init__(self, token):
        self.token = token

    def find_client_token(self):
        """
        create a new term for the client and try to find it in the text
        :return: founded term (token) with info about it
        """
        term_collection = TerminCollection()

        client = Termin('ЗАКАЗЧИК')
        client.add_variant('ПОКУПАТЕЛЬ')
        client.add_variant("КЛИЕНТ")
        client.add_variant("ПОТРЕБИТЕЛЬ")
        client.add_variant("АРЕНДАТОР")
        client.add_variant("АБОНЕНТ")
        client.add_variant("АГЕНТ")

        # with quotes
        client.add_variant("«ЗАКАЗЧИК»")
        client.add_variant('«ПОКУПАТЕЛЬ»')
        client.add_variant("«КЛИЕНТ»")
        client.add_variant("«ПОТРЕБИТЕЛЬ»")
        client.add_variant("«АРЕНДАТОР»")
        client.add_variant("«АБОНЕНТ»")
        client.add_variant("«АГЕНТ»")
        term_collection.add(client)

        return term_collection.try_parse(self.token)

    def find_doer_token(self):
        """
        create a new term for the doer and try to find it in the text
        :return: founded term (token) with info about it
        """
        term_collection = TerminCollection()

        doer = Termin("ИСПОЛНИТЕЛЬ")
        doer.add_variant("ПОДРЯДЧИК")
        doer.add_variant("ПОСТАВЩИК")
        doer.add_variant("ПРОДАВЕЦ")
        doer.add_variant("ЗАСТРОЙЩИК")
        doer.add_variant("АРЕНДОДАТЕЛЬ")
        doer.add_variant("ГЕНПОДРЯДЧИК")
        doer.add_variant("ПРОВАЙДЕР")
        doer.add_variant("ПРИНЦИПАЛ")

        # with quotes
        doer = Termin("«ИСПОЛНИТЕЛЬ»")
        doer.add_variant("«ПОДРЯДЧИК»")
        doer.add_variant("«ПОСТАВЩИК»")
        doer.add_variant("«ПРОДАВЕЦ»")
        doer.add_variant("«ЗАСТРОЙЩИК»")
        doer.add_variant("«АРЕНДОДАТЕЛЬ»")
        doer.add_variant("«ГЕНПОДРЯДЧИК»")
        doer.add_variant("«ПРОВАЙДЕР»")
        doer.add_variant("«ПРИНЦИПАЛ»")
        term_collection.add(doer)

        return term_collection.try_parse(self.token)
