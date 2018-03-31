from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def current_user(request):
	return User.objects.get(id = request.session['user_id'])

def registration(request):
	return render(request, 'exam/registration.html')

def register(request):
	check = User.objects.validate(request.POST)
	if request.method != 'POST':
		return redirect('/')
	if check[0] == False:
		for error in check[1]:
			messages.add_message(request, messages.INFO, error, extra_tags="registration")
			return redirect('/')
	if check[0] == True:
		hashed_pw = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())

		user = User.objects.create(
			name = request.POST.get('name'),
			username = request.POST.get('username'),
			password = hashed_pw
		)

		request.session['user_id'] = user.id
		return redirect('/dashboard')

def login(request):
	if request.method != 'POST':
		return redirect('/')
	user = User.objects.filter(username = request.POST.get('username')).first()

	if user and bcrypt.checkpw(request.POST.get('password').encode(), user.password.encode()):
		request.session['user_id'] = user.id
		return redirect('/dashboard')
	else: 
		messages.add_message(request, messages.INFO, 'invalid credentials', extra_tags="login")
		return redirect('/')
	return redirect('/dashboard')

def logout(request):
		request.session.clear()
		return redirect('/')

def dashboard(request):
	user = current_user(request)
	trips = Trip.objects.filter(trips = user)
	# trips = Trip.objects.exclude(others_trips)
	context = {
		'user': user,
		'trip_list': Trip.objects.exclude(trips = user),
		'trips': trips
	}
	return render(request, 'exam/dashboard.html', context)

def add_plan(request):

	return render(request, 'exam/add_plan.html')




def create(request):
	check = Trip.objects.trip_validation(request.POST)
	if request.method != 'POST':
		return redirect('/dashboard')
	if check[0] == False:
		for error in check[1]:
			messages.add_message(request, messages.INFO, error, extra_tags="add_item")
			return redirect('/dashboard')
	if check[0] == True:

		trip = Trip.objects.create(
			destination = request.POST.get('destination'),
			description = request.POST.get('description'),
			created_by = current_user(request),
			departure_date = request.POST.get('departure_date'),
			return_date = request.POST.get('return_date')
			)
		return redirect('/dashboard')
	return redirect('/dashboard')

def add_trip(request, id):
    	
	user = current_user(request)
	trip = Trip.objects.get(id=id)
	trip.trips.add(user)
	trip.save()
	return redirect('/dashboard')

def remove_trip(request, id):
    	
	user = current_user(request)
	trip = Trip.objects.get(id=id)
	trip.trips.remove(user)
	return redirect('/dashboard')

def show_itineraries(request, id):

	user =  User.objects.get(id = id)
	all_trips = trip.trips.all()
	all_trips.exclude(id)
	context = {
		'user': user,
		'trips': trip.trips.all()		
	}
	return render(request, 'exam/user.html', context)


