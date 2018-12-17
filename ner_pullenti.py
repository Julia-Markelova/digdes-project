"""
Pullenti recognition is here
"""
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis


def extract_money(text, processor):
    result = processor.process(SourceOfAnalysis(text))

    for entity in result.entities:
        print(entity.value) if entity.type_name == 'MONEY' else ""
