from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Follow
from .forms import PostForm
from .models import Post


@login_required
def feed_view(request):
    followed_users = Follow.objects.filter(
        follower=request.user
    ).values_list('following', flat=True)

    posts = Post.objects.filter(
        author_id__in=followed_users
    ).select_related('author', 'author__profile')

    form = PostForm()

    return render(request, 'posts/feed.html', {
        'posts': posts,
        'form': form,
    })


@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(request, 'Postagem criada com sucesso.')
            return redirect('profile', username=request.user.username)

    return redirect('feed')


@login_required
def update_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            messages.success(request, 'Postagem atualizada com sucesso.')
            return redirect('profile', username=request.user.username)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_form.html', {
        'form': form,
        'post': post,
    })


@login_required
def delete_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Postagem excluída com sucesso.')
        return redirect('profile', username=request.user.username)

    return render(request, 'posts/post_confirm_delete.html', {
        'post': post,
    })
