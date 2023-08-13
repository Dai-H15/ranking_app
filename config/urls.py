"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from login import views as login_views
from main import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls,name="admin"),
    path("signup/",login_views.signup_view ,name="signup"),
    path("login/",login_views.login_view ,name="login"),
    path("logout/",login_views.logout_view ,name="logout"),
    path("",main_views.index , name ="index"),
    path("ranking_progress/",main_views.ranking_progress,name="ranking_progress"),
    path("ranking_regist/",main_views.regist,name="ranking_regist"),
    path("settings/",main_views.settings,name="settings"),
    path("join/",main_views.join,name="join"),
    path("set_table/",main_views.set_table,name="set_table"),
    path("inquiry/",main_views.inquiry,name="inquiry"),
    path("results/",main_views.results,name="results"),
    path("calculate/",main_views.calculate,name="calculate"),
]