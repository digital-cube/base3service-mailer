import base
from base import http
from base import paginate
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import or_, desc
import datetime
import sendgrid
from tornado import gen
import os

if base.config.conf['apptype'] == 'monolith':
    base.route.set('prefix', base.config.conf['services']['mailer']['prefix'])
else:
    base.route.set('prefix', base.config.conf['prefix'])

import orm.models as models

import lookup.user_permissions as perm


@base.route('/about')
class AboutMailerServiceHandler(base.Base):

    @base.api()
    async def get(self):
        return {'service': 'mailer'}


@base.route('/')
class MailerServiceHandler(base.Base):
    executor = ThreadPoolExecutor(max_workers=32)

    @run_on_executor
    def sendgrid_send_email(self, sender, sender_name, receiver, receiver_name, subject, message):

        # print("SENDING MAIL TO", receiver)

        if '@' not in receiver:
            return False, "Invalid email address " + receiver

        sendgrid_api_key = os.getenv('SENDGRID_KEY')

        sg = sendgrid.SendGridAPIClient(sendgrid_api_key)
        mail = {
            'personalizations': [
                {
                    'to': [
                        {
                            'email': receiver,
                            'name': receiver_name
                        }
                    ],
                    'subject': subject
                }
            ],
            'from': {
                'email': sender,
                'name': sender_name
            },
            'content': [
                {
                    'type': 'text/html',
                    'value': message
                }
            ]
        }
        try:
            response = sg.send(mail)
            # print("RESP", response)
        except Exception as e:
            # print("E", e)
            return False, str(e)

        return True, None

    # Ne koristi se async / await vec thread executor jer se poziva sg.send a ne Asynchttp client

    @base.auth()
    @base.api()
    async def get(self, page: int = 1, per_page: int = 20, search: str = None, order_by: str = 'created',
                  order_dir: str = 'desc'):
        filters = []
        if search:
            filters.append(or_(models.Mail.subject.ilike(f'%{search}%'),
                               models.Mail.response_status.ilike(f'%{search}%'),
                               models.Mail.sender_email.ilike(f'%{search}%'),
                               models.Mail.receiver_email.ilike(f'%{search}%'),
                               ))

        _order_by = models.Mail.created
        if order_by == 'subject':
            _order_by = models.Mail.subject
        if order_by == 'receiver_email':
            _order_by = models.Mail.receiver_email
        if order_by == 'response_status':
            _order_by = models.Mail.response_status
        if order_by == 'sender_email':
            _order_by = models.Mail.sender_email

        if order_dir == 'desc':
            _order_by = desc(_order_by)

        query = self.orm_session.query(models.Mail).filter(*filters).order_by(_order_by)

        base_uri = '/api/mailer' if not search else f'/api/mailer?search={search}'

        query, summary = paginate(query, base_uri, page, per_page)

        return {'summary': summary,
                'emails': [
                    m.serialize(['id', 'sender_name', 'sender_email', 'receiver_name', 'receiver_email', 'id_receiver',
                                 'subject', 'response_status', 'sent_timestamp']) for
                    m in query]}

    @base.auth()
    @base.api()
    @gen.coroutine
    def put(self, mail: models.Mail):
        self.orm_session.add(mail)
        mail.id_user = self.id_user

        try:
            self.orm_session.commit()
        except:
            raise http.HttpInternalServerError(id_message="ERROR_STORING_EMAIL_LOCALLY",
                                               message="Error storing email locally")

        res, msg = yield self.sendgrid_send_email(mail.sender_email, mail.sender_name, mail.receiver_email,
                                                  mail.receiver_name,
                                                  mail.subject, mail.body)

        if res:
            mail.sent_timestamp = datetime.datetime.now()
            mail.response_status = 'SENT'
        else:
            mail.response_status = msg

        self.orm_session.commit()

        return {'id': mail.id}, http.status.CREATED
