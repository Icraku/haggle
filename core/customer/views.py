from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from core.customer import forms

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


@login_required()
def home(request):
    return redirect(reverse('customer:profile'))

@login_required(login_url="/sign-in/?next=/customer/")
def profile_page(request):
    user_form = forms.BasicUserForm(instance=request.user)
    password_form = PasswordChangeForm(request.user) # change password form

    if request.method == "POST":

        if request.POST.get('action') == 'update_profile':
            user_form = forms.BasicUserForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()

                # submit form
                messages.success(request, "You profile has been updated!")
                return redirect(reverse('customer:profile'))
        
        elif request.POST.get('action') == 'update_password':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important to keep the user logged in

                messages.success(request, "Your password has been updated!")
                return redirect(reverse('customer:profile'))
        

    return render(request, 'customer/profile.html', {
        'user_form': user_form,
        'password_form': password_form
    })
