from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from lead.models import Lead
from client.models import Client
from team.models import Team
from order.models import Order
from project.models import Project

@login_required
def dashboard(request):
    team = Team.objects.filter(created_by=request.user)[0]
    leads = Lead.objects.filter(team=team, converted_to_client = False).order_by('-created_at')[0:5]
    clients = Client.objects.filter(team=team).order_by('-created_at')[0:5]
    orders = Order.objects.filter(pic=request.user).order_by('-order_date')[0:5].select_related('client')
    if request.user.is_superuser:
        projects = Project.objects.order_by('-dead_line')[0:5]
    else:
        projects = Project.objects.filter(assign=request.user).order_by('-dead_line')[0:5]
    return render(request,'dashboard/dashboard.html',{
        'leads': leads,
        'clients': clients,
        'orders': orders,
        'projects': projects,
    })
