# -*- coding: utf-8 -*-
class VCardParser(object):
    def parse(self, vcards):
        cards = []
        lines = vcards.split('\n')
        one_card = []
        for line in lines:
            one_card.append(line)
            if line == 'END:VCARD':
                cards.append(VCard('\n'.join(one_card)))
                one_card = []
        return cards


class VCard(object):
    def __init__(self, content):
        self.content = content

    @property
    def title(self):
        lines = self.content.split('\n')
        for line in lines:
            if line.startswith("N:"):
                return line.replace('N:', '').replace(';', '.') + ".vcf"

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
                   and self.content == other.content and self.title == other.title

    def __repr__(self):
        return self.title + ":\n" + self.content
