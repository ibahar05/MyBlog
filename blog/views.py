from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView,RedirectView, ListView, FormView,CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import *
from .forms import *

class indexView(TemplateView):
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Bahar"
        return context

class RedirecToMaktabt(RedirectView):
    url = "https://maktabkhooneh.org/"

class PostList(PermissionRequiredMixin,LoginRequiredMixin,ListView):
    permission_required = "blog.view_post"
    model = Post
    context_object_name = "posts"
    paginate_by=2


    def get_queryset(self):
        posts = Post.objects.filter(status=True).order_by("-id")
        return posts

class PostDetailView(DetailView):
    model = Post

# class PostCreateView(FormView):
#     template_name = "blog/contact.html"
#     form_class = PostForm
#     success_url = "/post/"

#     def form_valid(self,form):
#         form.save()
#         return super().form_valid(form)

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    success_url = "/post/"

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostEditView(UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/post/"

class PostDeleteView(DeleteView):
    model = Post
    success_url = "/post/"
