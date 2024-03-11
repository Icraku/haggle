import stripe
import firebase_admin
from firebase_admin import credentials


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from core.customer import forms

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.conf import settings


# Check if the default app has been initialized
if not firebase_admin._apps:
    # Initialize the Firebase app only if it hasn't been initialized before
    cred = credentials.Certificate(settings.FIREBASE_ADMIN_CREDENTIAL)
    firebase_admin.initialize_app(cred)

stripe.api_key = settings.STRIPE_API_SECRET_KEY

# Create your views here.
# Home page
@login_required(login_url="/sign-in/?next=/customer/")
def home(request):
    return redirect(reverse('customer:profile'))

# Profile page
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

        elif request.POST.get('action') == 'update_phone':
            # Get Fireabase user data from token
            firebase_user = firebase_admin.auth.verify_id_token(request.POST.get('id_token'))

            """user = firebase_admin.auth.get_user_by_phone_number(user.phone_number)
            uid = user.uid

            user = auth.get_user_by_phone_number(user.phone)
            print('Successfully fetched user data: {0}'.format(user.uid))"""
            ## fix this part!!!!!!!!!

            # Update phone number
            request.user.customer.phone_number = firebase_user.phone_number
            request.user.customer.save()
            return redirect(reverse('customer:profile'))
        

    return render(request, 'customer/profile.html', {
        'user_form': user_form,
        'password_form': password_form
    })


# Payment method page
@login_required(login_url="/sign-in/?next=/customer/")
def payment_method_page(request):
    current_customer = request.user.customer

    # Remove existing payment method
    if request.method == "POST":
        stripe.PaymentMethod.detach(
            current_customer.stripe_payment_method_id
        )
        current_customer.stripe_payment_method_id = ""
        current_customer.save()
        return redirect(reverse('customer:payment_method'))

    # Get stripe customer data
    if not current_customer.stripe_customer_id:
        customer = stripe.Customer.create()
        current_customer.stripe_customer_id = customer['id']
        current_customer.save()

    # Get stripe payment method
    stripe_payment_method = stripe.PaymentMethod.list(
        customer =  current_customer.stripe_customer_id,
        type="card"
    )

    print(stripe_payment_method)

    if stripe_payment_method and len(stripe_payment_method.data) > 0:
        payment_method = stripe_payment_method.data[0]
        current_customer.stripe_payment_method_id = payment_method.id
        current_customer.save()
    else:
        current_customer.stripe_payment_method_id = ""
        current_customer.save()

    # If customer doesn't have a payment method, create a new one
    if not current_customer.stripe_payment_method_id:
        # Create a new setup intent and pass the client secret to the template
        intent = stripe.SetupIntent.create(
            customer=current_customer.stripe_customer_id
        )

        return render(request, 'customer/payment_method.html', {
            "client_secret": intent.client_secret,
            "STRIPE_API_PUBLIC_KEY": settings.STRIPE_API_PUBLIC_KEY,
        })
    else:
        return render(request, 'customer/payment_method.html')

# Haggle page
@login_required(login_url="/sign-in/?next=/customer/")
def haggle_page(request):
    # Check if the customer has a payment method first
    if not request.user.customer.stripe_payment_method_id:
        return redirect(reverse('customer:payment_method'))
    
    return render(request, 'customer/haggle.html')    