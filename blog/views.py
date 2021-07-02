from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView,  UpdateView, CreateView,  DeleteView
from django.views.generic.base import View

from .models import Mail, Post, Category
from .forms import CommentForm,  PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


class PostList(ListView):
    model = Post
    template_name = 'blog_list.html'
    context_object_name = 'blog_list'
    ordering = '-pub_date'
    paginate_by = 1


class PostDetail(DetailView):
    model = Post
    template_name = 'blog_detail.html'
    context_object_name = 'blog'

    def index(request):
        return render(request, 'blog/blog_detail.html')
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['category'] = list(Category.objects.filter(
    #         post=self.kwargs['pk']).values('category', 'category__name'))
    #     sub = list(Mail.objects.filter(subscribers=self.request.user.id).
    #                values('category'))
    #     context['subscribed'] = [s['category'] for s in sub]
    #     context['author_name'] = Post.objects.filter(id=self.kwargs['pk']).\
    #         values('author__author_id__author_nick')[0]['author__author_id__author_nick']
    #     return context


class PostAdd(CreateView):
    model = Post
    template_name = 'add.html'
    form_class = PostForm
    success_url = '/blog/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostFilter(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    ordering = ['-pub_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostEdit(UpdateView):
    model = Post
    template_name = 'edit.html'
    form_class = PostForm
    success_url = '/blog/'


class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/blog/'


@login_required
def subscribe(request, pk):
    if not Mail.objects.check(subscribers=get_user_model().
                                objects.get(id=request.user.id),
                                category=Category.objects.get(id=pk)):
        Mail.objects.create(subscribers=get_user_model().
                            objects.get(id=request.user.id),
                            category=Category.objects.get(id=pk))
    return redirect('/blog')


class AddComment(View):
    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = Post.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.post = post
            form.save()
        return redirect(post.get_absolute_url())
