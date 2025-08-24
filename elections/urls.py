from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<int:election_id>/', views.election_detail, name='election_detail'),
    path('vote/<int:position_id>/', views.vote_for_position, name='vote_position'),
]