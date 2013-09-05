import getpass
from numbers import Number
import requests
from vcards import VCardParser


class OperationFailed(Exception):
    def __init__(self, method, path, expected_code, actual_code, response_text):
        self.method = method
        self.path = path
        self.expected_code = expected_code
        self.actual_code = actual_code
        self.reason = 'Failed to {method} "{path}"'.format(**locals())
        expected_codes = (expected_code,) if isinstance(expected_code, Number) else expected_code
        expected_codes_str = ", ".join(str(code) for code in expected_codes)
        msg = '''\
{self.reason}.
  Operation            :  {method} {path}
  Expected code        :  {expected_codes_str}
  Actual code          :  {actual_code}
  Response from server : {response_text}'''.format(**locals())
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
        response = self.session.request(method, url, allow_redirects=False, **kwargs)
        if response.status_code not in expected_code:
            raise OperationFailed(method, path, expected_code, response.status_code, response.text)
        return response

    def _get_url(self, path):
        return self.baseurl + "/" + str(path).strip()

    def add_card(self, card, addressbook_path):
        expected_codes = [201]
        path = addressbook_path + '/' + card.title
        self._send('PUT', path, expected_codes, data=card.content, headers={'Content-Type': 'text/vcard', 'If-None-Match': '*'})


if __name__ == '__main__':
    server = raw_input('enter server url (without http) : ')
    addressbook_path = raw_input('enter addressbook path : ')
    user = raw_input('enter username: ')
    password = getpass.getpass()
    client = Client(server, username=user, password=password)

    vcards_file = raw_input('enter vcards filename: ')
    with open(vcards_file) as f:
        cards = VCardParser().parse(f.read())
        for card in cards:
            print "Importing " + card.title
            client.add_card(card, addressbook_path)

    print "\nImport done !"
