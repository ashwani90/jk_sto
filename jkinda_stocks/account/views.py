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
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Role, Profile, Organization
from django.contrib.auth import logout
import requests
import json

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            organization = Organization.objects.get(id=1)
            role = Role.objects.get(id=3)
            Profile.objects.create(user=user,organization=organization, role=role)
            # Create the user in chat model
            # call the external api here
            post_data = {'username': username}
            response = requests.post('http://localhost:8000/api/v1/create_user', data=post_data)
            if response:
                response = json.loads(response.content)
                token = response.get('token')
                user.token = token
                user.save()

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

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required
def get_users(request):
    
    users = User.objects.filter(is_active=True).select_related("profile", "profile__role", "profile__organization")
    roles = Role.objects.all()
    all_users = []
    for user in users:
        all_users.append(
            {
                "name": user.first_name+" "+user.last_name,
                "email": user.email,
                "id": user.id,
                "enabled": user.is_active,
                "role": user.profile.role.name,
                "organization_id": user.profile.organization.id
            }
        )
    data = { "users": all_users, "roles": roles }
    return render(request, 'pages/users.html', data)

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

@login_required
def enable_user(request):
    user_to_enable = request.GET.getlist("user_id")[0]
    current_user = request.user.id 
    # TODO:: check current user to be same organization as user and also role as admin
    user = User.objects.filter(id=user_to_enable).update(is_active=True)
    if user:
        return JsonResponse({"success": True, "message": "User Updated"})
    else:
        return JsonResponse({"success": False, "message": "Unable to update User"})
    
@login_required
def delete_user(request):
    user_to_enable = request.GET.getlist("user_id")[0]
    current_user = request.user.id 
    # TODO:: check current user to be same organization as user and also role as admin
    user = User.objects.filter(id=user_to_enable).update(is_active=False)
    if user:
        return JsonResponse({"success": True, "message": "User Deleted"})
    else:
        return JsonResponse({"success": False, "message": "Unable to delete User"})
    
@login_required
def change_role(request):
    user_to_enable = request.GET.getlist("user_id")[0]
    role_id = request.GET.getlist("role_id")[0]
    current_user = request.user.id 
    # TODO:: check current user to be same organization as user and also role as admin
    user = Profile.objects.filter(user_id=user_to_enable).update(role_id=role_id)
    if user:
        return JsonResponse({"success": True, "message": "User Deleted"})
    else:
        return JsonResponse({"success": False, "message": "Unable to delete User"})