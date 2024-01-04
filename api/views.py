from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import UserSerializers,TodoSerilaizer
from rest_framework.viewsets import ViewSet
from rest_framework import permissions,authentication
from todoapp.models import Todos
from rest_framework import serializers

# Create your views here.

class RegistrationView(APIView):
    #POST METHOD REG ONLY 
    def post(self,request,*args,**kwargs):
        serializer=UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
           
            return Response(data=serializer.data)
        else:
             return Response(data=serializer.errors)
        
#for all cruds   -- for performing all tasks 
            
class TodosView(ViewSet):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self,request,*args,**kwargs):
        serializer=TodoSerilaizer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    def list(self,request,*args,**kwargs):
        #list todos of logged-in user
        qs=Todos.objects.filter(user=request.user)
        serializer=TodoSerilaizer(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todos.objects.get(id=id)
        if todo_object.user != request.user: #if condition check loged-in user same as todo user who created the todo task
            raise serializers.ValidationError("permission denied for this user")
        else:
            todo_object.delete()
            return Response(data={"message":"selected data deleted "})
        
    
            




        
    # getb a todo detail


