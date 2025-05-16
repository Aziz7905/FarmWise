from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import (
    UserRegisterForm, UserUpdateForm, FarmerProfileUpdateForm,
    FarmerPostForm, CommentForm, FertilizerForm, PesticideForm, MaterialForm,
    TreeTypeForm, CropFieldForm, CropTaskForm, NoteForm
)
from .models import FarmerPost

from payments.models import SubscriptionPlan, FarmerSubscription
from payments.enum import SubscriptionTier


def homepage(request):
    return render(request, 'defaulthomepage.html') 


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

           
            profile = user.farmerprofile  
            free_plan = SubscriptionPlan.objects.filter(tier=SubscriptionTier.FREE.name).first()
            if free_plan:
                FarmerSubscription.objects.create(
                    farmer=profile,
                    plan=free_plan,
                    stripe_customer_id='free-internal',  
                    active=True
                )

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






@login_required
def add_fertilizer(request):
    form = FertilizerForm(request.POST or None)
    if form.is_valid():
        fert = form.save(commit=False)
        fert.farmer = request.user.farmerprofile
        fert.save()
        return redirect('dashboard')
    return render(request, 'users/add_fertilizer.html', {'form': form})


@login_required
def add_pesticide(request):
    form = PesticideForm(request.POST or None)
    if form.is_valid():
        item = form.save(commit=False)
        item.farmer = request.user.farmerprofile
        item.save()
        return redirect('dashboard')
    return render(request, 'users/add_pesticide.html', {'form': form})


@login_required
def add_material(request):
    form = MaterialForm(request.POST or None)
    if form.is_valid():
        item = form.save(commit=False)
        item.farmer = request.user.farmerprofile
        item.save()
        return redirect('dashboard')
    return render(request, 'users/add_material.html', {'form': form})


@login_required
def add_tree(request):
    form = TreeTypeForm(request.POST or None)
    if form.is_valid():
        tree = form.save(commit=False)
        tree.farmer = request.user.farmerprofile
        tree.save()
        return redirect('dashboard')
    return render(request, 'users/add_tree.html', {'form': form})


@login_required
def add_cropfield(request):
    form = CropFieldForm(request.POST or None)
    if form.is_valid():
        field = form.save(commit=False)
        field.farmer = request.user.farmerprofile
        field.save()
        return redirect('dashboard')
    return render(request, 'users/add_cropfield.html', {'form': form})


@login_required
def add_task(request):
    form = CropTaskForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.farmer = request.user.farmerprofile
        task.save()
        return redirect('dashboard')
    return render(request, 'users/add_task.html', {'form': form})


@login_required
def add_note(request):
    form = NoteForm(request.POST or None)
    if form.is_valid():
        note = form.save(commit=False)
        note.farmer = request.user.farmerprofile
        note.save()
        return redirect('dashboard')
    return render(request, 'users/add_note.html', {'form': form})



@login_required
def dashboard(request):
    profile = request.user.farmerprofile
    subscription = getattr(profile, 'farmersubscription', None)
    current_plan = subscription.plan.tier if subscription and subscription.active else "FREE"
    context = {
        'profile': profile,
        'fertilizers': profile.fertilizers.all(),
        'pesticides': profile.pesticides.all(),
        'materials': profile.materials.all(),
        'trees': profile.trees.all(),
        'fields': profile.cropfield_set.all(),
        'tasks': profile.croptask_set.all().order_by('date')[:5],
        'notes': profile.note_set.all(),
        'current_plan': current_plan,
    }
    return render(request, 'users/dashboard.html', context)




