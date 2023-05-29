from app.models import *
from app.forms import *
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from app.decorators import *

# Create your views here.

# ==========HOME PAGE, REGISTER AND LOGIN ===========#

# ---BASE HOME VIEW---#
# redirect according to user
def baseHomeView(request):
    if request.user.is_authenticated:
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == "client":
                return redirect("client-home")
            if group == "artist":
                return redirect("artist-home")
        else:
            return redirect("logout")
    else:
        return redirect("register")


# ----HOME PAGE CLIENT----#
# can view client's requests
# can view artist shops
@login_required(login_url="login")
@allowed_users(allowed_roles="client")
def homeClientView(request):
    context = {}
    return render(request, "homeclient.html", context)


# ---HOME PAGE ARTIST---#
# can view requests
# can view artist's shops
@login_required(login_url="login")
@allowed_users(allowed_roles="artist")
def homeArtistView(request):
    context = {}
    return render(request, "homeartist.html", context)


# ---REGISTER---#
@unauthenticated_user
def registerView(request):

    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            groupselect = request.POST["group"]
            group = Group.objects.get(name=groupselect)
            if groupselect == "artist":
                create_artist(user)
            elif groupselect == "client":
                create_client(user)
            user.groups.add(group)
            username = form.cleaned_data.get("username")
            messages.success(request, "Account created for " + username)
            return redirect("login")
    context = {"form": form}
    return render(request, "register.html", context)


# ---LOGIN---#
@unauthenticated_user
def loginView(request):
    form = LoginUserForm()

    if request.method == "POST":
        form = LoginUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("base-home")
            else:
                messages.info(request, "Username or Password is incorrect.")
    context = {"form": form}
    return render(request, "login.html", context)

@login_required(login_url='login')
def logoutView(request):
    logout(request)
    return redirect("login")


# ==============================================================================#

# CLIENT PAGES#

# VIEW REQUESTS - client-view-requests
# allows client to view current requests
@login_required(login_url="login")
@allowed_users(allowed_roles="client")
def viewRequestsView(request):
    current_client = find_client_by_user(request.user)
    requests = find_requests_by_client(current_client)
    context = {"requests": requests}
    return render(request, "client/view-requests.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles="client")
def editRequestView(request, requestone):
    current_request = Request.objects.get(id=requestone)
    form = CreateRequestForm()
    context = {"current_request": current_request, "form": form}
    if request.method == "POST":
        form = CreateRequestForm(request.POST)
        if form.is_valid():
            contact_email = form.cleaned_data["contact_email"]
            description = form.cleaned_data["description"]
            update_request_form(current_request, contact_email, description)
            message = "Successfully updated request form."
            context["message"] = message

    return render(request, "client/edit-request.html", context)


# ---MAKE REQUEST CLIENT---#
# client chooses an artist to request a commission for
# fill out their forms
@login_required(login_url="login")
@allowed_users(allowed_roles="client")
def makeRequestView(request, shop):
    shop = Shop.objects.get(id=shop)
    form = CreateRequestForm()
    context = {"shop": shop, "form": form}

    client = find_client_by_user(request.user)
    if request.method == "POST":
        form = CreateRequestForm(request.POST)
        if form.is_valid():
            contact_email = form.cleaned_data["contact_email"]
            description = form.cleaned_data["description"]
            create_request(shop, client, contact_email, description)
            message = "Request Successfully Submitted."
            context["message"] = message
    return render(request, "client/create-request.html", context)


# ---VIEW ARTISTS CLIENT ---#
# client views artists and their shops
# selecting a shop goes to make request view
@login_required(login_url='login')
@allowed_users(allowed_roles="client")
def viewArtistsView(request):
    artists = Artist.objects.all()
    shops = Shop.objects.all()
    context = {"artists": artists, "shops": shops}
    return render(request, "client/view-artists.html", context)


# ==========================================================


# ===========ARTIST PAGE VIEWS===============

# ---VIEW REQUEST ARTIST---#
# artists can view requests that clients have filled out
@login_required(login_url="login")
@allowed_users(allowed_roles="artist")
def viewRequestArtistView(request):
    artist = find_artist_by_user(request.user)
    requests = find_requests_by_artist(artist)
    context = {"requests": requests}
    return render(request, "artist/view-requests.html", context)


# ---- VIEW SPECIFIC REQUEST ARTIST ----
# view one specific request, then edit if accepted or denied
@login_required(login_url="login")
@allowed_users(allowed_roles="artist")
def viewOneRequestView(request, requestone):
    current_request = Request.objects.get(id=requestone)
    context = {"current_request": current_request}

    if request.method == "POST":
        status = request.POST["accepted"]
        update_request_status(current_request, status)
        message = "Request Status Updated"
        context["message"] = message
    return render(request, "artist/view-one-request.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles="artist")
def viewShopsArtistView(request):
    artist = find_artist_by_user(request.user)
    shops = find_shops_by_artist(artist)
    context = {"shops": shops}
    return render(request, "artist/view-shops.html", context)


# ---CREATE SHOP ARTIST---#
# artists can create 'shops'
# this will be what clients look at
# artists will have
@login_required(login_url="login")
@allowed_users(allowed_roles="artist")
def addShopArtistView(request):
    current_user = User.objects.get(id=request.user.id)
    current_artist = find_artist_by_user(current_user)
    form = CreateShopForm()
    if request.method == "POST":
        form = CreateShopForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            turnover = form.cleaned_data["turnover"]
            base_price = form.cleaned_data["base_price"]
            create_shop(current_artist, title, description, turnover, base_price)
            messages.success(request, "Shop Successfully Created!")
            return redirect("artist-add-shop")

    context = {"form": form}
    return render(request, "artist/create-shop.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles="artist")
def editShopArtistView(request, shop):
    form = CreateShopForm()
    shop = Shop.objects.get(id=shop)
    context = {"form": form, "shop": shop}

    if request.method == "POST":
        form = CreateShopForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            turnover = form.cleaned_data["turnover"]
            base_price = form.cleaned_data["base_price"]
            update_shop(shop, title, description, turnover, base_price)
            messages.success(request, "Shop Successfully Updated")
            return redirect("artist-view-shops")

    return render(request, "artist/edit-shop.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles="artist")
def deleteShop(request, shop):
    shop = Shop.objects.get(id=shop)
    delete_shop(shop)
    context = {}
    return render(request, "artist/shop-deleted.html", context)

def deleteRequest(request, requestid):
    current_request = Request.objects.get(id=requestid)
    delete_request(current_request)
    context = {}
    return render(request, 'request-deleted.html', context)