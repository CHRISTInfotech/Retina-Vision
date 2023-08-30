import base64
import datetime
import io
from PIL import Image
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from counter.serializer import imageserializer
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from absl import app
from Model.retina import main
import cv2


# Create your views here.
def Login(request):
    if request.method == 'POST':
        username=request.POST.get("username")
        password=request.POST.get('pass')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.add_message(request, messages.SUCCESS, "Welcome "+request.user.username)
            return redirect('home')
        else:
            return redirect('Login')
    else:
        return render(request,"home/login.html")

# just to test, you did UI.
def home(request):
    if request.method == 'POST':

        # code to save the image to media folder
        upload = request.FILES['file-upload']
        fss = FileSystemStorage()
        file = fss.save('images/'+upload.name, upload)
        file_url = fss.url(file)
        # call the function that will test the image and return the count
        result,count = main(file)
        _, buffer = cv2.imencode('.png', result)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        # Get the base64 encoded string
        messages.add_message(request,messages.SUCCESS,"Upload Success..!")
        return render(request,'home/modelresult.html',context={
            'result': image_base64,
            'count' : count
        })
    else:
        return render(request,'home/home.html')

# API: connecting your server (django) with IOT. Where you will send POST request to the server. Ie, the image to be processed.
@api_view(['GET']) 
def stream(request):
    flask_url = "http://172.50.131.200:8080/capture_image"  # Replace with your Raspberry Pi's IP address
    response = requests.get(flask_url)
    # Modify the filename to your preferred format
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'im_{current_datetime}.jpg'
    file = "./images/"+filename
    img_path = './media/'+file
    image_bytes = io.BytesIO(response.content)
    image = Image.open(image_bytes)
    image.save(img_path)
    result,count = main(file)
    _, buffer = cv2.imencode('.png', result)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    # Get the base64 encoded string
    messages.add_message(request,messages.SUCCESS,"Upload Success..!")
    return render(request,'home/modelresult.html',context={
        'result': image_base64,
        'count' : count
    })
    

    


