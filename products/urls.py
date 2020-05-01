from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="products"),
    path("new", views.new, name="new_products"),


]