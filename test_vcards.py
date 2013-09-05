# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_in
from vcards import Card, VcardParser

TOTO_CARD = """BEGIN:VCARD
VERSION:3.0
FN:Toto tutu
N:tutu;toto
ADR;TYPE=POSTAL:;2822 Email HQ;Suite 2821;RFCVille;PA;15213;USA
EMAIL;TYPE=INTERNET,PREF:toto@example.com
NICKNAME:the other one
NOTE:Example VCard.
ORG:Inc Copr
TEL;TYPE=WORK,VOICE:412 605 0499
TEL;TYPE=FAX:412 605 0705
URL:http://www.example.co.uk
UID:1234-5678-9000-2
END:VCARD"""

JOHN_CARD = """BEGIN:VCARD
VERSION:3.0
FN:John Doe
N:Doe;John
NICKNAME:john
NOTE:Example VCard 2.
URL:http://www.example.fr
END:VCARD"""

class TestVcard(object):
    def test_create_a_vcard(self):
        card = Card(TOTO_CARD)
        assert_equal(TOTO_CARD, card.content)
        assert_equal('tutu.toto.vcf', card.title)

    def test_parse_2_vcards_in_one_file(self):
        cards = VcardParser().parse(TOTO_CARD + '\n' + JOHN_CARD)
        assert_in(Card(TOTO_CARD), cards)
        assert_in(Card(JOHN_CARD), cards)
