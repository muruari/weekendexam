from __future__ import unicode_literals
from django.db import models
import re


class UserManager(models.Manager):
	def validate(self, post_data):
		is_valid = True
		errors = []


		if len(post_data.get('name')) and len(post_data.get('username')) < 3:
			is_valid = False
			errors.append('Usernames must have at least 3 characters. Please try again.')

		if not re.search(r'^[a-z" "A-Z]+$', post_data.get('name')):
			is_valid = False
			errors.append('Name must be alphabetical characters only. Please try again.')

		if len(post_data.get('password')) < 8:
			is_valid = False
			errors.append('Passwords must have at least 8 characters. Please try again.')
		if post_data.get('password_confirmation') != post_data.get('password'):
			is_valid = False
			errors.append('Passwords do not match. Please try again.')

		return (is_valid, errors)


class TripManager(models.Manager):
	def trip_validation(self, post_data):

		is_valid = True
		errors = []

		if len(post_data.get('description')) < 5:
			is_valid = False
			errors.append('Minimum description length is 5 characters.')
		return (is_valid, errors)






class User(models.Model):
	name = models.CharField(max_length = 255)
	username = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
    # trips = models.ManyToManyField(Trip, related_name="joined_trips", default=None)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

	def __str__(self):
		return "name:{}, username:{}, password:{}, created_at:{}, updated_at:{}".format(self.name, self.username, self.password, self.created_at, self.updated_at)



class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    created_by = models.ForeignKey(User, related_name = 'trips')
    trips = models.ManyToManyField(User, related_name="joined", default=None)    
    departure_date = models.CharField(max_length=10)
    return_date = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager()
    
    def __str__(self):
        return 'destination:{}, created_by:{}'.format(self.destination, self.user)

