from django.urls import path
from .views import PostFilter, PostList, PostDetail,  PostAdd, PostEdit, PostDelete,AddComment,  subscribe


urlpatterns = [
    path("", PostList.as_view()),
    path("search/", PostFilter.as_view(), name='search'),
    path("<int:pk>/", PostDetail.as_view(), name="blog"),
    path("comment/<int:pk>/", AddComment.as_view(), name="add_comment"),
    path('<int:pk>/subscribe/', subscribe, name='subscribe_category'),
    path('add/', PostAdd.as_view(), name='add'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),

]