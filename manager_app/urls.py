from django.urls import path
from django.contrib.auth import views as auth_views

from manager_app import views


app_name = "manager_app"
urlpatterns = [
    #path("", index, name="index"),

    # ----------------------------------
    # Pages
    path('', views.index, name="index"),
    path('contact-us/', views.contact_us, name='contact-us'),
    # path('about-us/', views.about_us, name='about-us'),
    path('author/', views.author, name='author'),
    path(
        'publications/',
        views.PublicationListView.as_view(),
        name='publication-list'
    ),
    path(
        'publications/create',
        views.PublicationCreateView.as_view(),
        name='publication-create'
    ),
    path(
        'publications/update/<int:pk>/',
        views.PublicationUpdateView.as_view(),
        name='publication-update'
    ),
    path(
        'publications/<int:pk>/',
        views.PublicationDetailView.as_view(),
         name='publication-detail'
    ),
    path(
        'publications/delete/<int:pk>/',
        views.PublicationDeleteView.as_view(),
         name='publication-delete'
    ),
    path(
        'editors/',
        views.EditorListView.as_view(),
        name='editor-list'),
    path(
        'editors/<int:pk>/',
        views.EditorDetailView.as_view(),
        name='editor-detail'),
    path(
        'editors/create',
        views.EditorCreateView.as_view(),
        name='editor-create'),
    path(
        'editors/update/<int:pk>',
        views.EditorUpdateView.as_view(),
        name='editor-update'),
    path(
        'editors/delete/<int:pk>',
        views.EditorDeleteView.as_view(),
        name='editor-delete'),
    path(
        'subjects/',
        views.SubjectListView.as_view(),
        name='subject-list'),
    path(
        'subjects/create/',
        views.SubjectCreateView.as_view(),
        name='subject-create'),
    path(
        'subjects/update/<int:pk>/',
        views.SubjectUpdateView.as_view(),
        name='subject-update'),
    path(
        'subjects/delete/<int:pk>/',
        views.SubjectDeleteView.as_view(),
        name='subject-delete'),





    # Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.user_logout_view, name='logout'),
    # path('accounts/register/', views.registration, name='register'),
    # path('accounts/password-change/', views.UserPasswordChangeView.as_view(),
    #      name='password_change'),
    # path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
    #     template_name='accounts/password_change_done.html'
    # ), name="password_change_done"),
    # path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    # path('accounts/password-reset-confirm/<uidb64>/<token>/',
    #      views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
    #     template_name='accounts/password_reset_done.html'
    # ), name='password_reset_done'),
    # path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
    #     template_name='accounts/password_reset_complete.html'
    # ), name='password_reset_complete'),
    #
    # # Sections
    # path('presentation/', views.presentation, name='presentation'),
    path('page-header/', views.page_header, name='page_header'),
    # path('features/', views.features, name='features'),
    # path('navbar/', views.navbars, name='navbar'),
    # path('nav-tabs/', views.nav_tabs, name='nav_tabs'),
    # path('pagination/', views.pagination, name='pagination'),
    # path('forms/', views.forms, name='forms'),
    # path('inputs/', views.inputs, name='inputs'),
    # path('avatars/', views.avatars, name='avatars'),
    # path('badges/', views.badges, name='badges'),
    # path('breadcrumbs/', views.breadcrumbs, name='breadcrumbs'),
    # path('buttons/', views.buttons, name='buttons'),
    # path('dropdowns/', views.dropdowns, name='dropdowns'),
    # path('progress-bars/', views.progress_bars, name='progress_bars'),
    # path('toggles/', views.toggles, name='toggles'),
    # path('typography/', views.typography, name='typography'),
    # path('alerts/', views.alerts, name='alerts'),
    # path('modals/', views.modals, name='modals'),
    # path('tooltips/', views.tooltips, name='tooltips'),
    path('under-construction/', views.under_construction, name='under_construction'),
]

# for all not-ready pages: {% url 'manager_app:under_construction' %}

