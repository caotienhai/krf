from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Team
from .forms import TeamForm

@login_required 
def edit_team(request,pk):
    team = get_object_or_404(Team,members__id=request.user.id, pk=pk)
    if request.method == 'POST':
        form = TeamForm(request.POST,instance=team)
        if form.is_valid():
            form.save()
            messages.success(request,'Changes Saved')
            return redirect('userprofile:myaccount')
    else:
        form = TeamForm(instance=team)
    return render(request, 'team/edit_team.html',{
        'team': team,
        'form': form
    })
    
@login_required 
def detail(request,pk):
    team = get_object_or_404(Team,members__id=request.user.id, pk=pk)
    return render(request, 'team/detail.html',{'team':team})