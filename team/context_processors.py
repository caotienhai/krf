from .models import Team

def team(request):
    if request.user.is_authenticated:
        team = Team.objects.filter(members__in=request.user)[0]
    else:
        team = None
    return {'team':team}