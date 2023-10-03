import os 
from twilio.rest import Client
accout_ssid="AC2aafc7bcbd200fc8adac03cfa8bc8510"
auth_token="3064482eac918f7e5054b5054f887541"
client=Client(accout_ssid,auth_token)

def sendsms(phone_number):
    message=client.messages.create(
        body=f"hi your verification code is sent",
        from_="+12565738031",
        to=phone_number
    )

