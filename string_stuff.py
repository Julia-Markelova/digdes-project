"""
Methods to work with strings
"""
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def replace_quotes_dashes(string):
    """
    delete all quotes and dashes from string
    :param string: str string
    :return: string without quotes and dashes
    """
    if '»' in string or '«' or '"' or '\'' or '-' in string:
        string = string.replace('»', '')
        string = string.replace('«', '')
        string = string.replace('"', '')
        string = string.replace('\'', '')
        string = string.replace('-', '')
    return string


def normal_form(string):
    """
    normalised all words in the given string
    :param string: string to normalise
    :return: normalised string
    """
    string1 = replace_quotes_dashes(string)
    company_arr = string1.split(" ")
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
