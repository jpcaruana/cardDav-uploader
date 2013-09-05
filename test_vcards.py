# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_in
from vcards import VCard, VCardParser

TOTO_CARD = """BEGIN:VCARD
VERSION:3.0
N:Toto;Tutu;;;
FN:Tutu Toto
ORG:python;
item1.EMAIL;type=INTERNET;type=pref:toto@tutu.com
REV:2013-08-29T21:50:13Z
UID:1234-5678-9000-1
END:VCARD"""

APPLE_CARD = """BEGIN:VCARD
VERSION:3.0
PRODID:-//Apple Inc.//iOS 6.1.3//EN
N:Jobs;Steve;;;
FN:Steve Jobs
ORG:python;
item1.EMAIL;type=INTERNET;type=pref:jobs@apple.com
item1.X-ABLabel:_$!<Other>!$_
REV:2013-08-29T21:50:13Z
END:VCARD"""

JOHN_CARD = """BEGIN:VCARD
VERSION:3.0
FN:John Doe
N:Doe;John
NICKNAME:john
NOTE:Example VCard 2.
URL:http://www.example.fr
UID:1234-5678-9000-1
END:VCARD"""


class TestVcard(object):
    def test_create_a_vcard(self):
        card = VCard(TOTO_CARD)
        assert_equal(TOTO_CARD, card.content)
        assert_equal('Toto.Tutu.vcf', card.title)

    def test_create_a_vcard_from_iphone(self):
        card = VCard(APPLE_CARD)
        assert_equal('Jobs.Steve.vcf', card.title)
        assert_in('UID:', card.content)

    def test_parse_2_vcards_in_one_file(self):
        cards = VCardParser().parse(TOTO_CARD + '\n' + JOHN_CARD)
        assert_in(VCard(TOTO_CARD), cards)
        assert_in(VCard(JOHN_CARD), cards)
