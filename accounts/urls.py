"""hollymovies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from accounts.models import Profile
from accounts.views import SubmittableLoginView, SignUpView, SubmittablePasswordChangeView, ProfileDetailsView, \
    ProfileUpdateView

app_name = 'accounts'
urlpatterns = [
    path('login/', SubmittableLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', SubmittablePasswordChangeView.as_view(), name='password_change'),
    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile'),
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='update_profile'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
]