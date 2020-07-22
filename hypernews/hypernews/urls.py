"""hypernews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from news.views import MyView
from news.views import NewsView
from news.views import JsonView
from news.views import CreateView
from news.views import SearchView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', MyView.as_view()),
    path('news/', NewsView.as_view()),
    path('news/<int:id>/', JsonView.as_view()),
    path('news/create/', CreateView.as_view()),
    path('news/search_results/', SearchView.as_view()),
]
urlpatterns += static(settings.STATIC_URL)
