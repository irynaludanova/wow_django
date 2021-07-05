from django.urls import path
from .views import PostsFilter, PostList, PostDetail,  PostAdd, PostEdit, PostDelete,AddComment,  subscribe


urlpatterns = [
    path("", PostList.as_view()),
    path("filter/", PostsFilter.as_view(), name='filter'),
    path("<slug:slug>/", PostDetail.as_view(), name="post_detail"),
    path("comment/<int:pk>/", AddComment.as_view(), name="add_comment"),
    path('<int:pk>/subscribe/', subscribe, name='subscribe_category'),
    path('add', PostAdd.as_view(), name='add'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),

]