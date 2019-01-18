from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.http.response import HttpResponseRedirect
from contacts.models import Contact

# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            #check username is already exist or not for this we need default user model
            if User.objects.filter(username=username).exists():
                messages.error(request,'that username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'that email is being used')
                    return redirect('register')
                else:
                   user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
                   #login after register
                   # auth.login(request,user)
                   # messages.success(request,'you are now logged in')
                   # return redirect('index')
                   user.save()
                   messages.success(request,'you are now registered and login')
                   return redirect('login')
        else:
            messages.error(request,'password do not match')
            return redirect('register')

    else:
            return render(request,'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are now logged in')
            return  HttpResponseRedirect(reverse('dashboard'))
        else:
            messages.error(request,'Invalid credentials')
    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'YOu are now logout')
        return redirect('index')

    return redirect('index')

def dashboard(request):
    user_contact = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts' : user_contact
    }
    return render(request,'accounts/dashboard.html',context)