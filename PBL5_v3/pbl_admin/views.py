from datetime import datetime as dtime
from django.shortcuts import redirect, render, get_object_or_404
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

# Manager Devices ========================

def listDevices():
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

    return zip(name_devices, image_devices, cost_devices, total_devices)

def list_devices_view(request):
    if request.session.get('check') == 'True':
        return render(request, 'list_devices.html', {'zip_devices' : listDevices})

    return redirect('/admin')

def add_devices_view(request):
    if request.session.get('check') == 'True':
        form_device = DeviceForm(request.POST or None)

        if form_device.is_valid():
            name = request.POST.get('name')
            cost = request.POST.get('cost')
            total = request.POST.get('total')
            image = request.POST.get('base64Image')

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
        cost = request.POST.get('cost')
        total = request.POST.get('total')

        image = db.child('devices').child(name).child('image').get().val()

        form_device = DeviceForm(
            request.POST or None, 
            instance=Device(name, image, cost, total)
        )

        if not form_device.is_valid:
            return redirect('/admin/devices')

        if request.POST.get('btnSave'):
            image = request.POST.get('base64Image')
            cost = request.POST.get('cost')
            total = request.POST.get('total')
            db.child('devices').child(name).update({
                'image' : image,
                'cost' : cost,
                'total' : total,
            })

            return redirect('/admin/devices')

        context = {
            'form_device' : form_device,
            'base64_image' : image,
            'title' : 'Cập nhật thiết bị',
            }

        return render(request, 'manager_devices.html', context)
    
    return redirect('/admin')

def delete_devices_view(request):
    if request.session.get('check') == 'True':
        name = request.POST.get('name')

        db.child('devices').child(name).remove()

        return redirect('/admin/devices')
    
    return redirect('/admin')

# ======================================

# Manager User ==========================
def list_user_view(request):
    if request.session.get('check') == 'True':
        users = db.child('users').get().val()
        fullnames = []
        for i in users:
            fullnames.append(db.child('users').child(i).child('fullname').get().val())
        
        zip_user = zip(fullnames, users)
        return render(request, 'list_user.html', {'zip_user' : zip_user})
    else:
        return redirect('/admin')

def create_user_view(request):
    if request.session.get('check') == 'True':
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        password = request.POST.get('pass')

        if username == None or password == None:
            return render(request, 'create_user.html')
        db.child('users').child(username).set({
            'password': password,
            'fullname' : fullname
            })
    
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
        id = db.child('users').child(username).child('history').get().val()
        if id == None:
            return render(request, 'list_device_user.html', {'check' : False, 'username' : username})
        else:
            name_device = []
            cost_device = []
            count_device = []
            sum_device = []
            date_device = []

            for i in id:
                names = db.child('users').child(username).child('history').child(i).get().val()
                for j in names:
                    cost = db.child('users').child(username).child('history').child(i).child(j).child('cost').get().val()
                    count = db.child('users').child(username).child('history').child(i).child(j).child('count').get().val()
                    date = db.child('users').child(username).child('history').child(i).child(j).child('date').get().val()
                
                    name_device.append(j)
                    cost_device.append(cost)
                    count_device.append(count)
                    date_device.append(date)
                    sum_device.append(int(cost)*int(count))

            zip_device = zip(name_device, cost_device, count_device, sum_device, date_device)
            
            context = {
                'username' : username,
                'zip_device' : zip_device,
                'check' : True,
                'sum_all' : sum(sum_device),
            }
            return render(request, 'list_device_user.html', context)

    return redirect('/admin')

def getDevicesByName(name):
    cost = db.child('devices').child(name).child('cost').get().val()
    total = db.child('devices').child(name).child('total').get().val()

    return cost, total

def add_device_user_view(request, username):
    if request.session.get('check') == 'True':
        products = request.POST.getlist('confirm[]')
        counts = request.POST.getlist('count[]')

        if products != []:
            setIdDevices = dtime.now().strftime("%Y-%m-%d-%H-%M-%S")
            for i, j in zip(products, counts):
                
                cost, total = getDevicesByName(i)

                db.child('users').child(username).child('history').child(setIdDevices).child(i).set({
                    'cost' : cost,
                    'count' : j,
                    'date' : dtime.now().strftime("%d/%m/%Y")
                })

                db.child('devices').child(i).update({
                    'total' : str(int(total) - int(j)),
                })

            return redirect('/admin/' + username + '/history')

        zip_devices_user = listDevices()

        return render(request, 'add_devices_user.html', {'zip_devices_user' : zip_devices_user})
    
    return redirect('/admin')

# ========================================

