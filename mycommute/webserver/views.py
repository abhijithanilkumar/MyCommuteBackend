from django.shortcuts import render
from models import *
import uuid
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from webserver.serializers import CommuterSerializer, CommuterDataSerializer
from django.contrib.auth.models import User

# Create your views here.

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
        return JSONResponse({
            'detail':'Profile not found for this user'
        },
        status=404)
