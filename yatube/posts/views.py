from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User
from .utils import page_num


def index(request):
    post_list = Post.objects.select_related('author', 'group')
    return render(
        request,
        'posts/index.html',
        {'page_obj': page_num(request, post_list)}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related('author')
    return render(
        request,
        'posts/group_list.html',
        {'group': group, 'page_obj': page_num(request, post_list)}
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.select_related(
        'author',
        'group'
    ).filter(author__username=username)
    return render(
        request,
        'posts/profile.html',
        {'page_obj': page_num(request, posts),
         'author': author}
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(
        request,
        'posts/post_detail.html',
        {'post': post}
    )


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.save()
        return redirect('posts:profile', request.user.username)
    return render(
        request,
        'posts/create_post.html',
        {'form': form, 'is_edit': False}
    )


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post.id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:post_detail', post.id)
    return render(
        request,
        'posts/create_post.html',
        {'form': form, 'is_edit': True}
    )
