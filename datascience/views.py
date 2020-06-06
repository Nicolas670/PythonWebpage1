import os
import io
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, CreateView
from .models import DataUpload, TextUpload
from django.urls import reverse_lazy
from collections import Counter
import requests
from io import BytesIO

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

#SKlearn libs for machine learning
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, deltaE_cie76

#open cv for color detection
import cv2



#----------------------------Helper Functions----------------------------

#Color Detection
def rgb2hex(color):
    return '#{:02x}{:02x}{:02x}'.format(int(color[0]), int(color[1]), int(color[2]))

def get_img(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def index(request):
    return render(request, "index.html")


def datascience(request):
    return render(request, "dataindex.html")


def topic_modelling(request):
    return render(request, "topic_modelling.html")


def detect_color(img):

    # Resize the image to decrease the amount of pixels and computational work
    mod_img = cv2.resize(img, (364, 600), interpolation=cv2.INTER_AREA)
    # Reshape the image to 2 dimensions (spacial and color) to fit the parameters of the KMeans classifier
    mod_img = mod_img.reshape(mod_img.shape[0] * mod_img.shape[1], 3)

    # Define number of clusters equal to given number of colors
    n_colors = 10  # Predefine n_colors as 10 for initial publishing
    clf = KMeans(n_clusters=n_colors)
    # Get the color clusters in accordance to the number of defined clusters
    labels = clf.fit_predict(mod_img)

    # Get the count of labels
    counts = Counter(labels)
    # And the center color of each cluster
    center_colors = clf.cluster_centers_

    # Combine the colors in a list
    ordered_colors = [center_colors[i] for i in counts.keys()]
    # Convert the colors to hex and rgb
    hex_colors = [rgb2hex(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    # Show pie chart with colors:
    plt.figure(figsize=(8, 6))
    plt.pie(counts.values(), labels=hex_colors, colors=hex_colors)

    # Get figure
    figure = plt.gcf()

    return figure


def color_detection(request):
    if request.method == "POST":
        # Get given image url
        given_text = str(request.POST["text"])

        # split at csrf token
        url = str.split(given_text, "&")[0]

        # Get image from url
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))

        # sklearn needs image as numpy array
        image = np.array(image)

        # Detect Colors; returns matplotlib pie chart
        figure = detect_color(image)

        # Convert figure to html displayable image
        uri = plot2uri(figure)

        # Clear old figure as otherwise the old and the new figure will be printed when applying gcf()
        plt.clf()

        # Plot image to make it json_serializable
        plt.imshow(image)
        figure_img = plt.gcf()
        uri_img = plot2uri(figure_img)

        response_data = {"pie": uri, "image": uri_img}

        return HttpResponse(json.dumps(response_data), content_type=("application/json"))

    return render(request, "color_detection.html")


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

        response_data = {"cloud": uri, "text": text, "img": img}

        return HttpResponse(json.dumps(response_data), content_type=("application/json"))

    return render(request, "upload_wordcloud_text.html")


def plot2uri(figure):
    """Converts a given matplotlib figure to an image / uri that can be displayed as html."""
    image = io.BytesIO()
    figure.savefig(image, format="png")
    image.seek((0))
    string = base64.b64encode(image.read())
    uri = urllib.parse.quote(string)

    return uri


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