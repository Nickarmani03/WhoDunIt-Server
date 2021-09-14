"""whodunit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from whodunitapi.views.genre import GenreView
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.urls import path
from whodunitapi.views import register_user, login_user, GenreView, Profile, Movie, MovieNight
from rest_framework import routers

# If any client submits a GET request to either one of those URLs, you need to clearly state that the ViewSet will handle the request.
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'genres', GenreView, 'genre')
router.register(r'profile', Profile, 'profile')
router.register(r'movie', Movie, 'movie')
router.register(r'movie_night', MovieNight, 'movie_night')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    # Requests to http://localhost:8000/register will be routed to the register_user function
    path('register', register_user),
    
    # Requests to http://localhost:8000/login will be routed to the login_user function
    path('login', login_user),

    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
