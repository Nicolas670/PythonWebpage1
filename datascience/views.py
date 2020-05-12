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

#Generating IDs:
import uuid


#Data Science libs
import matplotlib.pyplot as plt
from matplotlib import pylab
import urllib, base64
import numpy as np


#NLP Libs
from wordcloud import WordCloud, ImageColorGenerator


def index(request):
    return render(request, "index.html")


def nlp(request):
    return render(request, "dataindex.html")


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
def upload_wordcloud_text(request):

    if request.method == "POST":
        form = UploadTextForm(request.POST, request.FILES)

        if form.is_valid():
            id = str(uuid.uuid4())
            #form.__setattr__("title","hanswurst")
            new_text = form.save(commit=False)
            new_text.id = id
            new_text.save()

            #bind title to session to retrieve it after the redirect. The title is needed for finding the correct text doc.
            request.session["id"] = id
            return redirect(wordcloud)

    else:
        form = UploadTextForm()

    return render(request, "upload_wordcloud_text.html", {"form": form})


def success(request):
    return HttpResponse("Successfully uploaded")


def show_pictures(request):
    obj = DataUpload.objects.get(title="Lissabon2017")
    title = getattr(obj, "title")
    title = title.replace("2017", "2018")
    picture = obj._meta.get_field("picture")
    #inverted_picture = ImageOps.invert(picture)
    #transposed = picture.transpose(Image.FLIP_LEFT_RIGHT)
    return render(request, "show_image.html", {"object": obj, "picture":picture, "title": title})


def get_model_fields(model):
    return model._meta.fields


def wordcloud(request):

    id = request.session.get("id", "")
    obj = TextUpload.objects.get(id=id)
    text_path = obj.text.path
    text_file = open(text_path, "r")
    text = text_file.read()

    #Wordcloud
    cloud = WordCloud(background_color="white", width = 500, height = 250, max_font_size=100, min_font_size=10, max_words=50)
    cloud.generate(text)
    mask = np.array(Image.open("Static/images/warm-color-mask2.jpg"))
    plt.imshow(mask)
    image_colors = ImageColorGenerator(mask)


    #Set up matplotlib frame
    plt.figure(figsize = (20,10))
    plt.imshow(cloud.recolor(color_func=image_colors), interpolation= "bilinear")
    plt.axis("off")
    #plt.plot(range(10))


    #Save as Image
    fig = plt.gcf()
    image = io.BytesIO()
    fig.savefig(image, format = "png")
    image.seek(0)
    string = base64.b64encode(image.read())
    uri = urllib.parse.quote(string)

    graphic = plt.savefig(image, format="png")


    data = text.replace("Nix", "Everything")
    context = {"data": data, "object": obj, "cloud": uri}
    return render(request, "wordcloud.html", context)


def show_projects(request):
    return render(request, "projects.html")