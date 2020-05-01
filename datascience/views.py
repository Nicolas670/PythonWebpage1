from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView
from .models import DataUpload
from django.urls import reverse_lazy

from PIL import Image, ImageOps

from .forms import UploadForm
from products.models import Product


def index(request):
    return HttpResponse("Hello fellow data scientist.")


def nlp(request):
    return render(request, "lda_vis.html")


def picture(request):
    data_list = DataUpload.objects.all()
    return render(request, "data_index.html", {"data_list":data_list})


#Upload Picture
def data_upload(request):

    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("success")

    else:
        form = UploadForm()
    return render(request, "post.html", {"form": form})


#Upload Text for NLP
def upload(request):

    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("success")

    else:
        form = UploadForm()

    return render(request, "post.html", {"form": form})



def success(request):
    return HttpResponse("Successfully uploaded")


def show_pictures(request):
    #objects = DataUpload.objects.all()
    #obj = objects.filter(title="Lissabon2017")
    #fields = get_model_fields(obj)
    obj = DataUpload.objects.get(title="Lissabon2017")
    #picture = getattr(obj, "picture")
    picture = obj._meta.get_field("picture")
    #inverted_picture = ImageOps.invert(picture)
    #transposed = picture.transpose(Image.FLIP_LEFT_RIGHT)
    return render(request, "show_image.html", {"object": obj, "picture":picture})


def get_model_fields(model):
    return model._meta.fields




