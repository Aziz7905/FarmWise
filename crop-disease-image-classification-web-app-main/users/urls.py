from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.homepage, name='defaulthomepage'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('password-reset/', 
        auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), 
        name='password_reset'),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
        name='password_reset_confirm'),
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
        name='password_reset_complete'),

 
    path('profile/', views.profile, name='profile'),
    path('create-post/', views.create_post, name='create-post'),
    path('posts/', views.post_list, name='post-list'),
    path('posts/<int:pk>/', views.post_detail, name='post-detail'),
    path('posts/<int:pk>/like/', views.like_post, name='like-post'),
    path('posts/<int:pk>/edit/', views.update_post, name='edit-post'),
    path('posts/<int:pk>/delete/', views.delete_post, name='delete-post'),


    path('add-fertilizer/', views.add_fertilizer, name='add-fertilizer'),
    path('add-pesticide/', views.add_pesticide, name='add-pesticide'),
    path('add-material/', views.add_material, name='add-material'),
    path('add-tree/', views.add_tree, name='add-tree'),
    path('add-cropfield/', views.add_cropfield, name='add-cropfield'),
    path('add-task/', views.add_task, name='add-task'),
    path('add-note/', views.add_note, name='add-note'),

    path('dashboard/', views.dashboard, name='dashboard'),


]
