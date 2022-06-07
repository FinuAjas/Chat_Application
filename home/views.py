from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from . models import *
from django.contrib.auth import authenticate, login ,logout
from . forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from . models import *



def home(request):
    if request.user.is_authenticated:
        return render(request,'home.html')
    else:
        return redirect('login')    


def room(request, room):
    if request.user.is_authenticated:
        username = request.GET.get('username')
        room_details = Room.objects.get(name=room)
        return render(request, 'room.html', {
            'username': username,
            'room': room,
            'room_details': room_details
        })
    else:
        return redirect('login')        


def checkview(request):
    if request.user.is_authenticated:
        room = request.POST['room_name']
        username = request.POST['username']

        if Room.objects.filter(name=room).exists():
            return redirect('/'+room+'/?username='+username)
        else:
            new_room = Room.objects.create(name=room)
            new_room.save()
            return redirect('/'+room+'/?username='+username)
    else:
        return redirect('login')    

def send(request):
    if request.user.is_authenticated:
        message = request.POST['message']
        username = request.POST['username']
        room_id = request.POST['room_id']

        new_message = Message.objects.create(value=message, user=username, room=room_id)
        new_message.save()
        return HttpResponse('Message sent successfully')
    else:
        return redirect('login')    

def getMessages(request, room):
    if request.user.is_authenticated:
        room_details = Room.objects.get(name=room)
        messages = Message.objects.filter(room=room_details.id)
        return JsonResponse({"messages":list(messages.values())})        
    else:
        return redirect('login')    

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:    
        page = 'login'
        context = {
            'page': page,
        }
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                return render(request, 'login3.html',context)
        else:           
            return render(request, 'login3.html',context)

def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:  
        page = 'register'
        form = CustomUserCreationForm
        context = {
            'page':page,
            'form':form,
        }
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid:
                form.save()
                return redirect('login')
            else:
                return render(request, 'login3.html',context)
        else:
            return render(request, 'login3.html',context)        


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')   
