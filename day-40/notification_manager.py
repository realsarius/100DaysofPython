import smtplib
import os
from twilio.rest import Client
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NotificationManager:

    def __init__(self):
        self.smtp_address = os.environ["EMAIL_PROVIDER_SMTP_ADDRESS"]
        self.email = os.environ["MY_EMAIL"]
        self.email_password = os.environ["MY_EMAIL_PASSWORD"]
        self.twilio_virtual_number = os.environ["TWILIO_VIRTUAL_NUMBER"]
        self.twilio_verified_number = os.environ["TWILIO_VERIFIED_NUMBER"]
        self.whatsapp_number = os.environ["TWILIO_WHATSAPP_NUMBER"]
        self.client = Client(os.environ['TWILIO_SID'], os.environ["TWILIO_AUTH_TOKEN"])
        self.connection = None

    def _connect_smtp(self):
        try:
            self.connection = smtplib.SMTP(self.smtp_address)
            self.connection.starttls()
            self.connection.login(self.email, self.email_password)
            logger.info("SMTP connection established.")
        except Exception as e:
            logger.error(f"Failed to establish SMTP connection: {e}")

    def _disconnect_smtp(self):
        if self.connection:
            self.connection.quit()
            logger.info("SMTP connection closed.")

    def send_sms(self, message_body):
        try:
            message = self.client.messages.create(
                from_=self.twilio_virtual_number,
                body=message_body,
                to=self.twilio_verified_number
            )
            logger.info(f"SMS sent successfully. SID: {message.sid}")
        except Exception as e:
            logger.error(f"Failed to send SMS: {e}")

    def send_whatsapp(self, message_body):
        try:
            message = self.client.messages.create(
                from_=f'whatsapp:{self.whatsapp_number}',
                body=message_body,
                to=f'whatsapp:{self.twilio_verified_number}'
            )
            logger.info(f"WhatsApp message sent successfully. SID: {message.sid}")
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {e}")

    def send_emails(self, email_list, email_body):
        try:
            self._connect_smtp()
            for email in email_list:
                self.connection.sendmail(
                    from_addr=self.email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                )
                logger.info(f"Email sent to {email}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
        finally:
            self._disconnect_smtp()

