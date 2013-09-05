# -*- coding: utf-8 -*-
class VCardParser(object):
    def parse(self, vcards):
        cards = []
        lines = vcards.replace('\n ', '').split('\n')
        one_card = []
        for line in lines:
            one_card.append(line.strip())
            if line.startswith('END:VCARD'):
                cards.append(VCard('\n'.join(one_card)))
                one_card = []
        return cards


class VCard(object):
    def __init__(self, content):
        self.title = self.parse_title(content) + ".vcf"
        self.content = self.parse_content(content)

    def parse_content(self, content):
        card = []
        lines = content.split('\n')
        found_uid = False
        for line in lines:
            if line.startswith('UID:'):
                found_uid = True
            if line.startswith('END:VCARD') and not found_uid:
                card.append('UID:' + self.title)
            card.append(line)
        return '\n'.join(card)

    def parse_title(self, content):
        try_parse = lambda prefix: self._parse_field(content, prefix)
        return try_parse('N:') or try_parse('FN:')

    def _parse_field(self, content, field_prefix):
        for line in content.split('\n'):
            if line.startswith(field_prefix):
                line = line.replace(field_prefix, '')
                elements = [l.strip() for l in line.split(';') if l.strip() != '']
                return '.'.join(elements) if elements else None

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
                   and self.content == other.content and self.title == other.title

    def __repr__(self):
        return self.title + ":\n" + self.content
