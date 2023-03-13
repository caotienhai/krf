from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Userprofile
from django.shortcuts import render, redirect
from team.models import Team
from .forms import SignUpForm, UpdateUserForm
from djapos import google

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Userprofile.objects.create(user = user)
            team = Team.objects.create(name='The team name',created_by = request.user)
            team.members.add(request.user)
            team.save()
            
            return redirect('/log-in/')
    else:
        form = SignUpForm()
    
    return render(request,'userprofile/signup.html',{
        'form': form
    })
@login_required
def myaccount(request):
    team = Team.objects.filter(created_by=request.user)[0]
    return render(request, 'userprofile/myaccount.html',{
        'team': team
    })
    
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'userprofile/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('userprofile:myaccount')
    
@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='userprofile:myaccount')
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'userprofile/update_profile.html', {'user_form': user_form,})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'userprofile/password_reset.html'
    success_url = reverse_lazy('userprofile:password_reset_done')
    email_template_name = 'userprofile/password_reset_email.html'
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'userprofile/password_reset_confirm.html'
    success_url = reverse_lazy('userprofile:login')