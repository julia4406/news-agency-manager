from django.urls import path

from manager_app import views


app_name = 'manager_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('author/', views.author, name='author'),
    path('page-header/', views.page_header, name='page_header'),

    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.user_logout_view, name='logout'),

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
        'publication/status/<int:pk>/',
        views.update_status_of_publication,
        name='publication-status'
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
    path(
        'subject/<int:pk>/publications/',
        views.SubjectRelatedPublicationsListView.as_view(),
        name='subject-related'),

    path(
        'under-construction/',
        views.under_construction,
        name='under_construction'
    ),
]
