from django.urls import path
from movie_app.api import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('movies/', views.movie_list, name='movies-list'),
    path('request-count/', views.RequestCountView.as_view(), name='request_count'),
    path('request-count/reset/', views.ResetRequestCountView.as_view(),
         name='reset_request_count'),
    path('collection/', views.MovieCollectionAV.as_view(), name='collection'),
    path('collection/<uuid:id>', views.MovieCollectionDetailAV.as_view(),
         name='collection-detail')
]
