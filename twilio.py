from google.appengine.api import urlfetch
import base64
import urllib

account_sid = "AC34dca9d80f36198670465528e6708bac"
auth_token = "ec6a0cb73efa5011d20709af3548190d"

sms_url = 'https://api.twilio.com/2010-04-01/Accounts/%s/SMS/Messages.json' %  account_sid
from_number = '+12697434390'
auth_header_val = {'authorization': 'Basic %s' % base64.b64encode("%s:%s" % (account_sid, auth_token))}

def send_sms(phone_number, message):
    return urlfetch.fetch(sms_url,
                          urllib.urlencode(
                              {'From': from_number,
                               'To': phone_number,
                               'Body': message}),
                          urlfetch.POST,
                          auth_header_val,
                          deadline = 60)

