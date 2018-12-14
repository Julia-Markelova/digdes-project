"""
For total sum recognizing
"""
from yargy import Parser, rule, or_
from yargy.predicates import gram, normalized
from natasha.grammars import money
from natasha.extractors import Extractor

from extract_text import PlainText


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
            normalized('Итоговая сумма')
        ),
        or_(
            gram('NOUN').optional().repeatable(),
            gram('ADJF').optional().repeatable(),
            gram('VERB').optional().repeatable(),
            gram('PNCT').optional().repeatable()
        )
)


MY_MONEY = rule(
    SUMM,
    money.MONEY,
).interpretation(money.Money)


class MyMoneyExtractor(Extractor):
    def __init__(self):
        super(MyMoneyExtractor, self).__init__(MY_MONEY)


parser = Parser(MY_MONEY)


p = PlainText('/home/yulia/Рабочий стол/digdes/Uploads/000')
text = p.extract_doc_text('0cd32161147aea247b0124e69335c.xml').decode('utf-8')

# print(text)

extractor = MyMoneyExtractor()
matches = extractor(text)
# for match in matches:
#     print(match.span, match.fact)
#
# for match in parser.findall(text):
#     print([_.value for _ in match.tokens])


