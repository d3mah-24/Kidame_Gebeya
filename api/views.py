from django.forms.models import model_to_dict
from django.core import serializers
from rest_framework import filters
import json
from django.db.models import Max
import random
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from api.seri import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from .models import *
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from twilio.rest import Client

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


User = get_user_model()
# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['first_name'] = user.first_name
        token['email'] = user.email
        token["id"] = user.id

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@csrf_exempt
def updater(req):
    body_unicode = req.body.decode('utf-8')
    data = json.loads(body_unicode)
    # print(data)

    d = User.objects.get(id=data['id'])
    d.name = data["name"]

    d.password = make_password(data['pass'])
    d.save()
    # print(data['pass'], d.password)
    return JsonResponse(data)


@csrf_exempt
def cart_count(req):
    # if req.method == 'GET':
    body_unicode = req.body.decode('utf-8')
    data = json.loads(body_unicode)
    a = Cart.objects.filter(user=data["id"])
    # print(a, 111)
    return JsonResponse(a.count(), safe=False)


# def get_random(mod):
#     max_id = mod.objects.all().aggregate(max_id=Max("id"))['max_id']
#     while True:
#         pk = random.randint(1, max_id)
#         category = mod.objects.filter(pk=pk)[:4]
#         if category:
#             return category


def recent_products(req):
    if req.method == "GET":

        d = {"fashion": Products.objects.filter(category=1).values().order_by("-id").first(),
             "cosmo": Products.objects.filter(category=2).values().order_by("-id").first(),
             "shoe": Products.objects.filter(category=3).values().order_by("-id").first(),
             "electro": Products.objects.filter(category=4).values().order_by("-id").first()}
        # print(d)
        return JsonResponse(d)


def products_length(req):
    d = {"fashion":  Products.objects.filter(category=1).count(),
         "cosmo":  Products.objects.filter(category=2).count(),
         "shoe":  Products.objects.filter(category=3).count(),
         "electro":  Products.objects.filter(category=4).count(),

         }
    # print(d)

    return JsonResponse(d)


def products_search(req, q):
    d = {"results": list(Products.objects.filter(name__contains=q).values())

         }
    # print(d)

    return JsonResponse(d)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class productss(generics.ListAPIView):
    serializer_class = Product_ser

    def get_queryset(self):
        k = {"fashion": 1,
             "cosmo": 2,
             "shoe": 3,
             "electro": 4,
             }
        queryset = Products.objects.all()
        username = self.request.query_params.get('type')
        # print(type(username), username)
        if username == "all":
            queryset = queryset.order_by("-id").values()
        elif username is not None:
            queryset = queryset.filter(
                category=k[username]).order_by("-id").values()
        # print(queryset,)
        # print(queryset)

        return queryset

    def get_object(self):
        queryset = self.get_queryset()

        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        print(obj, 990)
        return obj
# def doss(req, username):
#     k = {"fashion": 1,
#          "cosmo": 2,
#          "shoe": 3,
#          "electro": 4,


#          }
#     queryset = Products.objects.all()

#     # print(type(username), username)
#     if username == "all":
#         queryset = queryset.order_by("-id").values()
#     elif username is not None:
#         queryset = queryset.filter(
#             category=k[username]).order_by("-id")
#     print(queryset, 9990)
#     # return queryset
#     return JsonResponse(list(queryset.values()), safe=False)

def detail(req, idd):
    a = list(Products.objects.filter(id=idd).values())[0]

    return JsonResponse(a, safe=False)


class Posts(APIView):

    def post(self, request, format=None):

        try:
            description = request.data["description"]
            name = request.data["name"]
            price = request.data["price"]
            category = request.data["category"]
            img = request.data["img"]
            print(img, category, price)
            ex = img.name.split(".")[-1]
            f_name = "".join(name.split())
            img.name = f"{price}{f_name}.{ex}"
            print(img.name, ex)
            Products.objects.create(
                category=Category.objects.get(id=int(category)), name=name,
                price=float(price), description=description, image=img, img_name=img.name
            )

        except Cart.DoesNotExist:
            raise Http404

        return Response(status=status.HTTP_204_NO_CONTENT)


class order(APIView):

    def post(self, request, format=None):

        try:
            address = request.data["address"]
            name = request.data["name"]
            phone_num = request.data["phone_num"]
            id = request.data["id"]
            products_ = Cart.objects.filter(user=MyUser.objects.get(
                id=id))

            cv = [Products.objects.get(
                id=h["item"]).name for h in products_.values("item")]
            pp = '\n'.join(cv)
            cap = f"""\n 
             
            Name :- {name},\n
            Phone Number :- {phone_num},\n
            Address :- {address},\n
            Products :- {pp},\n
        
            """
            # message = client.messages.create(
            #     body=cap,
            #     from_='+13613209516',
            #     to='+251945320109'
            # )

            # print(88899, name)
            data = {"txt": cap}
            products_.delete()
            return JsonResponse(data)

        except Cart.DoesNotExist:
            raise Http404

        return Response(status=status.HTTP_204_NO_CONTENT)


class Carts(APIView):

    def get_object(self, pk):
        try:
            return Cart.objects.filter(user=pk)
        except Cart.DoesNotExist:
            raise Http404

    def post(self, request, format=None):

        try:
            print(Products.objects.get(id=request.data["item"]).id, [
                  a["item"] for a in list(Cart.objects.values("item"))])
            if Products.objects.get(id=request.data["item"]).id not in [a["item"] for a in list(Cart.objects.values("item"))]:
                Cart.objects.create(user=MyUser.objects.get(
                    id=request.data["users"]), item=Products.objects.get(id=request.data["item"]))

        except Cart.DoesNotExist:
            raise Http404

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = Cart_ser(snippet,  many=True)
        return Response(serializer.data)

    def delete(self, request, pk, item, format=None):
        try:
            snippet = Cart.objects.get(user=pk, item=item)
        except Cart.DoesNotExist:
            raise Http404
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
