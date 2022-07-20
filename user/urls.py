from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import *
urlpatterns = [
    path('',AuthOverview,name="Auth View"),
    path('signin',obtain_auth_token,name="Signin"),
    path('signup',signUp,name="Signup"),
    path('auth-user',AuthUser,name="Auth User Data")
]