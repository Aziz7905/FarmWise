from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import (
    UserRegisterForm, UserUpdateForm, FarmerProfileUpdateForm,
    FarmerPostForm, CommentForm
)
from .models import FarmerPost


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = FarmerProfileUpdateForm(request.POST, request.FILES, instance=request.user.farmerprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = FarmerProfileUpdateForm(instance=request.user.farmerprofile)

    return render(request, 'users/profile.html', {'u_form': u_form, 'p_form': p_form})


@login_required
def create_post(request):
    profile = request.user.farmerprofile
    if request.method == 'POST':
        form = FarmerPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = profile
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post-list')
    else:
        form = FarmerPostForm()
    return render(request, 'users/create_post.html', {'form': form})


def post_list(request):
    posts = FarmerPost.objects.all().order_by('-date_posted')
    return render(request, 'users/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(FarmerPost, pk=pk)
    comments = post.comments.all().order_by('-date_posted')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'users/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


@login_required
def like_post(request, pk):
    post = get_object_or_404(FarmerPost, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


@login_required
def update_post(request, pk):
    post = get_object_or_404(FarmerPost, pk=pk)
    if request.user != post.author.user:
        return redirect('post-detail', pk=pk)

    form = FarmerPostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('post-detail', pk=pk)

    return render(request, 'users/update_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(FarmerPost, pk=pk)
    if request.user != post.author.user:
        return redirect('post-detail', pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post-list')
    return render(request, 'users/delete_post.html', {'post': post})



