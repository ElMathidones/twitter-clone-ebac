from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileUpdateForm, SignUpForm, UserUpdateForm
from .models import Follow


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data.get('email')
            user.save()

            display_name = form.cleaned_data.get('display_name')
            if display_name:
                user.profile.display_name = display_name
                user.profile.save()

            login(request, user)
            messages.success(request, 'Conta criada com sucesso.')
            return redirect('feed')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)

    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()

    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    })


@login_required
def edit_profile_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        if 'profile_submit' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileUpdateForm(
                request.POST,
                request.FILES,
                instance=profile
            )
            password_form = PasswordChangeForm(request.user)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Perfil atualizado com sucesso.')
                return redirect('profile', username=request.user.username)

        elif 'password_submit' in request.POST:
            user_form = UserUpdateForm(instance=request.user)
            profile_form = ProfileUpdateForm(instance=profile)
            password_form = PasswordChangeForm(request.user, request.POST)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Senha alterada com sucesso.')
                return redirect('profile', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    })


@login_required
def follow_toggle_view(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if user_to_follow == request.user:
        messages.warning(request, 'Você não pode seguir a si mesmo.')
        return redirect('profile', username=username)

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )

    if not created:
        follow.delete()
        messages.success(request, f'Você deixou de seguir {user_to_follow.username}.')
    else:
        messages.success(request, f'Você começou a seguir {user_to_follow.username}.')

    return redirect('profile', username=username)
