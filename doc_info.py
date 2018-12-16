import pymorphy2

morph = pymorphy2.MorphAnalyzer()


class DocumentInfo:

    def __init__(self, doc_name):
        """
        :param doc_name: string: full file name
        """
        self.doc_name = doc_name
        self.companies = set()
        self.money = []


class CompanyInfo:

    def __init__(self, company):
        """

        :param company: string name
        """
        self.company = self.normal_form(company)
        self.address = None
        self.person = None
        self.abbreviation()
        self.replace_quotes()

    def normal_form(self, string):
        company_arr = string.split(" ")
        for c in range(len(company_arr)):
            company_arr[c] = company_arr[c].lower()
            if morph.parse(company_arr[c])[0].tag.case == 'nomn':
                continue
            company_arr[c] = morph.parse(company_arr[c])[0].normal_form
        return " ".join(company_arr)

    def abbreviation(self):
        if 'общество с ограниченный ответственность' in self.company:
            self.company = self.company.replace('общество с ограниченный ответственность', 'ооо')
        elif 'открытое акционерное общество' in self.company:
            self.company = self.company.replace('открытое акционерное общество', 'оао')
        elif 'акционерное общество' in self.company:
            self.company = self.company.replace('акционерное общество', 'ао')
        elif 'закрытое акционерное общество' in self.company:
            self.company = self.company.replace('закрытое акционерное общество', 'зао')
        elif 'акционерный общество' in self.company:
            self.company = self.company.replace('акционерный общество', 'ао')

    def replace_quotes(self):
        if '»' in self.company or '«' in self.company:
            self.company = self.company.replace('»', '"')
            self.company = self.company.replace('«', '"')


class MoneyInfo:

    def __init__(self, value, currency):
        """

        :param value: int value
        :param currency: string curr
        """
        self.value = value
        self.currency = currency
