from django.urls import path
from .views import *


app_name = "accounts"
urlpatterns = [
    path('signup/',signupView,name="signup"),
    path('login/',loginView,name="login"),
    path('logout/',logoutView,name="logout"),
]