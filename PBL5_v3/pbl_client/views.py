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

def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('pass')

    if username != None and password != None:
        if username in db.child('users').get().val().keys():
            if password == db.child('users').child(username).child('password').get().val():
                request.session['client'] = username
                return redirect('/home')
    
    if request.session.get('client'):
        return redirect('/home')

    return render(request, 'login.html')

def home_view(request):
    username = request.session.get('client')
    if username :
        info = db.child('users').child(username).child('info').get().val()
        return render(request,'home.html',info)
    else:
        return redirect('/')

def logout_view(request):
    if request.session.get('client'):
        del request.session['client']
    
    return redirect('/')

def change_pass_view(request):
    username = request.session.get('client')
    if username:
        old_pass = request.POST.get('old_pass')
        new_pass = request.POST.get('new_pass')
        new_pass_confirm = request.POST.get('new_pass_confirm')
    
        if old_pass != None and old_pass == db.child('users').child(username).child('password').get().val():
            if new_pass == new_pass_confirm:
                db.child('users').child(username).update({
                    'password' : new_pass,
                })
                return redirect('/')
                
        return render(request, 'change_pass.html')

    return redirect('/')      

def control_view(request):
    username = request.session.get('client')
    if username:
        status ,speedCradle, speedFan = db.child('users').child(username).child('control').get().val()
        print(status)
        return render(request, 'control.html')
    return redirect('/')