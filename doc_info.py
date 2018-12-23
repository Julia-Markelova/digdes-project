"""
file with main named entities
"""
import json


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


class CompanyContracts:

    def __init__(self):
        """
        contracts_map: {company: {company-partner: number of contracts}}
        """
        self.contracts_map = {}

    def add_contract(self, company1, company2):
        """
        add companies into contracts map
        :param company1: first company name
        :param company2: second company name
        """
        if company1 not in self.contracts_map.keys():
            self.contracts_map[company1] = {}
            self.contracts_map[company1][company2] = 1

        elif company2 not in self.contracts_map[company1].keys():
            self.contracts_map[company1][company2] = 1

        else:
            count = self.contracts_map[company1][company2]
            self.contracts_map[company1][company2] = count + 1

    def get_contracts(self, company):
        """
        get info about company contracts
        :param company: company name
        :return: dict with companies-partners and count of contracts with them
        """
        return self.contracts_map[company]

    def get_contracts_number_between(self, company1, company2):
        if company1 in self.contracts_map.keys():
            if company2 in self.contracts_map[company1].keys():
                return self.contracts_map[company1][company2]
        elif company2 in self.contracts_map.keys():
            if company1 in self.contracts_map[company2].keys():
                return self.contracts_map[company2][company1]

    def save_to_json_file(self, file_name):
        """
        save contracts map to json file
        :param file_name: filename
        """
        with open(file_name, 'w+', encoding='utf-8') as f:
            json.dump(self.contracts_map, f, indent=4, ensure_ascii=False)

    def load_from_json_file(self, file_name):
        with open(file_name, 'r') as f:
            self.contracts_map = json.load(f)
