from .models import Team

def team(request):
    if request.user.is_authenticated:
        team = None
        #team = Team.objects.filter(created_by=request.user)[0]
    else:
        team = None
    return {'team':team}