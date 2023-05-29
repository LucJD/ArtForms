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
from app.views import *

urlpatterns = [
    path("client/view-artists/", viewArtistsView, name="client-view-artists"),
    path("client/make-request/<shop>/", makeRequestView, name="client-make-request"),
    path("client/view-requests/", viewRequestsView, name="client-view-requests"),
    path(
        "client/edit-request/<requestone>/", editRequestView, name="client-edit-request"
    ),
    path("login/", loginView, name="login"),
    path("logout/", logoutView, name="logout"),
    path("register/", registerView, name="register"),
    path("client/home/", homeClientView, name="client-home"),
    path("artist/home/", homeArtistView, name="artist-home"),
    path("artist/add-shop/", addShopArtistView, name="artist-add-shop"),
    path("artist/view-requests/", viewRequestArtistView, name="artist-view-requests"),
    path(
        "artist/view-one-request/<requestone>/",
        viewOneRequestView,
        name="artist-view-one-request",
    ),
    path("artist/edit-shop/<shop>/", editShopArtistView, name="artist-edit-shop"),
    path("artist/view-shops/", viewShopsArtistView, name="artist-view-shops"),
    path("artist/deleted-shop/<shop>/", deleteShop, name="delete-shop"),
    path("request-deleted/<requestid>", deleteRequest, name="delete-request"),
    path("", baseHomeView, name="base-home"),
    path("admin/", admin.site.urls),
]
