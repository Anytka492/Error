from django.urls import path
from django.views.generic import TemplateView
from . import views

from .views import *

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('news/', PostList.as_view(), name='post_list'),
    path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),

    path('article/', ArticleList.as_view(), name='article_list'),
    path('article/<int:id>/', ArticleDetail.as_view(), name='article_detail'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('article/<int:pk>/update/', ArticleEdit.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('categories/<int:pk>', views.CategoryListView.as_view(), name='category_list'),
    path('index/', views.Index.as_view()),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
