from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Customer
from django.contrib.auth.models import Group

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		print("Profile created!")

# post_save.connect(create_profile, sender=User)

@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
	if not created:
		instance.profile.save()
		print("Profile updated!")

# post_save.connect(update_profile, sender=User)

def customer_profile(sender, instance, created, **kwargs):
	if created:
		group = Group.objects.get(name='Customer')
		instance.groups.add(group)
		Customer.objects.create(
			user=instance,
			name=instance.username,
			)
		print("Profile customer '" + instance.username + "' was created!")

post_save.connect(customer_profile, sender=User)