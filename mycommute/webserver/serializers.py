from webserver.models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class CommuterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commuter
        exclude = ('user',)
        depth = 1

class CommuterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commuter
        exclude = ('user', 'userid', 'wallet',)
        depth = 1

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
