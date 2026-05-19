from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Blog, Category
from .forms import BlogForm


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Blog.objects.filter(is_published=True).select_related('author', 'category')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()[:10]
        ctx['recent_posts'] = Blog.objects.filter(is_published=True).order_by('-created_at')[:5]
        ctx['popular_posts'] = Blog.objects.filter(is_published=True).order_by('-views_count')[:5]
        return ctx


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        # increment views safely
        obj.increment_views()
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = self.get_object()
        ctx['related_posts'] = Blog.objects.filter(category=post.category, is_published=True).exclude(pk=post.pk)[:4]
        return ctx


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_staff


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_staff


class CategoryListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return Blog.objects.filter(category=self.category, is_published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_category'] = self.category
        ctx['categories'] = Category.objects.all()[:10]
        return ctx


class SearchResultsView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        return Blog.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(short_description__icontains=q),
            is_published=True
        ).distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_query'] = self.request.GET.get('q', '')
        ctx['categories'] = Category.objects.all()[:10]
        return ctx
