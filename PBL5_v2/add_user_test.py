import pyrebase

config = {
    "apiKey" : "AIzaSyDar4RogfH1TQo1tDyItTQt6_LWbHtBOD4",
    "authDomain": "pbl5-arduino.firebaseapp.com",
    "databaseURL": "https://pbl5-arduino-default-rtdb.firebaseio.com",
    "projectId": "pbl5-arduino",
    "storageBucket": "pbl5-arduino.appspot.com",
    "messagingSenderId": "370500106218",
    "appId": "1:370500106218:web:cc072bddfe3d38fd312493"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

check = firebase.auth().sign_in_with_email_and_password('admin@gmail.com', '123456')
print(check['registered'])
# username = 'test1'
# password = '1234'

# db.child('users').child(username).set({'password': password})

# hum = 90
# image_encode = 'day la duong dan image'
# temp = 25
# db.child('users').child(username).child('info').set(
#     {
#         'hum' : hum,
#         'image_encode': image_encode,
#         'temp' : temp
#     }
# )
# time = '14h20p'
# db.child('users').child(username).child('public').set({
#     'time' : time
#     })


# db.child('users').child(username).child('public').child('device').set({
#     'cam bien anh sang' : {
#         'cost' : 14,
#         'count' : 2
#     },
#     'bluetooth' : {
#          'cost' : 75,
#         'count' : 5
#     }
# })

