from pullenti_wrapper.processor import (
    Processor,
    DATE,
    GEO,
    ORGANIZATION,
    PERSON,
    MONEY,
    ADDRESS
)


def wrapper_extractor(text, doc):
    processor = Processor([PERSON, ORGANIZATION, GEO, DATE, MONEY])
    result = processor(text)
    for match in result.walk():
        if match.referent.label == 'ORGANIZATION':
            # try:
            #     first = [value for key, value in match.referent.slots if key == 'TYPE'][0]
            #     last = [value for key, value in match.referent.slots if key == 'NAME'][0]
            #     doc.companies.add(str(first + ' ' + last))
            # except IndexError:
            #     pass
            for slot in match.referent.slots:
                if slot.key == 'NAME':
                    doc.companies.add(str(slot.value))
        if match.referent.label == 'MONEY':
            for slot in match.referent.slots:
                if slot.key == 'VALUE':
                    doc.money.add(int(slot.value))
