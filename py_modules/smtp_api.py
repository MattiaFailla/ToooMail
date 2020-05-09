import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

from py_modules import backend_api
from py_modules.db_api import DBApi

import configuration

current_configuration = configuration.get_current()
logger = current_configuration.logger


class SMTPApi:
    def __init__(self):
        self.userId = backend_api.get_user_id()
        self.userName = backend_api.get_user_info("mail")
        self.password = backend_api.get_user_info("password")
        self.server = backend_api.get_user_server_config("server_smtp")
        self.fromMail = backend_api.get_user_info("mail")

    def send_mail(self, subject, cc, to, body, attach=None):
        """ This function will send an email to the target email.

            :param subject: The subject of the mail.
            :param cc: The cc if any.
            :param to: The recipient.
            :param body: The body of the mail in HTML format.

            :param attach: The list of dictionaries of attachments.
            :type attach: List

            @note: The attach is a list of actual file, not the path.

            @note: example of attach:
            attach:
                [
                    {
                        fileName: "test.png",
                        file: <IO FILE>
                    },
                    {
                        fileName: "tm.docx",
                        file: <IO FILE>
                    }
                ]

        """
        msg = MIMEMultipart()
        msg['From'] = self.fromMail
        msg['To'] = to
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        # Send the mail to cc if any
        if cc is not None:
            msg['Cc'] = cc

        textVersion = body
        htmlVersion = body

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText("Text version: "+textVersion, 'plain')
        part2 = MIMEText(htmlVersion, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        if attach:
            for entry in attach:

                file = entry.file
                fileName = entry.fileName

                part = MIMEApplication(
                    file.read(),
                    Name=basename(fileName)
                )
                # After the file is closed
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
                msg.attach(part)

        smtp = smtplib.SMTP(self.server, port=587)
        smtp.starttls()
        smtp.login(
            self.userName, self.password
        )
        smtp.sendmail(self.fromMail, to, msg.as_string())
        smtp.close()
