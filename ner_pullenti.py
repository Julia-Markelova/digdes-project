"""
Pullenti recognition is here
"""
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis

from doc_info import CompanyInfo


def extract_money_org(text, processor, doc):
    result = processor.process(SourceOfAnalysis(text))

    for entity in result.entities:
        doc.money.add(entity.value) if entity.type_name == 'MONEY' else None
        if entity.type_name == 'ORGANIZATION':
            company = CompanyInfo(str(entity))
            doc.companies.add(company.company)
        # print(entity.value) if entity.type_name == 'MONEY' else ""
        print(entity) if entity.type_name == 'ORGANIZATION' else ""
