from django.shortcuts import render
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

def create_user_view(request):
    username = request.POST.get('username')
    password = request.POST.get('pass')

    db.child('users').child(username).set({'password': password})

    return render(request, 'create_user.html')

def list_user_view(request):
    users = db.child('users').get().val()
    username = []
    time = []
    for i in users:
        username.append(i)
        time.append(db.child('users').child(i).child('public').child('time').get().val().__str__())
    
    zip_user = zip(username, time)
    return render(request, 'list_user.html', {'zip_user' : zip_user})

def list_device_user_view(request, username):
    devices = db.child('users').child(username).child('public').child('device').get().val()
    if devices == None:
        return render(request, 'list_device_user.html', {'check' : False})
    else:
        mess = ''
        name_device = []
        cost_device = []
        count_device = []

        for i in devices:
            name_device.append(i)
            cost_device.append(db.child('users').child(username).child('public').child('device').child(i).child('cost').get().val())
            count_device.append(db.child('users').child(username).child('public').child('device').child(i).child('count').get().val())

        zip_device = zip(name_device, cost_device, count_device)
        return render(request, 'list_device_user.html', {'zip_device' : zip_device, 'check' : True})