# from django.conf import settings
# from twilio.rest import Client
# import random


# class MessageHandler:
#     phone_number=None
#     otp=None
#     def __init__(self,phone_number,otp) -> None:
#         self.phone_number=phone_number
#         self.otp=otp
#     def send(self):     
#         client= Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
#         message=client.messages.create (body=f'your otp is:{self.otp}',from_=f'{settings.TWILIO_PHONE_NUMBER}',to=f'{settings.COUNTRY_CODE}{self.phone_number}')


import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])


def send(phone):
    verify.verifications.create(to=phone, channel='sms')



def check(phone, code):
    try:
        result = verify.verification_checks.create(to=phone, code=code)
    except TwilioRestException:
        return False
    return result.status == 'approved'