
from django.contrib import admin
from django.urls import path
from app1.api import views 
from app1.api.views import *

urlpatterns = [
    path('list/', WatchlistAV.as_view() , name="list"),
    path('list/<int:pk>/' , WatchdetailsAV.as_view() , name = "list_detail"),
    path('platform/', StreamingPlatformListAV.as_view(), name="platform" ),
    path('list/<str:name>/', CategoryListAV.as_view(), name = "category"),
    path('platform/<int:pk>/', StreamingPlatformdetailsAV.as_view(), name="platform_detail"),
    path('list/<int:pk>/review/', ReviewlistAV.as_view(), name="review"),
    path('list/<int:pk>/createreview/', ReviewCreate.as_view(), name="Create_review"),
    path('list/review/<int:pk>/', ReviewDetailsAV.as_view(), name="review_details"),
    path('user/<str:username>/', ReviewUser.as_view(), name = "ReviewUser"),
]
