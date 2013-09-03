import getpass
from numbers import Number

import requests


class OperationFailed(Exception):
    def __init__(self, method, path, expected_code, actual_code):
        self.method = method
        self.path = path
        self.expected_code = expected_code
        self.actual_code = actual_code
        self.reason = 'Failed to {method} "{path}"'.format(**locals())
        expected_codes = (expected_code,) if isinstance(expected_code, Number) else expected_code
        expected_codes_str = ", ".join(str(code) for code in expected_codes)
        msg = '''\
{self.reason}.
  Operation     :  {method} {path}
  Expected code :  {expected_codes_str}
  Actual code   :  {actual_code}'''.format(**locals())
        super(OperationFailed, self).__init__(msg)


class Client(object):
    def __init__(self, host, port=0, username=None, password=None, protocol='http'):
        if not port:
            port = 443 if protocol == 'https' else 80
        self.baseurl = '{protocol}://{host}:{port}'.format(**locals())
        self.session = requests.session()
        if username and password:
            self.session.auth = (username, password)
        print "Connecting to %s with user %s" % (self.baseurl, username)

    def _send(self, method, path, expected_code, **kwargs):
        url = self._get_url(path)
        print url
        response = self.session.request(method, url, allow_redirects=False, **kwargs)
        print response.text
        if response.status_code not in expected_code:
            raise OperationFailed(method, path, expected_code, response.status_code)
        return response

    def _get_url(self, path):
        return self.baseurl + str(path).strip()

    def add_card(self, card):
        expected_codes = [201]
        path = '/card.php/addressbooks/jp/default/example.vcf'
        self._send('PUT', path, expected_codes, data=card, headers={'Content-Type': 'text/vcard', 'If-None-Match': '*'})


if __name__ == '__main__':
    server = raw_input('enter server url: ')
    user = raw_input('enter username  : ')
    password = getpass.getpass()

    client = Client(server, username=user, password=password)
    card = """BEGIN:VCARD
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
    client.add_card(card)
