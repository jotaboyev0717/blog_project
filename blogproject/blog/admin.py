from django.contrib import admin

from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_approved', 'is_featured', 'views', 'created_at']
    list_filter = ['is_approved', 'is_featured', 'category', 'created_at']
    list_editable = ['is_approved', 'is_featured']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at']
    search_fields = ['text']
