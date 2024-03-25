from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Subscriber, Category, MyModel, Author
from datetime import datetime
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.generic.base import View
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from django.utils.translation import pgettext_lazy
from django.utils.translation import gettext as _

from rest_framework import viewsets
from rest_framework import permissions
import pytz

from news.serializers import *
from news.models import *



import logging
logger = logging.getLogger(__name__)


class Index(View):
    def get(self, request):
        models = MyModel.objects.all()

        context = {
            'models': models,
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'index.html', context))

    # по пост-запросу будем добавлять в сессию часовой пояс,
    # который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/index/')


class AuthorViewset(viewsets.ModelViewSet):
   queryset = Author.objects.all()
   serializer_class = AuthorSerializer


class PostViewset(viewsets.ModelViewSet):
   queryset = Post.objects.all()
   serializer_class = PostSerializer


class CommentViewset(viewsets.ModelViewSet):
   queryset = Comment.objects.all()
   serializer_class = CommentSerializer


class Categories(models.Model):
    name = models.CharField(max_length=100, help_text=_('category name'))  # добавим переводящийся текст подсказку к полю



class PostList(LoginRequiredMixin, ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'main.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'Post'
    pk_url_kwarg = 'pk'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

class PostSearch(ListView):
    form_class = PostFilter
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'Posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = "Следующие новости скоро опубликуем!"
        context['filterset'] = self.filterset
        return context

def create_news(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')

    return render(request, 'news_create.html', {'form': form})


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    success_url = reverse_lazy('main')

    def form_valid(self, form):
        time_now = datetime.now()
        time_day_ago = time_now - timedelta(hours=24)
        post_list = Post.objects.filter(Q(post_creation_date__gte=time_day_ago) & Q(
            author=form.instance.author))
        if len(post_list) <= 3:
            return super().form_valid(form)
        else:
            return HttpResponse(f'Доступный максимум 3 статьи за сутки.Вы разместили {len(post_list)}')

    def post(self, request, *args, **kwargs):
        p = Post(title=request.POST['title'],
                 text=request.POST['text'],
                 categoryType=request.POST['categoryType'],
                 author=Author.objects.get(id=request.POST['author']),
                 )
        p.save()
        subscribers_list = []
        email_list = set()
        selected_categories = request.POST.getlist('postCategory')
        for i in selected_categories:
            p.postCategory.add(i)
            subscribers_list.append(User.objects.filter(cats=i))

        for user_obj in subscribers_list:
            for i in user_obj:
                email_list.add(i.email)
        email_list = list(email_list)



class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('post_list')

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class ArticleList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'main.html'
    context_object_name = 'Posts'
    paginate_by = 10


class ArticleDetail(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'Post'
    pk_url_kwarg = 'id'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_article',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class ArticleEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.update_article',)
    form_class = PostForm
    model = Post
    template_name = 'article_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_article',)
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscriber':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('pk')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.category).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_subscriber'] = Subscription.objects.filter(user=self.request.user, category=self.category).exists()
        context['category'] = self.category
        return context