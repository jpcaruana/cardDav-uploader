# -*- coding: utf-8 -*-
from nose.tools import assert_equal
from vcards import Card

CARD = """BEGIN:VCARD
VERSION:3.0
FN:Toto tutu
N:tutu;toto
ADR;TYPE=POSTAL:;2822 Email HQ;Suite 2821;RFCVille;PA;15213;USA
EMAIL;TYPE=INTERNET,PREF:toto@example.com
NICKNAME:the other one
NOTE:Example VCard 2.
ORG:Inc Copr
TEL;TYPE=WORK,VOICE:412 605 0499
TEL;TYPE=FAX:412 605 0705
URL:http://www.example.co.uk
UID:1234-5678-9000-2
END:VCARD"""

class TestVcard(object):
    def test_card(self):
        card = Card(CARD)
        assert_equal(CARD, card.content)
        assert_equal('tutu.toto.vcf', card.title)
