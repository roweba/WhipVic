from django.db import models

from .querysets import *

from django.db import connection
#import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import UserManager
from .models import *

class CustomerManager(models.Manager):
	def create_customer(self, username, first_name, last_name, email, password):
		return self.create(username=username, first_name=first_name, last_name=last_name, email=email, password=password)


class DepotManager(models.Manager):
	def create_depot(self, address):
		return self.create(address=address)


class VehicleManager(models.Manager):
	def create_vehicle(self, depot, available, v_type, license):
		return self.create(depot=depot, available=available, v_type=v_type, license=license)

	def get_queryset(self):
		return VehicleQuerySet(self.model, using=self._db)

	def vehicles(self, depot=None, v_type=None):
		if not depot:
			return self.get_queryset().vehicles()
		elif not v_type:
			return self.get_queryset().vehicles(depot)
		else:
			return self.get_queryset().vehicles(depot, v_type)


class BookingManager(models.Manager):
	def create_booking(self, customer, vehicle, depot, booking_time):
		return self.create(customer=customer, vehicle=vehicle, depot=depot, booking_time=booking_time)

	def get_queryset(self):
		return BookingQuerySet(self.model, using=self._db)

	def bookings(self, customer=None, vehicle=None, depot=None):
		if customer:
			return self.get_queryset().bookings(customer=customer)
		if vehicle:
			return self.get_queryset().bookings(vehicle=vehicle)
		if depot:
			return self.get_queryset().bookings(depot=depot)
		return self.get_queryset().bookings()

class ProfileManager(models.Manager):
	@receiver(post_save, sender=User)
	def create_profile(sender, instance, created, *args, **kwargs):
		# ignore if this is an existing User
		if not created:
			return
	Profile.objects.create(user=instance)
	post_save.connect(create_profile, sender=User)
	
	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()
