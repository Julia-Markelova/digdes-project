"""
file with main named entities
"""
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


class DocumentInfo:

    def __init__(self, doc_name):
        """
        :param doc_name: string: full file name
        """
        self.doc_name = doc_name
        self.companies = set()
        self.money = set()


class CompanyInfo:

    def __init__(self, company):
        """

        :param company: string name
        """
        self.company = abbreviation(normal_form(company))
        self.address = None
        self.person = None
        self.replace_quotes()

    def replace_quotes(self):
        if '»' in self.company or '«' in self.company:
            self.company = self.company.replace('»', '"')
            self.company = self.company.replace('«', '"')


def normal_form(string):
    """
    normalised all words in the given string
    :param string: string to normalise
    :return: normalised string
    """
    company_arr = string.split(" ")
    for c in range(len(company_arr)):
        company_arr[c] = company_arr[c].lower()
        company_arr[c] = morph.parse(company_arr[c])[0].normal_form
    return " ".join(company_arr)


def abbreviation(string):
    """
    convert definitions with their abbreviation
    :param string: string to replace in
    :return: converted string
    """
    word_abbr = {'общество с ограниченный ответственность': 'ооо',
                 'открытый акционерный общество': 'oaо',
                 'акционерный общество': 'ао',
                 'закрытый акционерный общество': 'зао'}
    for key in word_abbr.keys():
        if key in string:
            return string.replace(key, word_abbr[key])
    else:
        return string


class MoneyInfo:

    def __init__(self, value, currency):
        """

        :param value: int value
        :param currency: string curr
        """
        self.value = value
        self.currency = currency
