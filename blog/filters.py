from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'pub_date': ['gt'],
            'title': ['icontains'],
            'author__author_id__author_nick': ['icontains'],
        }
