import unittest
from base import http
from unittest.mock import patch

from tests.test_base import token2user, SetUpTestMailerServiceBase


@patch('base.token.token2user', token2user)
class Test(SetUpTestMailerServiceBase):

    def test(self):
        self.api(None, 'GET', self.prefix() + '/about', expected_code=http.status.OK,
                 expected_result={"service": "mailer"})

    def test_get_list_of_emails(self):
        pass

    def test_unauthorized_user_cant_send_email(self):
        self.api(None, 'PUT', self.prefix() + '/',
                 body={
                     "mail": {
                         'sender_name': 'Digital CUBE',
                         'sender_email': 'digital@digitalcube.rs',
                         'receiver_name': 'Igor',
                         'receiver_email': 'igor@digitalcube.rs',
                         'subject': 'Test sending email',
                         'body': 'Test'
                     }
                 },
                 expected_code=http.status.UNAUTHORIZED)

    def test_send_mail(self):
        self.api("TOKEN", 'PUT', self.prefix() + '/',
                 body={
                     "mail": {
                         'sender_name': 'Digital CUBE',
                         'sender_email': 'digital@digitalcube.rs',
                         'receiver_name': 'Igor',
                         'receiver_email': 'igor@digitalcube.rs',
                         'subject': 'Test sending email',
                         'body': 'Test'
                     }
                 },
                 expected_code=http.status.CREATED,
                 expected_result_contain_keys={'id'})


if __name__ == '__main__':
    unittest.main()
