from pullenti_wrapper.processor import (
    Processor,
    DATE,
    GEO,
    ORGANIZATION,
    PERSON,
    MONEY,
)

processor = Processor([PERSON, ORGANIZATION, GEO, DATE, MONEY])
text = '...'
result = processor(text)
print(result)
