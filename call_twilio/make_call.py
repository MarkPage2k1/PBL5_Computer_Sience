import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# to_phone = '+84344490049'
to_phone = "+84376321178"


call = client.calls.create(
                        twiml='''
                            <Response>
                                <Say voice="alice">Hi guest! Good morning!</Say>
                                <Play>https://avocado-gecko-8624.twil.io/assets/viendanbac.mp3</Play>
                            </Response>''',
                        to = to_phone,
                        from_='+17349549326',
                        # url = "http://demo.twilio.com/docs/voice.xml"      
                    )

print(call.sid)
print()
print("Waiting ...")

while True:
    calls = client.calls.list(limit=1)
    if (calls[0].status != "ringing" and calls[0].status != "queued" and calls[0].status != "completed" and calls[0].status != "in-progress"):
        print("ID: " + calls[0].sid)
        print("Stattus: " + calls[0].status)
        print("Duration: " + calls[0].duration)
        print("Duration: " + calls[0].to)

        message = client.messages.create(
            to = to_phone,
            from_='+17349549326',
            body="Are you a hacker? We recently discovered that your IP address illegally accessed our server. If you have done these things, we ask that you stop doing this. If the situation persists, we will file a lawsuit. Looking forward to your cooperation!")
        print(message.sid)
        break
    elif calls[0].status == "completed":
        print(" -- DONE -- ")
        break