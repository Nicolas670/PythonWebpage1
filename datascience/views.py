import os
import io
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView
from .models import DataUpload, TextUpload
from django.urls import reverse_lazy

from PIL import Image, ImageOps
import PIL

from .forms import UploadForm, UploadTextForm
from products.models import Product

#Data Science libs
import matplotlib.pyplot as plt
from matplotlib import pylab
import urllib, base64


#NLP Libs
from wordcloud import WordCloud


def index(request):
    return render(request, "dataindex.html")


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


#Standard upload
def upload(request):

    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("success")

    else:
        form = UploadForm()

    return render(request, "post.html", {"form": form})



#Upload Text for NLP
def upload_text(request):

    if request.method == "POST":
        form = UploadTextForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect(wordcloud)

    else:
        form = UploadTextForm()

    return render(request, "upload_text.html", {"form": form})



def success(request):
    return HttpResponse("Successfully uploaded")


def show_pictures(request):
    obj = DataUpload.objects.get(title="Lissabon2017")
    #picture = getattr(obj, "picture")
    title = getattr(obj, "title")
    title = title.replace("2017", "2018")
    picture = obj._meta.get_field("picture")
    #inverted_picture = ImageOps.invert(picture)
    #transposed = picture.transpose(Image.FLIP_LEFT_RIGHT)
    return render(request, "show_image.html", {"object": obj, "picture":picture, "title": title})


def get_model_fields(model):
    return model._meta.fields


def wordcloud(request):
    obj = TextUpload.objects.get(title="Nix")
    text_path = obj.text.path
    text_file = open(text_path, "r")
    text = text_file.read()

    #Wordcloud
    cloud = WordCloud(background_color="white", width = 500, height = 250)
    cloud.generate(text)

    #Set up matplotlib frame
    plt.figure(figsize = (20,10))
    plt.imshow(cloud, interpolation= "bilinear")
    plt.axis("off")
    #plt.plot(range(10))

    #Save as Image
    fig = plt.gcf()
    image = io.BytesIO()
    fig.savefig(image, format = "png")
    image.seek(0)
    string = base64.b64encode(image.read())
    uri = urllib.parse.quote(string)
    """
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
    graphIMG.save(image, "PNG")
    content_type = "Image/png"
    imagecontent = image.getvalue()

    graphic = (imagecontent, content_type)
    pylab.close()
    """

    graphic = plt.savefig(image, format="png")


    data = text.replace("Nix", "Everything")
    context = {"data": data, "object": obj, "cloud": uri}
    return render(request, "wordcloud.html", context)

