from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result
from sqlalchemy import create_engine
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import lxml
class Gmail(ActionRunner):

    def __init__(self, *args, **kwargs):
        self.error_status = False
        self.config = kwargs
        """Check for empty fields"""
        self.smtp = kwargs['smtp'] if 'smtp' in kwargs else None
        if self.smtp == None:
            self.smtp = 'Smtp no specified'
            self.error_status = True
        self.port = kwargs['port'] if 'port' in kwargs else None
        if self.port == None:
            self.port = 'Port not specified'
            self.error_status = True
        self.username = kwargs['username'] if 'username' in kwargs else None
        if self.username == None:
            self.username = 'No username specified'
            self.error_status = True
        self.password = kwargs['password'] if 'password' in kwargs else None
        if self.password == None:
            self.password = 'No password specified'
            self.error_status = True
        self.to = kwargs['to'] if 'to' in kwargs else None
        if self.to == None:
            self.to = 'To field not specified'
            self.error_status = True
        self.From = kwargs['from'] if 'from' in kwargs else None
        if self.From == None:
            self.From = 'From field not specified'
            self.error_status = True
        self.reply_to = kwargs['replyTo'] if 'replyTo' in kwargs else None
        self.title = kwargs['title'] if 'title' in kwargs else ''
        self.message = kwargs['message'] if 'message' in kwargs else ''
    async def run(self, void):
        if self.error_status:
            """Raise error if datas is empty"""
            raise Exception(f'Incorrect configuration:\n'
                            f'smtp: {self.smtp}\n'
                            f'port: {self.port}\n'
                            f'username: {self.username}\n'
                            f'password: {self.password}\n'
                            f'To: {self.to}\n'
                            f'From: {self.From}\n'
                            f'Reply_to: {self.reply_to}\n'
                            )
        else:
            """Create and configurate message container """
            message = MIMEMultipart('alternative')
            message['From'] = self.From
            message['To'] = self.to
            message['Subject'] = self.title
            message.add_header('reply-to', self.reply_to)

            """Cleaning self.message from HTML tags using bs4 """
            self.clearmessage = BeautifulSoup(self.message, "lxml").text

            """Creating two parts of message one with HTML tags one without"""
            part1 = MIMEText(self.clearmessage, 'plain')
            part2 = MIMEText(self.message, 'html')
            message.attach(part1)
            message.attach(part2)

            """Creating a session with STMP protocol"""
            session = smtplib.SMTP(self.smtp, self.port)
            session.ehlo()
            session.starttls()

            """Entering login and password"""
            session.login(self.username, self.password)
            session.sendmail(self.From,self.to, message.as_string())
            session.quit()
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

