from django.urls import path
from . import views
from .views import index, data_upload

from .views import CreateView

urlpatterns = [
    path("", views.index, name="data_home"),
    path("nlp", views.nlp, name="nlp"),
    path("picture", views.picture, name="data_picture"),
    path("post/", views.data_upload, name="add_post"),
    path("upload/", views.upload, name="upload"),
    path("display", views.show_pictures, name="display"),
    path("upload/text", views.upload_text, name="upload_text"),
    path("display/wordcloud", views.wordcloud, name="wordcloud"),




]