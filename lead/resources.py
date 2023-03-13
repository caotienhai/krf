from import_export import resources
from .models import Lead

class LeadResource(resources.ModelResource):
    class Meta:
        model = Lead
