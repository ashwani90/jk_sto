from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import Activation
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, FormView
from .forms import (
    SignUpForm, ProfileForm, LoginForm
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
# from .models import Activation

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'account/register.html', {'form': form})

def loginMethod(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            # Todo:: Please do this with the username instead of mail
            user = authenticate(username="ashwani", password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

# class SignUpView(FormView):
#     template_name = 'account/register.html'
#     form_class = SignUpForm

#     def form_valid(self, form):
#         print("Coming here")
#         request = self.request
#         user = form.save(commit=False)

        
#         user.username = form.cleaned_data['username']

#         # Create a user record
#         user.save()

#         if settings.ENABLE_USER_ACTIVATION:
#             code = get_random_string(20)

#             act = Activation()
#             act.code = code
#             act.user = user
#             act.save()

#             # send_activation_email(request, user.email, code)

#             # messages.success(
#             #     request, _('You are signed up. To activate the account, follow the link sent to the mail.'))
#         else:
#             raw_password = form.cleaned_data['password1']

#             # user = authenticate(username=user.username, password=raw_password)
#             # login(request, user)

#             # messages.success(request, _('You are successfully signed up!'))

#         return redirect('signup')

# class SignUpView(CreateView):
#     print("Coming up here")
#     form_class = SignUpForm
#     success_url = reverse_lazy('login')
#     template_name = 'account/register.html'

# Edit Profile View
class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('home')
    template_name = 'account/profile.html'