from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Post

class PostList(ListView):
    model = Post
    template_name = 'diary/home.html'
    ordering = '-pk'

class PostDetail(DetailView):
    model = Post

class PostCreate(CreateView):
    model = Post
    fields = ['title', 'content']