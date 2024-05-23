from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User,Trip
import bcrypt

def index(request):
    return render(request,'index.html')

def create(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value,extra_tags="fail")
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print (pw_hash)
        if request.method == "POST":
            user=User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=pw_hash
                )
            request.session['userid'] = user.id
    return redirect('/dashboard')

def login(request):
    email = User.objects.filter(email=request.POST['email']) 
    if email: 
        logged_email = email[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_email.password.encode()):
            request.session['userid'] = logged_email.id
            return redirect('/dashboard')
    messages.error(request, "The password or email you entered is incorrect",extra_tags="login")
    return redirect("/")

def dash(request):
    data={
        "current_user":User.objects.get(id=request.session['userid']),
        "trips":Trip.objects.all(),
    }
    return render (request, 'dashboard.html',data)

def reset(request):
    request.session.clear()
    return redirect('/')

def add_trip(request):
    data={
        "current_user":User.objects.get(id=request.session['userid']),
        "trips":Trip.objects.all(),
    }
    return render(request,'trip.html',data)

def trip(request):
    errors = Trip.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/new')
    else:
        if request.method == "POST":
            trip_x= Trip.objects.create(
                        country=request.POST['dest'],
                        startdate=request.POST['date'],
                        enddate=request.POST['dateend'],
                        organizer=User.objects.get(id=request.session['userid']),
                        itinerary=request.POST['itin'],
            )
    return redirect('/dashboard')

def edit(request,id):
    data={
        "trip_x":Trip.objects.get(id=id),
        "current_user":User.objects.get(id=request.session['userid']),
    }
    return render(request,"edit.html",data)

def process_edit(request,id):
    errors = Trip.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/trips/edit/{id}')
    else:
        trip_x=Trip.objects.get(id=id)
        trip_x.country=request.POST['dest']
        trip_x.startdate=request.POST['date']
        trip_x.enddate=request.POST['dateend']
        trip_x.itinerary=request.POST['itin']
        trip_x.save()
    return redirect(f"/trips/{id}")

def show(request,id):
    data={
        "trip_x":Trip.objects.get(id=id),
        "current_user":User.objects.get(id=request.session['userid']),
    }
    return render (request,"details.html",data)

def trips(request):
    data={
        "current_user":User.objects.get(id=request.session['userid']),
        "trips":Trip.objects.all(),
    }
    return render(request, "mytrips.html",data)

def cancel(request,x,y):
    user_y=User.objects.get(id=x)
    trip_y=Trip.objects.get(id=y)
    user_y.trip.remove(trip_y)
    return redirect("/trips/mytrips")

def join(request,x,y):
    user_y=User.objects.get(id=x)
    trip_y=Trip.objects.get(id=y)
    user_y.trip.add(trip_y)
    return redirect("/trips/mytrips")

def delete(request,id):
    trip_x=Trip.objects.get(id=id)
    trip_x.delete()
    return redirect('/dashboard')