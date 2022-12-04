from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from profiles.models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)
