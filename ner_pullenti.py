"""
Pullenti recognition is here
"""
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection

from doc_info import CompanyInfo


def extract_money_org(text, processor, doc):
    result = processor.process(SourceOfAnalysis(text))

    # token = result.first_token
    # print(text)
    # while token:
    #     tokens = new_termin(token)
    #     token = token.next0_
    #     if tokens:
    #         # for t in tokens:
    #         print(tokens._m_end_token)
    #         print(tokens.kit.first_token)
    #         print(tokens.__dict__)

    for entity in result.entities:
        doc.money.add(entity.value) if entity.type_name == 'MONEY' else None
        if entity.type_name == 'ORGANIZATION':
            for name in entity.names:
                # company = CompanyInfo(str(name))
                doc.companies.add(str(name))
        # print(entity.value) if entity.type_name == 'MONEY' else ""
        # print(entity.names, entity.types, entity.eponyms) \
        #     if entity.type_name == 'ORGANIZATION' else ""


def new_termin(token):

    termin_collection = TerminCollection()

    client = Termin('ЗАКАЗЧИК')
    client.add_variant('ПОКУПАТЕЛЬ')
    client.add_variant("КЛИЕНТ")
    client.add_variant("ПОТРЕБИТЕЛЬ")
    termin_collection.add(client)

    doer = Termin("ИСПОЛНИТЕЛЬ")
    doer.add_variant("ПОДРЯДЧИК")
    doer.add_variant("ПОСТАВЩИК")
    doer.add_variant("ПРОДАВЕЦ")
    doer.add_variant("ЗАСТРОЙЩИК")
    termin_collection.add(doer)

    return termin_collection.try_parse(token)
