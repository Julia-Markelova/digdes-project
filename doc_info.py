"""
file with main named entities
"""


class Document:

    def __init__(self, doc_name):
        """
        :param doc_name: string: full file name
        """
        self.doc_name = doc_name
        self.companies = set()
        self.money = set()
        self.company_client = None
        self.company_doer = None

    def __str__(self):
        print_string = "\nDocument: " + self.doc_name + "\n"
        for company in self.companies:
            print_string += "\tCompany: " + company + "\n"
        for money in self.money:
            print_string += "\tMoney: " + str(money) + "\n"
        return print_string


class Company:

    def __init__(self, file):
        """

        """
        self.file = file
        self.companies = set()
        self.company_names = set()  # compare with xml only by names
        self.address = None
        self.person = None

    def __str__(self):
        print_string = "\nCOMPANY:\n"
        for company in self.companies:
            print_string += "\tCompany: " + str(company) + "\n"
        print_string += "\tPerson: " + str(self.person) + "\n"
        return print_string


class Money:

    def __init__(self, value, currency):
        """

        :param value: int value
        :param currency: string curr
        """
        self.value = value
        self.currency = currency
