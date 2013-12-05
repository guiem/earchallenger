from django.db import models
from earchallenger_web.models.usermodel import UserProfile
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class StatsLine(models.Model):
    profile = models.ForeignKey(UserProfile)
    datestamp = models.DateTimeField(_("Timestamp"))
    correct = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(1)])
    num_trials = models.IntegerField(_("Num.Trials"))
    num_hints = models.IntegerField(_("Num.Hints"))
    num_notes = models.IntegerField(_("Num.Notes"))
    instrument = models.CharField(_("Instrument"),max_length=255)
    sequence = models.CharField(_("Sequence"),max_length=1000)
    user_rating = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(10)])

    class Meta:
        abstract = False
        app_label = 'earchallenger_web'

#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        profile, created = UserProfile.objects.get_or_create(user=instance)

#post_save.connect(create_user_profile, sender=User)