from django.shortcuts import render
import pyrebase
firebaseConfig = {
        'apiKey': "AIzaSyDar4RogfH1TQo1tDyItTQt6_LWbHtBOD4",
        'authDomain': "pbl5-arduino.firebaseapp.com",
        'databaseURL': "https://pbl5-arduino-default-rtdb.firebaseio.com",
        'projectId': "pbl5-arduino",
        'storageBucket': "pbl5-arduino.appspot.com",
        'messagingSenderId': "370500106218",
        'appId': "1:370500106218:web:cc072bddfe3d38fd312493",
        'measurementId': "G-D310VN8Q6V"
    }
firebase = pyrebase.initialize_app(firebaseConfig)
def login_view(request):
    email = request.POST.get('emailLogin')
    password = request.POST.get('passLogin')

    auth = firebase.auth()
    try:
        auth.sign_in_with_email_and_password(email, password)
        mess = 'Login success!'
    except:
        mess = 'Login erorr!'
    return render(request,'login.html', {'mess': mess})

def reghister_view(request):
    email = request.POST.get('emailReghister')
    password = request.POST.get('passReghister')
    confirmpass = request.POST.get('passConfirm')

    auth = firebase.auth()
    try:
        if password == confirmpass:
            auth.create_user_with_email_and_password(email, password)
            mess = 'Reghister success!'
    except:
        mess = 'Reghister erorr!'
    return render(request,'reghister.html', {'mess': mess})