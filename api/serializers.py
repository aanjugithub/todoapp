from rest_framework import serializers
from django.contrib.auth.models import User
from todoapp.models import Todos

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","email","password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data) # ** are provided for unpacking data

class TodoSerilaizer(serializers.ModelSerializer):
    user=serializers.StringRelatedField() #this code is to extract the username from user id while creating the todo task
    class Meta:
        model=Todos
        fields="__all__"
        read_only_fields=["id","user","status"]