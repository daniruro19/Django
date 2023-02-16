from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import GalleryImageForm
from .models import GalleryImage
#import boto3
import json
from pathlib import Path
from django.http import JsonResponse
from django.shortcuts import render, redirect
import cv2
from PIL import Image

def index(request):
    print("index")
    context = {"valor":"texto"}
    return render(request, "faceApp/index.html", context)
    #return HttpResponse("Esta es la vista")

def detalle(request, iddetalle):
    return HttpResponse("detalle %s." % iddetalle)

def upload(request):
    print(request)
    form = GalleryImageForm()
    print(form)
    return render(request, "faceApp/upload.html", { "form": form })

def manage_upload(request):
    if request.method == "POST":
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            object=form.save()
            return redirect("en_face:show_image", id=object.id)
    return redirect("en_face:index")

def process_image(request):
    #blur
    context = {
        "coordenadas": request.POST["coordenadas"],
        "lista": json.loads(request.POST["coordenadas"]),
        "imagen": request.POST["imagen"]
    }

    id=request.POST["imagen"]
    object=GalleryImage.objects.get(id = id)
    img= Image.open(object.image.url)
    for item in json.loads(request.POST["coordenadas"]):
        x= item[0]
        y= item[1]
        w= item[2]
        h= item[3]
        img[x,x+w,y,y+h] = cv2.GaussianBlur(img[x,x+w,y,y+h], (15,15),0)
    cv2.imwrite(object.image.url)
    return render(request, "en_face/process_image.html", context)

def show_image(request, id):
    print(id)
    object=GalleryImage.objects.get(id = id)
    return render(request, "faceApp/show_image.html", { "data": object })

def ajax(request, id):
    list=[]
    list.append({"x":1, "y":3})
    list.append({"x":3, "y":4})
    return JsonResponse(list, safe= False)

def usaajax(request):
    return render(request, "faceApp/usaajax.html")

