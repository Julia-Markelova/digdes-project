"""
here is natasha named entity recognition
"""
from doc_info import *
from natasha import AddressExtractor, OrganisationExtractor, MoneyExtractor
from ner_stuff import Extractor

ignore_arr = ['/home/yulia/Рабочий стол/digdes/Uploads/00b/aacda0c43805abdb599b7ce50cb33.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/16b76c3f92cbc79b77a66db99f03d.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/f0ea6af68e668dbfa4198a4363b89.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/9950ce5a38ee85b0e106db097b22d.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/2a9591c17e3aebaa98c5aacb1894f.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/65f211db67d202d6d9810b8b501c4.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/971e630fc295ed8361c99aab7b078.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00b/10c7f77e3f5752add9d1b6e3ad729.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/000/dd0484a61204db2c799515f7b5264.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/000/999228967c5940d881f239200d649.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/000/80d7990b0853f2215ca9059c95e17.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/000/a888d8cab352af8f81de1179e27ba.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/000/97b7b5e9870966d0de063c0b01dcb.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/001/cc7ae592b4f773785ab1dc1cd181e.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/001/c1919dd680f4fc6806e925d528566.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/001/6531b34690967cd2a69a27b857d01.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/002/211f1216982f5865d38143fb21b31.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/002/7760b4903d229e8db81a96666afea.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/002/7348aa265cd0a1b6d209211b84bd4.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/002/edd2a4eada1e1ca24069393f356c4.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/002/e6ceb692775485ec61db059f38380.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/002/d0995bb6142227cfbe8b8994aaf0c.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/003/97ca4cc552b64ae702dd3402aab37.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/003/38a76a2731674349727cf5ac7f8b9.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/003/59a9e31f021609caa7ceb1e8839a0.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/004/2ab270a7c57a6b7c9b3d61316188b.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/004/d9922f95507bac1ba491461c28991.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/004/fc530b75c6f85975109d09ae15c01.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/004/f7921e94bc0f18ee12dc76b7bed9a.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/004/81bbda6c71b5bdd26d568b4f9f89f.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/004/ee51fc02a5cb4ff72ac47bdc9ecc3.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/005/fadaa318f8e846d0f688359b79150.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/005/3f41891719e11498e4d03657285e0.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/005/fbc390ce83aad1ece2de5c0370268.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/006/5eb822472031075f487a56ede8a34.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/006/de14f11f27f16fe5f02742a9335c9.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/006/d85695aa9238f98c2203248b8218b.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/006/d2850b9dad52b202e3e9dfeabc760.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/006/2ab835838428b7b56c06c2b361a3b.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/006/7cb18f60d25972f4f19c9704ecd5e.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/006/96cd48432b8aa317457cc6fed3a23.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/007/b13a6e8f802e64c67c42d43183933.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/007/07148a8ee84575e39c8a6396a4f5d.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/007/279e63a1c422b1d03a88bad4f45bc.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/007/8aaafbee7093ca7a5aea0dc91fb4b.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/008/9597d823350ccb3f3455814a1e786.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/008/fc2e7e16cb35d014d61d66402b9fa.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/008/ac95ffc3eb225751fa888dd30be44.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/008/016a6203468e04ddbe4c1751ec7ed.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/009/c8daf29b8fb792c0873c90f3ac04c.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/009/e05c1316982b5176004f2871be23b.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/009/5b5dffb7f23fe85e2eec57a4a180a.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/009/2eff7aad7d2d721f06d04e93b116f.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/009/79b552a10c7af53de55b2765a4776.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/009/b3b56a15edbd038218c9fc7d91339.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00a/a0f360fcd8ccf54e7715629960a8a.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00a/3ec005dcbb444f1fae93cc6455fa1.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00a/d97218d62cd16de6415c1101540d1.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00a/cab00c2f45953baa0c48398480c69.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00a/0c0fa64856e6dde447bba88f64cb0.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00a/fcceeac334a7267e094eb7f2e5c7a.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00a/d4ea026e076de0c66eb24e8784ecd.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00a/85345c46b771281b616c12e073373.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00a/812285ed72cf2f7a98d1927a03fa5.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00a/8213c9fce677471093a00681976e2.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00a/b00c534169b2b59fa7ba0ca07f6e6.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00c/99eec7169a492259339a9300e3b7b.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00c/3ed099197fd650bf17d8108fd8361.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00c/97d19aaad501ce165a0afa71ddddb.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00c/9c2ab891e00a16e0275784c392c1d.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00c/cb5bae5eec714557bea0f14fc25a1.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00c/8156ba32a8082d4b8a8e7b4ece8c0.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00c/dca6e1c93415b85bb7670e6815912.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00d/d584e77fe89d3bd3925f3ea8b69d4.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00d/429a0ff74ba89842a0a9837bf316e.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00d/c49918b9fd76c0055d0386b46d434.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00e/6f550f29c0c951867dd4ffe16ff11.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00e/f3e3c7a0a6d67c6c0d8b0c78318f6.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00e/2751d50d48a13300111f747a3d837.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00e/ed2b815552084e83b02f237663480.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00e/3eb1913e3582095546284f7763ae8.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00e/6786baa29095f846eccb7d0cf5eb8.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00f/e77dac687d6deb4345e276bed5408.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00f/2b7b8715cf30f0495a8ba1336a64e.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00f/5d7e0d535a50e1cd5732e2bd6383f.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00f/f3bfd9e43ef91f34f2c46b7c5ced7.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00f/d1d3728823801891d00c3c1a4ebc5.xml',
              '/home/yulia/Рабочий стол/digdes/Uploads/00f/60b029d152728f8f515bf3f5eef38.xml']


class NatashaExtractor(Extractor):

    def __init__(self, text, file, doc):
        super().__init__(text, doc)
        self.file = file

    def __extract_organizations__(self):
        """
        extract info about organisations from a text and save it to a Document.
        Check if file is not in ignore list (there are files which call RecursionError)
        :return: Document obj with a set of organisations
        """
        if self.file in ignore_arr:  # only for organisations -_-
            return self.doc

        extractor = OrganisationExtractor()
        matches = extractor(self.text)

        for match in matches:
            self.doc.companies.add(match.fact.name)

        return self.doc

    def __extract_money__(self):
        """
        extract money from text
        :return: Document
        """
        extractor = MoneyExtractor()
        matches = extractor(self.text)

        for match in matches:
            value = Money(match.fact.integer, match.fact.currency)
            self.doc.money.add(value.value)

        return self.doc

    def extract_compare_money(self):
        """
        extract money from text and compare it with money from xml-file
        """
        self.doc = self.__extract_money__()
        self.__compare_money_with_xml__()

    def extract_compare_organizations(self):
        """
        extract organizations from text and compare them with organizations from xml-file
        """
        self.doc = self.__extract_organizations__()
        self.__compare_organizations_with_xml__()


def extract_address(text):
    # ADDRESS
    extractor = AddressExtractor()
    matches = extractor(text)
    spans = [_.span for _ in matches]  # !
    address = text[spans[0][0]:spans[0][1]]
    # TODO: remove print
    print(address)
