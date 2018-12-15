
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
        self.company = company
        self.address = None
        self.person = None


class MoneyInfo:

    def __init__(self, value, currency):
        """

        :param value: int value
        :param currency: string curr
        """
        self.value = value
        self.currency = currency
