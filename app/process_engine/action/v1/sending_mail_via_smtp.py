from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import Optional


class Smtp(BaseModel):
    smtp: str
    port: int
    username: str
    password: str


class Message(BaseModel):
    send_to: str
    send_from: str
    title: Optional[str] = ''
    reply_to: Optional[str] = None
    message: Optional[str] = ''


class Configuration(BaseModel):
    server: Smtp
    message: Message


class PostMan:

    def __init__(self, server: Smtp):
        self.server = server

    def _connect(self) -> smtplib.SMTP:
        """Creating a session with STMP protocol"""
        session = smtplib.SMTP(self.server.smtp, self.server.port)
        session.ehlo()
        session.starttls()
        """Entering login and password"""
        session.login(self.server.username, self.server.password)
        return session

    @staticmethod
    def _prepare_message(message: Message) -> MIMEMultipart:
        """Create and configure message container """
        message_container = MIMEMultipart('alternative')
        message_container['From'] = message.send_from
        message_container['To'] = message.send_to
        message_container['Subject'] = message.title
        message_container.add_header('reply-to', message.reply_to)
        """Cleaning self.message from HTML tags using bs4 """
        clear_message = BeautifulSoup(message.message, "lxml").text
        """Creating two parts of message one with HTML tags one without"""
        part1 = MIMEText(clear_message, 'plain')
        part2 = MIMEText(message.message, 'html')
        message_container.attach(part1)
        message_container.attach(part2)

        return message_container

    def send(self, message: Message):
        session = self._connect()
        session.sendmail(message.send_from, message.send_to, self._prepare_message(message).as_string())
        session.quit()


class Gmail(ActionRunner):
    def __init__(self, **kwargs):
        self.status = ''
        try:
            self.config = Configuration(**kwargs)
            self.post = PostMan(self.config.server)
        except Exception as exc:
            self.status += str(exc) + '\n'

    async def run(self, void):
        try:
            self.post.send(self.config.message)
        except Exception as exc:
            self.status += str(exc) + '\n'
        if not self.status == '':
            ActionRunner.console = self.status
            return Result(port='session', value=False)
        return Result(port='session', value=True)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='app.process_engine.action.v1.sending_mail_via_gmail',
            className='Gmail',
            inputs=["void"],
            outputs=['session'],
            init={
                'server': {
                    'smtp': "smtp.gmail.com",
                    'port': 587,
                    'username': None,
                    'password': None
                },
                'message': {
                    "send_to": None,
                    "send_from": None,
                    "reply_to": None,
                    "title": None,
                    "message": None
                }
            },
            version='0.1',
            license="MIT",
            author="iLLu"

        ),
        metadata=MetaData(
            name='Send mail',
            desc='Send mail via defined smtp server.',
            type='flowNode',
            width=200,
            height=100,
            icon='start',
            group=["Connectors"]
        )
    )
