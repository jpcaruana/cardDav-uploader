# -*- coding: utf-8 -*-
class Card(object):
    def __init__(self, content):
        self.content = content

    @property
    def title(self):
        lines = self.content.split('\n')
        for line in lines:
            if line.startswith("N:"):
                return line.replace('N:', '').replace(';', '.') + ".vcf"
