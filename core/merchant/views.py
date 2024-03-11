from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import NamePriceForm, TimeDateForm, MarginsForm


@login_required(login_url='/sign-in/?next=/merchant/')
def home(request):
    return redirect(reverse('merchant:schedule_haggle'))

@login_required(login_url='/sign-in/?next=/merchant/')
def schedule_haggle_page(request):

    step1_form = NamePriceForm()
    step2_form = TimeDateForm()
    step3_form = MarginsForm()

    current_step = 1  # Default to step 1

    if request.method == 'POST':
        current_step = int(request.POST.get('step', 1))
        if current_step == 1:
            step1_form = NamePriceForm(request.POST)
            if step1_form.is_valid():
                product = step1_form.save(commit=False)
                product.merchant = request.user
                product.save()
                return redirect(reverse('merchant:schedule_haggle'))
        elif current_step == 2:
            step2_form = TimeDateForm(request.POST)
            if step2_form.is_valid():
                product = step2_form.save(commit=False)
                product.merchant = request.user
                product.save()
                return redirect(reverse('merchant:schedule_haggle'))
        elif current_step == 3:
            step3_form = MarginsForm(request.POST)
            if step3_form.is_valid():
                product = step3_form.save(commit=False)
                product.merchant = request.user
                product.save()
                return redirect(reverse('merchant:schedule_haggle'))

    return render(request, 'merchant/schedule_haggle.html', {
        'current_step': current_step,
        'step1_form': step1_form,
        'step2_form': step2_form,
        'step3_form': step3_form
    })

