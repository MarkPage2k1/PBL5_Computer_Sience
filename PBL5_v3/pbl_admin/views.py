from django.shortcuts import redirect, render
import pyrebase

from pbl_admin.models import Device

from .forms import DeviceForm
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

# Login =================================
def login_admin_view(request):
    email = request.POST.get('email')
    password = request.POST.get('pass')

    if email != None and password != None:
        try:
            firebase.auth().sign_in_with_email_and_password(email, password)
            request.session['check'] = 'True'
            return redirect('/admin/home')
        except:
            request.session['check'] = 'False'
    
    if request.session.get('check') == 'True':
        return redirect('/admin/home')

    return render(request, 'login_admin.html')

def logout_admin_view(request):
    if request.session.get('check') == 'True':
        del request.session['check']
    return redirect('/admin')

# =======================================

# Manager User ==========================
def list_user_view(request):
    if request.session.get('check') == 'True':
        users = db.child('users').get().val()
        time = []
        for i in users:
            time.append(db.child('users').child(i).child('public').child('time').get().val())
        
        zip_user = zip(users, time)
        return render(request, 'list_user.html', {'zip_user' : zip_user})
    else:
        return redirect('/admin')

def create_user_view(request):
    if request.session.get('check') == 'True':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        if username == None or password == None:
            return render(request, 'create_user.html')
        db.child('users').child(username).set({'password': password})
    
    return redirect('/admin')

def delete_user_view(request, username):
    if request.session.get('check') == 'True':
        if request.POST.get('btnDelete') == 'Yes':
            db.child('users').child(username).remove()

            return redirect('/admin')
            
        return render(request, 'delete_user.html', {'username' : username})
    
    return redirect('/admin')

def list_device_user_view(request, username):
    if request.session.get('check') == 'True':
        devices = db.child('users').child(username).child('public').child('device').get().val()
        if devices == None:
            return render(request, 'list_device_user.html', {'check' : False, 'username' : username})
        else:
            cost_device = []
            count_device = []
            sum_device = []

            for i in devices:
                cost = db.child('users').child(username).child('public').child('device').child(i).child('cost').get().val()
                count = db.child('users').child(username).child('public').child('device').child(i).child('count').get().val()
                
                cost_device.append(cost)
                count_device.append(count)
                sum_device.append(int(cost)*int(count))

            zip_device = zip(devices, cost_device, count_device, sum_device)
            
            context = {
                'username' : username,
                'zip_device' : zip_device,
                'check' : True,
                'sum_all' : sum(sum_device),
            }
            return render(request, 'list_device_user.html', context)

    return redirect('/admin')

def add_device_user_view(request, username):
    if request.session.get('check') == 'True':
        name_devices = db.child('devices').get().val()
        image_devices = []
        cost_devices = []
        total_devices = []

        for i in name_devices:
            image_devices.append(db.child('devices').child(i).child('image').get().val())
            cost_devices.append(db.child('devices').child(i).child('cost').get().val())
            total_devices.append(db.child('devices').child(i).child('total').get().val())

        zip_devices_user = zip(name_devices, image_devices, cost_devices, total_devices)
        return render(request, 'add_devices_user.html', {'zip_devices_user' : zip_devices_user})
    
    return redirect('/admin')

# ========================================

# Manager Devices ========================
def list_devices_view(request):
    if request.session.get('check') == 'True':
        name_devices = db.child('devices').get().val()
        
        image_devices = []
        cost_devices = []
        total_devices = []

        for i in name_devices:
            image_devices.append(
                db.child('devices').child(i).child('image').get().val()
            )

            cost_devices.append(
                db.child('devices').child(i).child('cost').get().val()
            )

            total_devices.append(
                db.child('devices').child(i).child('total').get().val()
            )

        zip_devices = zip(name_devices, image_devices, cost_devices, total_devices)
        return render(request, 'list_devices.html', {'zip_devices' : zip_devices})

    return redirect('/admin')

def add_devices_view(request):
    if request.session.get('check') == 'True':
        form_device = DeviceForm(request.POST or None)

        if form_device.is_valid():
            name = request.POST.get('name')
            image = request.POST.get('image')
            cost = request.POST.get('cost')
            total = request.POST.get('total')

            db.child('devices').child(name).set({
                'image' : image,
                'cost' : cost,
                'total' : total,
            })

            return redirect('/admin/devices')
        return render(request, 'manager_devices.html', {'form_device' : form_device, 'title' : 'Thêm thiết bị'})
    
    return redirect('/admin')

def update_devices_view(request):
    if request.session.get('check') == 'True':
        name = request.POST.get('name')
        image = request.POST.get('image')
        cost = request.POST.get('cost')
        total = request.POST.get('total')
        
        form_device = DeviceForm(
            request.POST or None, 
            instance=Device(name, image, cost, total)
        )

        if not form_device.is_valid():
            return redirect('/admin/devices')

        if request.POST.get('btnSave'):
            db.child('devices').child(name).update({
                'image' : image,
                'cost' : cost,
                'total' : total,
            })

            return redirect('/admin/devices')

        return render(request, 'manager_devices.html', {'form_device' : form_device, 'title' : 'Cập nhật thiết bị'})
    
    return redirect('/admin')

def delete_devices_view(request):
    if request.session.get('check') == 'True':
        name = request.POST.get('name')

        db.child('devices').child(name).remove()

        return redirect('/admin/devices')
    
    return redirect('/admin')

# ======================================