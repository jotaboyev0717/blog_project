from datetime import timedelta

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import RegisterForm, PostForm, CommentForm
from .models import Post, Category


def home(request):
    approved_posts = Post.objects.filter(is_approved=True)

    now = timezone.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    context = {
        'latest_posts': approved_posts.order_by('-created_at')[:6],
        'most_viewed': approved_posts.order_by('-views')[:6],
        'weekly_popular': approved_posts.filter(created_at__gte=week_ago).order_by('-views')[:6],
        'monthly_popular': approved_posts.filter(created_at__gte=month_ago).order_by('-views')[:6],
        'featured_posts': approved_posts.filter(is_featured=True)[:6],
    }
    return render(request, 'blog/home.html', context)


def post_list(request):
    posts = Post.objects.filter(is_approved=True)

    category_slug = request.GET.get('category')
    tag = request.GET.get('tag')
    query = request.GET.get('q')

    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    if tag:
        posts = posts.filter(tags__name__in=[tag])
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    context = {
        'posts': posts.distinct(),
        'categories': Category.objects.all(),
        'query': query or '',
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_approved=True)

    Post.objects.filter(pk=post.pk).update(views=post.views + 1)
    post.views += 1

    comments = post.comments.select_related('author').all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.is_approved = False
            post.save()
            form.save_m2m()
            return redirect('my_posts')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/my_posts.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})
