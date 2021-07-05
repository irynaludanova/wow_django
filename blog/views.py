from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView,  UpdateView, CreateView,  DeleteView
from django.views.generic.base import View

from .models import Mail, Post, Category
from .forms import CommentForm,  PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

class  PostCategory:
    def get_categories(self):
        return Category.objects.all()


class PostList(PostCategory, ListView):
    model = Post
    queryset = Post.objects.filter(draft=False)
    ordering = '-pub_date'
    paginate_by=3


class PostDetail(PostCategory, DetailView):
    model = Post
    queryset = Post.objects.filter(draft=False)
    slug_field="url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class PostAdd(CreateView):
    model = Post
    template_name = 'add.html'
    form_class = PostForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostsFilter(PostCategory, ListView):
    def get_queryset(self):
        queryset = Post.objects.filter(category__in=self.request.GET.getlist('category'))
        return queryset

    def get_context_data(self, *args, **kwargs):
         context = super().get_context_data(*args, **kwargs)
         context["category"] = ''.join([f"category={x}&" for x in self.request.GET.getlist("category")])
         return context


class PostEdit(UpdateView):
    model = Post
    template_name = 'edit.html'
    form_class = PostForm
    success_url = '/'


class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/'


@login_required
def subscribe(request, pk):
    if not Mail.objects.check(subscribers=get_user_model().
                                objects.get(id=request.user.id),
                                category=Category.objects.get(id=pk)):
        Mail.objects.create(subscribers=get_user_model().
                            objects.get(id=request.user.id),
                            category=Category.objects.get(id=pk))
    return redirect('/')


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

