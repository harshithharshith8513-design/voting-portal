from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Election, Position, Candidate, Vote
from users.models import UserProfile
import csv
from datetime import datetime

@staff_member_required
def admin_dashboard(request):
    """Main admin dashboard with statistics and quick actions"""
    total_users = User.objects.count()
    total_elections = Election.objects.count()
    active_elections = Election.objects.filter(status='active').count()
    total_votes = Vote.objects.count()
    
    # Recent activity
    recent_votes = Vote.objects.select_related('voter', 'candidate', 'position').order_by('-timestamp')[:10]
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    # Election statistics
    election_stats = Election.objects.annotate(
        vote_count=Count('position__candidate__vote'),
        candidate_count=Count('position__candidate', distinct=True),
        position_count=Count('position', distinct=True)
    ).order_by('-id')[:5]
    
    # Department-wise user distribution
    dept_stats = UserProfile.objects.values('department').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    context = {
        'total_users': total_users,
        'total_elections': total_elections,
        'active_elections': active_elections,
        'total_votes': total_votes,
        'recent_votes': recent_votes,
        'recent_users': recent_users,
        'election_stats': election_stats,
        'dept_stats': dept_stats,
    }
    
    return render(request, 'admin/custom_dashboard.html', context)

@staff_member_required
def manage_elections(request):
    # Count elections by status
    active_count = Election.objects.filter(status='active').count()
    upcoming_count = Election.objects.filter(status='upcoming').count()
    ended_count = Election.objects.filter(status='ended').count()
    total_count = Election.objects.count()

    context = {
        'active_count': active_count,
        'upcoming_count': upcoming_count,
        'ended_count': ended_count,
        'total_count': total_count,
    }
    return render(request, 'admin/manage_elections.html', context)


@staff_member_required
def election_results(request, election_id):
    """Detailed election results page"""
    election = get_object_or_404(Election, id=election_id)
    results = {}
    
    for position in election.position_set.all():
        candidates = position.candidate_set.annotate(
            total_votes=Count('vote')  # Changed from vote_count to avoid conflict
        ).order_by('-total_votes')
        
        total_position_votes = sum(c.total_votes for c in candidates)
        
        # Calculate percentages
        for candidate in candidates:
            if total_position_votes > 0:
                candidate.percentage = (candidate.total_votes / total_position_votes) * 100
            else:
                candidate.percentage = 0
        
        results[position] = {
            'candidates': candidates,
            'total_votes': total_position_votes
        }
    
    return render(request, 'admin/election_results.html', {
        'election': election,
        'results': results
    })

@staff_member_required
def manage_users(request):
    """User management page"""
    search_query = request.GET.get('search', '')
    department_filter = request.GET.get('department', '')
    
    users = User.objects.select_related('userprofile')
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(userprofile__student_id__icontains=search_query)
        )
    
    if department_filter:
        users = users.filter(userprofile__department=department_filter)
    
    # Get all departments for filter dropdown
    departments = UserProfile.objects.values_list('department', flat=True).distinct()
    
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    return render(request, 'admin/manage_users.html', {
        'users': users,
        'departments': departments,
        'search_query': search_query,
        'department_filter': department_filter
    })

@staff_member_required
def export_election_results(request, election_id):
    """Export election results to CSV"""
    election = get_object_or_404(Election, id=election_id)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="election_results_{election.id}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Position', 'Candidate', 'Student ID', 'Votes', 'Percentage'])
    
    for position in election.position_set.all():
        candidates = position.candidate_set.annotate(
            total_votes=Count('vote')  # Changed from vote_count to avoid conflict
        ).order_by('-total_votes')
        
        total_votes = sum(c.total_votes for c in candidates)
        
        for candidate in candidates:
            percentage = (candidate.total_votes / total_votes * 100) if total_votes > 0 else 0
            writer.writerow([
                position.name,
                candidate.name,
                candidate.student_id,
                candidate.total_votes,
                f'{percentage:.2f}%'
            ])
    
    return response

@staff_member_required
def toggle_election_status(request, election_id):
    """Toggle election status (active/ended)"""
    if request.method == 'POST':
        election = get_object_or_404(Election, id=election_id)
        new_status = request.POST.get('status')
        
        if new_status in ['active', 'ended', 'upcoming']:
            election.status = new_status
            election.save()
            messages.success(request, f'Election status updated to {new_status}')
        else:
            messages.error(request, 'Invalid status')
    
    return redirect('manage_elections')

@staff_member_required
def live_vote_data(request, election_id):
    """API endpoint for live vote data (JSON response)"""
    election = get_object_or_404(Election, id=election_id)
    data = {}
    
    for position in election.position_set.all():
        candidates_data = []
        for candidate in position.candidate_set.all():
            vote_count = candidate.vote_set.count()
            candidates_data.append({
                'name': candidate.name,
                'votes': vote_count
            })
        data[position.name] = candidates_data
    
    return JsonResponse(data)
