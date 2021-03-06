from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    last_sync = models.DateTimeField()

    class Meta:
        abstract = False
        app_label = 'earchallenger_web'

#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        profile, created = UserProfile.objects.get_or_create(user=instance)

#post_save.connect(create_user_profile, sender=User)