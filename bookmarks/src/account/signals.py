from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from actions.utils import create_action
from .models import Profile


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        create_action(instance, 'has created an account')
    instance.profile.save()
