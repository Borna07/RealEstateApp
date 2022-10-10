from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-city-data/<slug:city_name>/', views.get_city_data, name='get-city-data'),
    path('deepdive/<slug:city_name>/<int:week>', views.deepDive, name='deepDive'),


]