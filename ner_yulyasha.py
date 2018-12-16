"""
For total sum recognizing
"""
from yargy import Parser, rule, or_
from yargy.predicates import gram, normalized, dictionary

from natasha.grammars import money
from natasha.extractors import Extractor
from natasha import MoneyExtractor
from xml_parser import *

import os

from extract_text import PlainText


RUBLES = rule(
    gram('ADJF').optional().repeatable(),
    gram('PNCT').optional().repeatable(),
    dictionary({
        'сумма',
        'стоимость',
        'итог',
        'итого',
        'всего'
    }),
    gram('VERB').optional().repeatable(),
    gram('PNCT').optional().repeatable()
)

SUMM = rule(
        or_(
            gram('NOUN').optional().repeatable(),
            gram('ADJF').optional().repeatable(),
            gram('VERB').optional().repeatable(),
        ),
        or_(
            normalized('итого'),
            normalized('всего'),
            normalized('общая стоимость'),
            normalized('стоимость'),
            normalized('сумма'),
            normalized('итоговая сумма'),
            normalized('Итого'),
            normalized('Всего'),
            normalized('Общая стоимость'),
            normalized('Стоимость'),
            normalized('Сумма'),
            normalized('Итоговая сумма'),
            normalized('стоимость работ'),
            normalized('руб'),
            normalized('рублей')
        ),
        or_(
            gram('NOUN').optional().repeatable(),
            gram('ADJF').optional().repeatable(),
            gram('VERB').optional().repeatable(),
            gram('PNCT').optional().repeatable()
        )
)


MY_MONEY = rule(
    or_(RUBLES,
        money.MONEY),
    or_(RUBLES,
        money.MONEY,
        RUBLES),
    or_(money.MONEY,
        RUBLES),
    or_(money.MONEY)
).interpretation(money.Money)


class MyMoneyExtractor(Extractor):
    def __init__(self):
        super(MyMoneyExtractor, self).__init__(MY_MONEY)


parser = Parser(MY_MONEY)

directory = '/home/yulia/Рабочий стол/digdes/Uploads/00b'
p = PlainText(directory)

for files in p.xml_docs_map:

    print(files)
    text = p.extract_doc_text(files).decode('utf-8')

    extractor = MyMoneyExtractor()
    matches = extractor(text)
    for match in matches:
        print("matcher: ", match.fact.integer, match.fact.currency)

    extractor = MoneyExtractor()
    matches = extractor(text)
    for match in matches:
        print("natasha: ", match.fact.integer, match.fact.currency)

    # XML stuff
    xml = ExtractXML(os.path.join(directory, files))
    xml.get_value(TagNames.MONEY)


