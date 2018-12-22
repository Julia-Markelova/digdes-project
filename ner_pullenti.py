"""
Pullenti recognition is here
"""
import logging.config
import sys

from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection

from doc_info import Company, CompanyContracts
from ner_stuff import Extractor
from string_stuff import cut_text
from xml_parser import ReturnValues

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
company_contracts = CompanyContracts()


class PullentiExtractor(Extractor):

    def __init__(self, processor, text, doc):
        super().__init__(text, doc)
        self.processor = processor

    def extract_compare_money_org(self):
        """
        extract money and organizations from text-file and compare it with xml-file
        :return: ReturnValues
        """
        try:
            result = self.processor.process(SourceOfAnalysis(self.text))
        except AttributeError or ValueError:
            logging.warning("Failed to extract entities from file %s", self.doc.doc_name)
            return ReturnValues.ERROR

        for entity in result.entities:
            self.doc.money.add(entity.value) if entity.type_name == 'MONEY' else None
            if entity.type_name == 'ORGANIZATION':
                for name in entity.names:
                    self.doc.companies.add(str(name))
        self.__compare_organizations_with_xml__(None)
        self.__compare_money_with_xml__()
        return ReturnValues.FOUND

    def extract_compare_main_info(self):
        """
        find in the text Client term and Executor term to extract near they
        organization-client and organization-executor with person's names
        """
        result = self.processor.process(SourceOfAnalysis(self.text))

        token = result.first_token
        begin = 0
        empty_client = True
        empty_executor = True

        company1 = Company(self.doc.doc_name)
        company2 = Company(self.doc.doc_name)

        while token:

            term = Client(token)
            client_token = term.find_client_token()
            term = Executor(token)
            executor_token = term.find_doer_token()

            if empty_client and client_token:
                begin, company1, company2 = \
                    self.__fill_company__(begin, client_token, company1, company2)
                empty_client = False

            if empty_executor and executor_token:
                begin, company2, company1 = \
                    self.__fill_company__(begin, executor_token, company2, company1)
                empty_executor = False

            if not empty_executor and not empty_client:
                # remove equals
                company1.companies -= company2.companies
                company2.companies -= company1.companies

                self.__fill_contracts_map__(company1, company2)

                logging.info("Found organization: \n%s", company1)
                logging.info("Found organization-partner:\n%s", company2)

                self.__compare_organizations_with_xml__(
                    company1.company_names | company2.company_names)

                break

            token = token.next0_

    def __fill_contracts_map__(self, company1, company2):

        comp1, comp2 = None, None

        if bool(company1.companies):
            comp1 = company1.companies.pop()
            company1.companies.add(comp1)
        if bool(company2.companies):
            comp2 = company2.companies.pop()
            company2.companies.add(comp2)

        if comp1 and comp2:
            company_contracts.add_contract(str(comp1), str(comp2))
            company_contracts.add_contract(str(comp2), str(comp1))
            company_contracts.save_to_json_file()

    def __fill_company__(self, begin, token, company1, company2):

        part = cut_text(self.text, begin, token.end_char)
        company1 = self.__extract_client_doer__(part, company1)
        if bool(company2.companies) and not company2.person:
            company2 = self.__extract_persons__(part, company2)
        elif bool(company1.companies) and not company1.person:
            company1 = self.__extract_persons__(part, company1)
            if not company1.person or company1.person == company2.person:
                part = cut_text(self.text, token.end_char,
                                token.end_char + 200)
                company1 = self.__extract_persons__(part, company1)
        begin = token.end_char

        return begin, company1, company2

    def __extract_client_doer__(self, part, company):
        result = self.processor.process(SourceOfAnalysis(part))

        # TODO: remove print
        print(part, "\n")
        for entity in result.entities:
            if entity.type_name == 'ORGANIZATION':
                company.companies.add(str(entity))
                for name in entity.names:
                    company.company_names.add(str(name))

        return company

    def __extract_persons__(self, part, company):
        result = self.processor.process(SourceOfAnalysis(part))
        for entity in result.entities:
            if entity.type_name == 'PERSON':
                company.person = str(entity)

        return company


class Client:
    """
    Need to add client's names into pullenti dict
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
        client.add_variant("ЗАЕМЩИК")
        client.add_variant("ПОЛЬЗОВАТЕЛЬ")

        term_collection.add(client)

        return term_collection.try_parse(self.token)


class Executor:
    """
       Need to add executor's names into pullenti dict
       """
    def __init__(self, token):
        self.token = token

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
        doer.add_variant("КРЕДИТОР")
        doer.add_variant("ОПЕРАТОР")
        doer.add_variant("CУБПОДРЯДЧИК")

        term_collection.add(doer)

        return term_collection.try_parse(self.token)
