from django.shortcuts import redirect, render
from matplotlib.style import context
import pyrebase
# Create your views here.

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

def home_view(request):
    username = request.POST.get('username')
    password = request.POST.get('pass')
    if username==None and password==None:
        return render(request, 'login.html')
    elif username in db.child('users').get().val().keys():
        if password == db.child('users').child(username).child('password').get().val():
            info = db.child('users').child(username).child('info').get().val()
            return render(request,'home.html',info)
    