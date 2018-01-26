from django.shortcuts import render, redirect, reverse
from .models import *
from django.contrib.messages import error
import bcrypt
import datetime

def index(request):
    return render(request, 'belt/index.html')

def register(request):
    # check if the model.Manger captured any errors 
    errors = Users.objects.reg_validation(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    # create user object 
    Users.objects.create(
        name= request.POST['name'],
        username = request.POST['username'],
        # encrypting PW before putting into DB
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    )
    # message to show the user that registration was a success
    context = {
        'messages' : ["registered successfully"]
    }
    return render(request, "belt/index.html", context)  

def login(request):
    # try to obtain username from db. if failed render page with message
    try: 
        user = Users.objects.get(username = request.POST['r_username'])
    except:
        context = {
            'messages' : ["Username not registered"]
        }
        return render(request, "belt/index.html", context)        

    # checking if the password matches 
    if not bcrypt.checkpw(request.POST['r_password'].encode(), user.password.encode()):
        context = {
            'messages' : ["Incorrect Password"]
        }
        return render(request, "belt/index.html", context)

    # setting the user that is signed in to the user untill someone else signs in.
    request.session['user_id'] = user.id
    return redirect('/travels')

def travels(request):
    # used to display user's travels and other user's travels
    user = Users.objects.get(id = request.session['user_id'])
    user_travels = user.plans.all()
    context = {
        "user" : user,
        "user_travels" : user_travels, 
        "other_travels" : Travels.objects.all().exclude(user_travels = user)
    }
    return render(request, 'belt/travels.html', context)

def travel_add(request):
    return render(request, 'belt/travel_add.html')

def travel_add_proc(request):
    # check for errors
    errors = Users.objects.travel_validation(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/travels/add')
    # create travel with user as first user
    Travels.objects.create(
        destination=request.POST['destination'],
        description = request.POST['description'],
        date_start = request.POST['date_start'],
        date_end = request.POST['date_end']
    )
    # adding travel to current user
    user = Users.objects.get(id = request.session['user_id'])
    travel = Travels.objects.last()
    travel.user_travels.add(user)
    return redirect('/travels')

def travel_desc(request, travel_id):
    travel = Travels.objects.get(id = travel_id)
    # used for displaying who created the travel
    plan_by = travel.user_travels.first()
    context = {
        "travel" : travel,
        "plan_by" : plan_by,
        "other_users" : travel.user_travels.exclude(id = plan_by.id)
    }
    return render(request,'belt/travel_desc.html', context)

def travel_join(request, travel_id):
    user = Users.objects.get(id = request.session['user_id'])
    travel = Travels.objects.get(id = travel_id)
    travel.user_travels.add(user)
    return redirect('/travels')
    # add current user to travel that was clicked

def logout(request):
    request.session['user_id'] = []
    return redirect('/')