from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from django.urls import reverse_lazy

from .models import Post
from .filters import PostsFilter
from .forms import PostForm
from .resources import *


class PostsList(ListView):
    model = Post
    ordering = '-created_on'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_of_posts'] = len(Post.objects.all())
        return context


class NewsList(ListView):
    model = Post
    queryset = Post.objects.filter(type='N')
    ordering = '-created_on'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_of_news'] = len(Post.objects.filter(type='N'))
        return context

class ArticlesList(ListView):
    model = Post
    queryset = Post.objects.filter(type='A')
    ordering = '-created_on'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_of_articles'] = len(Post.objects.filter(type='A'))
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostsSearch(ListView):
    model = Post
    ordering = '-created_on'
    template_name = 'posts_search.html'
    context_object_name = 'posts_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def get_initial(self):
        return {'type': news}


class ArticlesCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def get_initial(self):
        return {'type': article}


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    # template_name = 'news_edit.html'

    def get_template_names(self):
        post = self.get_object()
        if post.type == news and 'news' in self.request.path:
            self.template_name = 'news_edit.html'
        elif post.type == article and 'article' in self.request.path:
            self.template_name = 'article_edit.html'
        else:
            self.template_name = '404.html'
        return self.template_name

class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('posts_list')

    def get_template_names(self):
        post = self.get_object()
        if post.type == news and 'news' in self.request.path:
            self.template_name = 'news_delete.html'
        elif post.type == article and 'article' in self.request.path:
            self.template_name = 'article_delete.html'
        else:
            self.template_name = '404.html'
        return self.template_name