from django.shortcuts import render,redirect
from login.models import User_Info
from django.contrib import messages
from django.http import JsonResponse
import datetime
import hashlib
import pickle as pkl
from Crypto.Cipher import AES
import numpy as np
import os
from django.conf import settings


cur_usr = None
key = "qk342h5jb afweliow awelrkh"

def Index(request):
    return render(request, 'base.html')

def Login(request):
    global session_start
    if request.method == 'POST':
        usr = request.POST["username"]
        pas = request.POST["pass"]
        pas = hashlib.sha256(pas.encode('UTF-8')).hexdigest()
        
        session_start = datetime.datetime.now()
        if User_Info.objects.filter(username = usr, password = pas).exists():
            user = User_Info.objects.get(username=usr)
            return render(request,'home.html', {"use": user})
        else :
            messages.error(request,'Invalid Credentials !')
            return redirect('/')

def Logout(request):
    usr = request.POST["log_user"]
    session_end = datetime.datetime.now()+datetime.timedelta(hours=5,minutes=30)
    messages.error(request,'Thank You !')
    return redirect('/')

def SignUp(request):
    return render(request,"signup.html")

def Transfer(request):
    global session_start
    usr = request.POST["username"]
    mid = request.POST["mailid"]
    dob = request.POST["dob"]
    pas = request.POST["pass"]
    pas = hashlib.sha256(pas.encode('UTF-8')).hexdigest()

    if User_Info.objects.filter(username = usr).exists():
        messages.error(request,'Username Taken !')
        return redirect('SignUp')
    elif User_Info.objects.filter(email = mid).exists():
        messages.error(request,'Email_id already exists !')
        return redirect('SignUp')
    else:
        user = User_Info(username=usr, password=pas, email=mid, dob=dob)
        user.save()
        return render(request,'home.html', {"use": user})

def Update(request):
    mid = request.POST["mailid"]
    usr = request.POST["username"]
    pas = request.POST["pass"]
    pas = hashlib.sha256(pas.encode('UTF-8')).hexdigest()

    if User_Info.objects.filter(email = mid).exists():
        messages.error(request,'Email_id already exists !')
    user = User_Info.objects.get(username=usr)
    user.email = mid
    user.password = pas
    user.save()
    return render(request,'home.html', {"use": user})

def Return(request):
    usr = request.POST["log_user"]
    user = User_Info.objects.get(username=usr)
    return render(request,'home.html', {"use": user})

def Dash(request):
    global cur_usr
    usr = request.POST.get("user",False)
    cur_usr = usr
    user = User_Info.objects.get(username=usr)
    count = User_Info.objects.exclude().count()
    return render(request, "dash.html", {"use": user, "count": count})

# encrypt & decrypt using AES

def encrypt_message(message, key):
    message = message.encode()
    padding = 16 - (len(message) % 16)
    message += bytes([padding] * padding)
    key = key[:16].encode()
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(message)
    return ciphertext


def Prediction(request):
    global cur_usr
    usr = request.POST["user"]
    cur_usr = usr
    user = User_Info.objects.get(username=usr)

    ph = request.POST['ph']
    temp = request.POST['temp']
    taste = request.POST['taste']
    odor = request.POST['odor']
    fat = request.POST['fat']
    turb = request.POST['turb']
    color = request.POST['color']

    BASE_DIR = settings.BASE_DIR
    knn_path = os.path.join(BASE_DIR, 'model', 'model.pkl')
    lbl_enc_path = os.path.join(BASE_DIR, 'model', 'lbl_enc.pkl')
    
    # inp = [6.6, 38, 0, 0, 0, 0, 253]
    inp = [ph, temp, taste, odor, fat, turb, color]
    inp = [str(x) for x in inp]
    enc = [encrypt_message(val, key) for val in inp]
    enc_int = np.array([int.from_bytes(val, byteorder='big') for val in enc]).reshape(1,-1)

    load_knn = pkl.load(open(knn_path, 'rb'))
    lbl_enc = pkl.load(open(lbl_enc_path, 'rb'))

    pred = load_knn.predict(enc_int)
    res = lbl_enc.inverse_transform(pred)[0]
    
    messages.error(request, f'Predicted Quality - {res} !')

    return render(request, "home.html", {"use": user, "pred": res})