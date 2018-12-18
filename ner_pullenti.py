"""
Pullenti recognition is here
"""
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection

from doc_info import CompanyInfo


def extract_money_org(text, processor, doc):
    result = processor.process(SourceOfAnalysis(text))

    extract_main_info(text, processor)

    # for entity in result.entities:
    #     doc.money.add(entity.value) if entity.type_name == 'MONEY' else None
    #     if entity.type_name == 'ORGANIZATION':
    #         for name in entity.names:
    #             # company = CompanyInfo(str(name))
    #             doc.companies.add(str(name))
        # print(entity.value) if entity.type_name == 'MONEY' else ""
        # print(entity.names, entity.types, entity.eponyms) \
        #     if entity.type_name == 'ORGANIZATION' else ""


def extract_main_info(text, processor):
    result = processor.process(SourceOfAnalysis(text))

    token = result.first_token
    begin = 0
    empty_client = True
    empty_doer = True

    while token:
        tokens = new_client(token)

        if tokens and empty_client:
            part = cut_text(text, begin, tokens.end_char)
            print(part, "\n")
            extract_client_doer(part, processor)
            extract_persons(part, processor)
            begin = tokens.end_char
            empty_client = False

        tokens = new_doer(token)

        if tokens and empty_doer:
            part = cut_text(text, begin, tokens.end_char)
            if begin == 0:
                begin = tokens.end_char
            print(part, "\n")
            extract_client_doer(part, processor)
            extract_persons(part, processor)
            empty_doer = False

        if not empty_doer and not empty_client:
            break
        token = token.next0_


def extract_client_doer(text, processor):
    result = processor.process(SourceOfAnalysis(text))

    for entity in result.entities:
        if entity.type_name == 'ORGANIZATION':
            for name in entity.names:
                print("ORGANIZATION: ", name)


def extract_persons(text, processor):
    result = processor.process(SourceOfAnalysis(text))

    for entity in result.entities:
        if entity.type_name == 'PERSON':
            print("PERSON: ", entity)


def cut_text(text, begin, end):
    return text[begin:end]


def new_doer(token):
    termin_collection = TerminCollection()

    doer = Termin("ИСПОЛНИТЕЛЬ")
    doer.add_variant("ПОДРЯДЧИК")
    doer.add_variant("ПОСТАВЩИК")
    doer.add_variant("ПРОДАВЕЦ")
    doer.add_variant("ЗАСТРОЙЩИК")
    termin_collection.add(doer)

    return termin_collection.try_parse(token)


def new_client(token):

    termin_collection = TerminCollection()

    client = Termin('ЗАКАЗЧИК')
    client.add_variant('ПОКУПАТЕЛЬ')
    client.add_variant("КЛИЕНТ")
    client.add_variant("ПОТРЕБИТЕЛЬ")
    termin_collection.add(client)

    return termin_collection.try_parse(token)
