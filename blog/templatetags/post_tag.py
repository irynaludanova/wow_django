from django import template
from blog.models import Category, Post

register = template.Library()

@register.simple_tag()
def get_categories():
    return  Category.objects.all()


@register.inclusion_tag('blog/tags/last_posts.html')
def get_last_posts(count=5):
    posts = Post.objects.order_by('-pub_date')[:count]
    return{'last_posts': posts }
