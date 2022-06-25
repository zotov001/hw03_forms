from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


LIMIT_POSTS_ON_PAGE: int = 10


def index(request):
    """Все посты, разбивает по LIMIT_POSTS_ON_PAGE штук на странице"""
    post_list = Post.objects.select_related('author', 'group')
    page_number = request.GET.get('page')
    paginator = Paginator(post_list, LIMIT_POSTS_ON_PAGE).get_page(page_number)
    return render(
        request, 'posts/index.html', {'page_obj': paginator})


def group_posts(request, slug):
    """Посты группы, разбивает по LIMIT_POSTS_ON_PAGE штук на странице."""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, LIMIT_POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    context = {
        'group': group,
        'page_obj': paginator.get_page(page_number),
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Посты автора, разбивает по LIMIT_POSTS_ON_PAGE штук на странице."""
    author = get_object_or_404(User, username=username)
    posts_list = author.posts.all()
    posts_count = posts_list.count()
    paginator = Paginator(posts_list, LIMIT_POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    context = {
        'author': author,
        'page_obj': paginator.get_page(page_number),
        'posts_count': posts_count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Выводит определенный пост и инф о нем."""
    post = get_object_or_404(Post.objects.select_related(
        'author',
        'group',
    ), id=post_id)
    posts_count = Post.objects.filter(author=post.author).count()
    context = {
        'post': post,
        'posts_count': posts_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request, is_edit=False):
    """Создание нового поста."""
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user.username)
    return render(request, "posts/create_post.html", {'form': form})


@login_required
def post_edit(request, post_id):
    """Редактирование поста."""
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    if not form.is_valid():
        context = {
            'form': form,
            'is_edit': True
        }
        return render(request, 'posts/create_post.html', context)
    if post.author == request.user and request.method == "POST":
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:post_detail', post_id)
    return redirect('posts:post_detail', post_id)
