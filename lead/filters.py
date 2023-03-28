from .models import Comment, Contact
import django_filters

class CommentFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(
        lookup_expr=('icontains'),
        widget=django_filters.widgets.RangeWidget(attrs={'type':'date'}))
    class Meta:
        model = Comment
        fields = ['lead', 'team', 'created_by', 'created_at' ]
        
class LeadContactFilter(django_filters.FilterSet):    
    class Meta:
        model = Contact
        fields = ['lead', 'team', 'assign_to']