from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from elections.admin_views import (
    admin_dashboard, manage_elections, election_results, 
    manage_users, export_election_results, toggle_election_status, 
    live_vote_data
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Custom Admin URLs
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-elections/', manage_elections, name='manage_elections'),
    path('admin-election-results/<int:election_id>/', election_results, name='election_results'),
    path('admin-users/', manage_users, name='manage_users'),
    path('admin-export/<int:election_id>/', export_election_results, name='export_election_results'),
    path('admin-toggle-status/<int:election_id>/', toggle_election_status, name='toggle_election_status'),
    path('admin-live-data/<int:election_id>/', live_vote_data, name='live_vote_data'),
    
    # Regular URLs
    path('', include('users.urls')),  # This already includes your users URLs
    path('users/', include('users.urls')),  # Add this line for explicit /users/ paths
    path('elections/', include('elections.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
