from django.shortcuts import render,redirect

from django.views.generic import View

from todoapp.forms import UserForm,LoginForm,ToDoForm

from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth import login,logout,authenticate

from todoapp.models import Todos

from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

def ownerpermission_required(fn):
    def wrapper(request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todos.objects.get(id=id)
        if todo_object.user != request.user:
            logout(request)
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


decs=[signin_required,ownerpermission_required] #when 2 decorators are there create a var like this decs


#registration view
class RegistartionView(View):
    def get(self,request,*args,**kwargs):
        form=UserForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=UserForm(request.POST)
        if form.is_valid():

            form.save()
            print("account created..........")
            return redirect('register')
        else:
            messages.error("error in registration")
            return render(request,"register.html",{"form":form})
        

#login
class LogInView(View):
    def get(self,request,*args,**Kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
     
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(uname,pwd,"-------------")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                print("--------- valid credentials-----")
                login(request,user_object)
                return redirect("index")
            
        print("invalid login...........")
        return render(request,"login.html",{"form":form})
    


#todo view--login to get todolistview
@method_decorator(signin_required,name="dispatch")
class ToDoView(View):
    def get(self,request,*args,**kwargs):
        #to list todos in the same index disply side.1st import todos model
        qs=Todos.objects.filter(user=request.user)
        form=ToDoForm()
        pending_count=Todos.objects.filter(status="todo",user=request.user).count()
        progress_count=Todos.objects.filter(status="inprogress",user=request.user).count()
        finished_count=Todos.objects.filter(status="completed",user=request.user).count()
        return render(request,"index.html",{
                                            "form":form,
                                            "data":qs,
                                            "pending":pending_count,
                                            "progress":progress_count,
                                            "completed":finished_count
                                            })
    
    def post(self,request,*args,**kwargs):
        form=ToDoForm(request.POST)
       
        if form.is_valid():
           
            form.instance.user=request.user
            form.save()
            return redirect("index")
        else:

            return render(request,"index.html",{"form":form})

#update a particular id status=? either inpprog or complted
# http://127.0.0.1:8000/todos/id/update

@method_decorator(decs,name="dispatch")
class TodoUpdateView(View):
    def get(self,request,*args,**kwargs):
        #to get the id ,from url to which needs to update
        id=kwargs.get("pk")
        #status is extracted from request.GET
        if "status" in request.GET:
            value=request.GET.get("status")
            if value == "inprogress":
                Todos.objects.filter(id=id).update(status="inprogress")
            elif value == "completed":
                Todos.objects.filter(id=id).update(status="completed")
        return redirect("index")
    

#to delete an item using id
# http://127.0.0.1:8000/todos/id/delete

@method_decorator(decs,name="dispatch")
class ToDoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todos.objects.filter(id=id).delete()
        return redirect("index")
    

#signout
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")





        
