from django.urls import path
from . import views
from .views import index, data_upload

from .views import CreateView

urlpatterns = [
    path("", views.index, name="home"),
    path("nlp", views.nlp, name="nlp"),
    path("picture", views.picture, name="data_picture"),
    path("post/", views.data_upload, name="add_post"),
    path("display", views.show_pictures, name="display"),
    path("nlp/wordcloud", views.upload_wordcloud_text, name="upload_wordcloud_text"),
    path("display/wordcloud", views.wordcloud, name="wordcloud"),
    path("projekte", views.show_projects, name="projects"),


]