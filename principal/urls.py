from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('search/', views.search_view, name='search_view'),
    path('stream/<str:username>/', views.usuario_stream_view, name='usuario_stream'),
]