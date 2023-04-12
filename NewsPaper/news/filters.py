from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from django.contrib.auth.models import User
from .models import Post
from django import forms


class PostFilter(FilterSet):
    author = ModelChoiceFilter(
        field_name='author__user__username',
        queryset=User.objects.all(),
    )
    date = DateFilter(
        field_name='creation_time',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Поиск после указанной даты',
        lookup_expr='date__gte'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }
