from django.contrib import admin
from django.urls import path, include
from appquery import views



app_name = "appquery"
urlpatterns = [
    path('db/', views.DBView.as_view(), name="appquery1"),
    #path('clientdb/',views.ClientDBListAPIView.as_view(), name="clientdb" ),

]



