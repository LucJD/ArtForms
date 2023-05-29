from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# ---USER MODELS---#
class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # shops_set
    def __str__(self):
        return self.user.username


def create_artist(user):
    artist = Artist(user=user)
    artist.save()


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # request_set
    def __str__(self):
        return self.user.username


def create_client(user):
    client = Client(user=user)
    client.save()


class Shop(models.Model):
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    turnover = models.CharField(max_length=50)
    base_price = models.FloatField()
    # request_set

    def __str__(self):
        return self.title + ": " + self.artist.user.username


def create_shop(artist, title, description, turnover, base_price):
    shop = Shop(
        artist=artist,
        title=title,
        description=description,
        turnover=turnover,
        base_price=base_price,
    )
    shop.save()
    return shop


class Request(models.Model):
    ACCEPTED = [("Accepted", "Accepted"), ("Denied", "Denied"), ("Pending", "Pending")]
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contact_email = models.EmailField()
    description = models.TextField()
    accepted = models.TextField(choices=ACCEPTED, default=ACCEPTED[2])

    def __str__(self):
        return self.shop.title + ": " + self.client.user.username


def create_request(shop, client, contact_email, description):
    request = Request(
        shop=shop, client=client, contact_email=contact_email, description=description
    )
    request.accepted = "Pending"
    request.save()
    return request


# ----------FUNCTIONS------------#

# -----artist-----#
def find_artist_by_user(user):
    try:
        return Artist.objects.get(user=user)
    except:
        return None


# ------client -----#
def find_client_by_user(user):
    try:
        return Client.objects.get(user=user)
    except:
        return None


# -----shops-----


def find_shops_by_artist(artist):
    return list(artist.shop_set.all())


def update_shop(shop, title, description, turnover, base_price):
    shop.title = title
    shop.description = description
    shop.turnover = turnover
    shop.base_price = base_price
    shop.save()
    return shop


def delete_shop(shop):
    shop.delete()


def find_requests_by_shop(shop):
    return list(shop.request_set.all())


# -----requests-----


def find_requests_by_artist(artist):
    requests = []
    shops = find_shops_by_artist(artist)

    for shop in shops:
        if find_requests_by_shop(shop) != []:
            requests.extend(find_requests_by_shop(shop))
    return requests


def find_requests_by_client(client):
    return list(client.request_set.all())


def update_request_status(request, status):
    request.accepted = status
    request.save()


def update_request_form(request, contact_email, description):
    request.contact_email = contact_email
    request.description = description
    request.save()


def delete_request(request):
    request.delete()
