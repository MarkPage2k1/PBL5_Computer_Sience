# django
from django.shortcuts import redirect, render
from matplotlib.style import context
import requests
import pyrebase

#import model emoji detection
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

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
        temp = db.child('users').child(username).child('info').child('temp').get().val()
        hum = db.child('users').child(username).child('info').child('hum').get().val()
        image_encode = db.child('users').child(username).child('info').child('image_encode').get().val()
        emoji = getEmoji(image_encode)

        info = {
            'temp' : temp,
            'hum' : hum,
            'image_encode' : image_encode,
            'emoji' : emoji,
        }

        return render(request,'home.html',info)

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
    
        if old_pass and old_pass == db.child('users').child(username).child('password').get().val():
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
        statusCradle = request.POST.get('cbCradle')
        statusFan = request.POST.get('cbFan')
        Auto = request.POST.get('Auto')

        btnSave = request.POST.get('Save')

        if btnSave is None:
            AutoDB = db.child('users').child(username).child('control').child('auto').get().val()
            statusCradleDB = db.child('users').child(username).child('control').child('status_cradle').get().val()
            statusFanDB = db.child('users').child(username).child('control').child('status_fan').get().val()

            context = {
                'auto' : AutoDB,
                'statusCradle' : statusCradleDB,
                'statusFan' : statusFanDB,
            }

            return render(request, 'control.html', context)

        Auto = 'OFF' if Auto is None else 'ON'
        statusCradle = 'OFF' if statusCradle is None else 'ON'
        statusFan = 'OFF' if statusFan is None else 'ON'


        db.child('users').child(username).child('control').update({
                'auto' : Auto,
                'status_cradle' : statusCradle,
                'status_fan' : statusFan
            })

        return redirect('/control')
    return redirect('/')

def getEmoji(urlImage):
    if urlImage:
        model = load_model('keras_model.h5')

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        image = Image.open(requests.get(urlImage, stream=True).raw)
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    
        data[0] = normalized_image_array

        prediction = model.predict(data)
        pred = np.argmax(prediction)

        label = ["Khóc", "Hạnh phúc", "Ngủ"]

        return label[pred]
    
    return None
        