from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import desc

from base import orm


class Mail(orm.BaseSql, orm.sql_base):
    __tablename__ = 'mails'

    id_user = Column(UUID, nullable=False, index=True)

    sender_name = Column(String, nullable=True)
    sender_email = Column(String, nullable=False)

    receiver_name = Column(String, nullable=True)
    receiver_email = Column(String, nullable=False)

    subject = Column(String, nullable=False)
    body = Column(String, nullable=False)

    response_status = Column(String, nullable=True)
    sent_timestamp = Column(DateTime, nullable=True)

    @staticmethod
    def order_by(s_order, order_dir):
        if s_order == 'subject':
            order = Mail.subject
        elif s_order == 'receiver_email':
            order = Mail.receiver_email
        elif s_order == 'sender_email':
            order = Mail.sender_email
        else:
            order = Mail.created

        if order_dir == 'desc':
            order = desc(order)

        return order
