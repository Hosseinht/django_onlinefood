from django.contrib import messages
from django.urls import reverse
from django.views import generic

from .forms import UserRegistrationForm
from .models import User


class RegisterUserView(generic.CreateView):
    form_class = UserRegistrationForm
    template_name = "accounts/register_user.html"

    def get_success_url(self):
        return reverse("users:register_user")

    def form_valid(self, form):
        password = form.cleaned_data["password"]

        user = form.save(commit=False)
        user.set_password(password)
        user.role = User.CUSTOMER
        user.save()
        messages.success(self.request, "Your account has been created successfully")
        return super(RegisterUserView, self).form_valid(form)
