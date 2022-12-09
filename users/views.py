from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserRegistrationForm
from .models import User


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # assign the role(vendor or customer)
            # commit=False: means this form is not saved but ready to be saved. when we want to add some
            # other fields to this particular user we can do it here.
            # user = form.save(commit=False)
            # user.role = User.CUSTOMER
            # user.save()
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            user.role = user.CUSTOMER
            user.save()
            messages.success(request, "Your account has been created successfully")
            return redirect('users:register_user')
    else:
        form = UserRegistrationForm()

    context = {"form": form}
    return render(request, "accounts/register_user.html", context)
