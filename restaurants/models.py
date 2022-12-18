from django.conf import settings
from django.contrib import admin
from django.db import models

# Create your models here.
from profiles.models import Profile
from users.utils import send_notification

User = settings.AUTH_USER_MODEL


def get_restaurant_license_path(restaurant, filename):
    return "restaurants/license/%s/%s" % (str(restaurant.name), filename)


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    license = models.ImageField(upload_to=get_restaurant_license_path)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @admin.display(ordering="user__first_name")
    def user_name(self):
        return self.user.get_full_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # check if the restaurant is created
            restaurant = Restaurant.objects.get(pk=self.pk)
            if restaurant.is_approved != self.is_approved:
                mail_template = "users/emails/restaurant_approval.html"
                context = {"users": self.user, "is_approved": self.is_approved}
                if self.is_approved:
                    mail_subject = "Congratulation! Your restaurant has been approved."
                    send_notification(mail_subject, mail_template, context)
                else:
                    mail_subject = (
                        "We are sorry! You are not eligible for publishing your food menu on our "
                        "marketplace. "
                    )
                    send_notification(mail_subject, mail_template, context)
        return super(Restaurant, self).save(*args, **kwargs)
