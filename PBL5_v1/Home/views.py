from django.shortcuts import render
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
authe = firebase.auth()
database = firebase.database()
 
def home_view(request):
    context = {
        'image_encode' : database.child('test').child('image_encode').get().val(),
        'status' : database.child('test').child('status').get().val(),
        'time' : database.child('test').child('time').get().val(),
        'temp' : database.child('test').child('temp').get().val(),
        'hum' : database.child('test').child('hum').get().val()
    }
    return render(request, 'home.html' ,context)
