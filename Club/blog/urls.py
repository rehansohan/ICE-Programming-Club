from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('search/', views.SearchResultsView.as_view(), name='blog_search'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='blog_category'),
    path('edit/<slug:slug>/', views.BlogUpdateView.as_view(), name='blog_edit'),
    path('delete/<slug:slug>/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
]
