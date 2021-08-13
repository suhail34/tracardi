from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result
from sqlalchemy import create_engine
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import lxml
from pydantic import BaseModel
from typing import Optional

class Configuration(BaseModel):
    smtp : str
    port : int
    username : str
    password : str
    to : str
    From : str
    title: Optional[str] = ''
    replyTo: Optional[str] = None
    message: Optional[str] = ''
    @staticmethod
    def send(config):
        """Create and configurate message container """
        message = MIMEMultipart('alternative')
        message['From'] = config.From
        message['To'] = config.to
        message['Subject'] = config.title
        message.add_header('reply-to', config.replyTo)

        """Cleaning self.message from HTML tags using bs4 """
        clearmessage = BeautifulSoup(config.message, "lxml").text

        """Creating two parts of message one with HTML tags one without"""
        part1 = MIMEText(clearmessage, 'plain')
        part2 = MIMEText(config.message, 'html')
        message.attach(part1)
        message.attach(part2)

        """Creating a session with STMP protocol"""
        session = smtplib.SMTP(config.smtp, config.port)
        session.ehlo()
        session.starttls()

        """Entering login and password"""
        session.login(config.username, config.password)
        session.sendmail(config.From, config.to, message.as_string())
        session.quit()
class Gmail(ActionRunner):
    def __init__(self, *args, **kwargs):
        self.config = kwargs
        self.config = Configuration(**kwargs)
    async def run(self, void):
            Configuration.send(self.config)
            return Result(port='session', value='Mail Send!')
def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='app.process_engine.action.v1.sending_mail_via_gmail',
            className='Gmail',
            inputs=["void"],
            outputs=['session'],
            init={'smtp': "smtp.gmail.com",
                  'port': 587,
                  'username': None,
                  'password': None,
                  "to": None,
                  "from": None,
                  "replyTo": None,
                  "title": None,
                  "message": None

                  },
            version='0.1',
            license="MIT",
            author="iLLu"

        ),
        metadata=MetaData(
            name='Send mail via gmail',
            desc='Send mail via gmail.',
            type='flowNode',
            width=100,
            height=100,
            icon='start',
            group=["Gmail"]
        )
    )
