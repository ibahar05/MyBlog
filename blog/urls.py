from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path("",views.indexView.as_view(),name="index"),
    path("go_to",views.RedirecToMaktabt.as_view()),
    path("post/",views.PostList.as_view(),name="post"),
    path("post/<int:pk>/", views.PostDetailView.as_view(),name="post_detail"),
    path("post/create/",views.PostCreateView.as_view(),name="post_create"),
    path("post/<int:pk>/edit/", views.PostEditView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete")
]