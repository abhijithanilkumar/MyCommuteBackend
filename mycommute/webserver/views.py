from django.shortcuts import render
from models import *
import uuid
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from webserver.serializers import CommuterSerializer, CommuterDataSerializer
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

# Create your views here.

@api_view(['POST'])
def login(request):
    """API that logs in an existing user"""
    username = request.data.pop('username')
    password = request.data.pop('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        try:
            commuter = Commuter.objects.get(user=user)
        except:
            return JsonResponse({
                'detail':'Profile not found for this user'
            },
            status=404)
        serialized = CommuterSerializer(commuter)
        return Response(data=serialized.data, status=201)
    else:
        return JsonResponse({
            'detail':'User not found'
        },
        status=404)

@api_view(['POST'])
def register(request):
    """API that generates unique QR code for a commuter using the details"""
    deserializedCommuterData = CommuterDataSerializer(data=request.data)
    if not deserializedCommuterData.is_valid():
        print deserializedCommuterData.errors
        return Response(data=deserializedCommuterData.errors, status=400)
    userid = uuid.uuid4().hex[:33]
    username = request.data.pop('username')
    password = request.data.pop('password')
    email = request.data.pop('email')
    newuser = User.objects.create_user(
        username=username,
        password=password,
        email=email,
    )
    newuser.save()
    commuter, created = Commuter.objects.update_or_create(
        user=newuser,
        email=newuser.email,
        userid=userid,
        wallet=500,
        defaults=deserializedCommuterData.validated_data
    )
    serialized = CommuterSerializer(commuter)
    return Response(data=serialized.data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """API that returns profile information of a registered user"""
    try:
        commuter = Commuter.objects.get(user=request.user)
        serialized = CommuterSerializer(commuter)
        return Response(data=serialized.data)
    except:
        return JsonResponse({
            'detail':'Profile not found for this user'
        },
        status=404)

@api_view(['POST'])
def buslogin(request):
    """API that creates a route in the database"""
    username = request.data.pop('username')
    password = request.data.pop('password')
    rname = request.data.pop('rname')
    buser = authenticate(username=username, password=password)
    if buser is not None:
        bus = Bus.objects.get(user=buser)
        route, created = Route.objects.update_or_create(
            name=rname,
            bus=bus
        )
        bus_data = {
            "token": Token.objects.get(user=buser).key,
        }
        return Response(data = bus_data)
    else:
        return JsonResponse({
            'detail':'Bus not found'
        },
        status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def readqr(request):
    """API that reads the QR code and starts/stops the trip"""
    userid = request.data.pop('userid')
    reading = request.data.pop('reading')
    busid= request.user
    try:
        commuter = Commuter.objects.get(userid=userid)
    except:
        return JsonResponse({
            'detail':'User not found'
        },
        status=404)
    user = commuter.user
    if Trip.objects.filter(user=user).exists():
        trip = Trip.objects.filter(user=user).order_by('-id')[0]
        if trip.start == trip.stop:
            trip.stop = reading
            cost = 4*(trip.stop-trip.start)
            commuter.wallet = commuter.wallet - cost
            trip.save()
            commuter.save()
            response = "Trip Ended. Cost : %d" % (cost)
            return Response(data=response, status=200)
        else:
            bus = Bus.objects.get(user=busid)
            route = Route.objects.get(bus=bus)
            trip, created = Trip.objects.update_or_create(
                user=user,
                route=route,
                start=reading,
                stop=reading
            )
            response = "Hello %s %s! Welcome Aboard!" % (commuter.firstName, commuter.lastName)
            return Response(data=response, status=200)
    else:
        bus = Bus.objects.get(user=busid)
        route = Route.objects.get(bus=bus)
        trip, created = Trip.objects.update_or_create(
            user=user,
            route=route,
            start=reading,
            stop=reading
        )
        response = "Hello %s %s! Welcome Aboard!" % (commuter.firstName, commuter.lastName)
        return Response(data=response, status=200)
