from django.contrib import admin
from .models import Blog, Category


@admin.action(description='Publish selected posts')
def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action(description='Unpublish selected posts')
def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_published=False)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'created_at', 'views_count')
    list_filter = ('is_published', 'category', 'created_at')
    search_fields = ('title', 'short_description', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_published, make_unpublished]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
