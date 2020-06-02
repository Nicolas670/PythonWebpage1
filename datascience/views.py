import os
import io
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, CreateView
from .models import DataUpload, TextUpload
from django.urls import reverse_lazy

from PIL import Image, ImageOps
import PIL

from .forms import UploadForm, UploadTextForm

import json
from django.forms.models import model_to_dict

#Generating IDs:
import uuid


#Data Science libs
import matplotlib.pyplot as plt
from matplotlib import pylab
import urllib, base64
import numpy as np

#Folium
import folium
from geopy.geocoders import Nominatim

#NLP Libs
from wordcloud import WordCloud, ImageColorGenerator


def index(request):
    return render(request, "index.html")


def datascience(request):
    return render(request, "dataindex.html")

def topic_modelling(request):
    return render(request, "topic_modelling.html")

def create_folium_map(request):

    if request.method == "POST":
        country = request.POST["text"]
        #city = request.POST["city"]

        geolocator = Nominatim(user_agent="get_ll", timeout=3)

        #Get coordinates for given location
        location = geolocator.geocode(country)
        latitude = location.latitude
        longitude = location.longitude

        #generate folium map for given country(or other location)
        folium_map = folium.Map(location = [latitude, longitude], zoom_start=6)

        #Add City marker if city was provided
        """if city:
            city_latitude = city.latitude
            city_longitude = city.longitude
            city = {"Latitude": city_latitude, "Longitude": city_longitude, "City": city}

            # add markers to map
            for lat, lng, city in zip(city['Latitude'], city['Longitude'], city['City']):
                label = '{}'.format(city)
                label = folium.Popup(label, parse_html=True)
                folium.CircleMarker(
                    [lat, lng],
                    radius=5,
                    popup=label,
                    color='blue',
                    fill=True,
                    fill_color='#3186cc',
                    fill_opacity=0.7,
                    parse_html=False).add_to(folium_map)"""

        context = folium_map._repr_html_() #model_to_dict(folium_map.get_root())

        return HttpResponse(json.dumps(context), content_type=("application/json"))

    return render(request, "folium.html")


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
        #get provided text
        text = str(request.POST["text"])

        #Instantiate Wordcloud
        cloud = WordCloud(background_color="black",width = 500, height = 250,max_font_size=100)
        cloud.generate(text)

        #Set Wordcloud Colors with mask
        mask = np.array(Image.open("Static/images/warm-color-mask2.jpg")) #Use absolute path in production: "/home/Nicolas1a6/PythonWebpage1/static/images/warm-color-mask2.jpg"
        plt.imshow(mask)
        image_colors = ImageColorGenerator(mask)

        # Set up matplotlib frame
        plt.figure(figsize=(20, 10))
        plt.imshow(cloud.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis("off")

        # Save as Image
        fig = plt.gcf()
        image = io.BytesIO()
        fig.savefig(image, format="png")
        image.seek(0)
        string = base64.b64encode(image.read())
        uri = urllib.parse.quote(string)

        graphic = plt.savefig(image, format="png")

        #wc = DataUpload(picture=graphic, title = "sample")
        #wc.save

        response_data = {"cloud": uri, "text": text}

        return HttpResponse(json.dumps(response_data), content_type=("application/json"))

    return render(request, "upload_wordcloud_text.html")


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



def show_projects(request):
    return render(request, "projects.html")