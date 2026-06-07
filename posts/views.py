from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Follow
from .forms import CommentForm, PostForm
from .models import Like, Post


@login_required
def feed_view(request):
    followed_users = Follow.objects.filter(
        follower=request.user
    ).values_list('following', flat=True)

    posts = Post.objects.filter(
        author_id__in=followed_users
    ).select_related('author', 'author__profile').prefetch_related('likes', 'comments')

    form = PostForm()
    liked_post_ids = set(
        request.user.likes.values_list('post_id', flat=True)
    )

    return render(request, 'posts/feed.html', {
        'posts': posts,
        'form': form,
        'liked_post_ids': liked_post_ids,
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
def post_detail_view(request, pk):
    post = get_object_or_404(
        Post.objects.select_related('author', 'author__profile'),
        pk=pk
    )

    comments = post.comments.select_related('user', 'user__profile').all()
    liked_post_ids = set(
        request.user.likes.values_list('post_id', flat=True)
    )

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

            messages.success(request, 'Comentário publicado com sucesso.')
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'liked_post_ids': liked_post_ids,
    })


@login_required
def like_toggle_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if created:
        messages.success(request, 'Postagem curtida.')
    else:
        like.delete()
        messages.success(request, 'Curtida removida.')

    next_url = request.POST.get('next') or 'feed'
    return redirect(next_url)


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
