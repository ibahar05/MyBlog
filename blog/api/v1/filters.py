import django_filters
from django import forms
from blog.models import Post, Category
from accounts.models import Profile


class PostFilter(django_filters.FilterSet):

    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    author = django_filters.ModelMultipleChoiceFilter(
        queryset=Profile.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    status = django_filters.MultipleChoiceFilter(
        choices=[
            (True, "Published"),
            (False, "Draft"),
        ],
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Post
        fields = []
