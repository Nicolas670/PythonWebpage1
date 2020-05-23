from django.urls import path
from . import views
from .views import index, data_upload

from .views import CreateView

urlpatterns = [
    path("", views.index, name="home"),
    path("tools", views.datascience, name="datascience"),
    path("picture", views.picture, name="data_picture"),
    path("post/", views.data_upload, name="add_post"),
    path("display", views.show_pictures, name="display"),
    path("tools/wordcloud", views.upload_wordcloud_text, name="upload_wordcloud_text"),
    path("projekte", views.show_projects, name="projects"),
    path("tools/folium", views.create_folium_map, name="folium"),


]