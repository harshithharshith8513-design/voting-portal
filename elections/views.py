from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Election, Position, Candidate, Vote

@login_required
def dashboard(request):
    active_elections = Election.objects.filter(status='active')
    return render(request, 'elections/dashboard.html', {
        'elections': active_elections
    })

@login_required
def election_detail(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    
    if not election.is_active():
        messages.error(request, 'This election is not currently active')
        return redirect('dashboard')
    
    positions = Position.objects.filter(election=election)
    voted_positions = Vote.objects.filter(
        voter=request.user,
        position__election=election
    ).values_list('position_id', flat=True)
    
    return render(request, 'elections/election_detail.html', {
        'election': election,
        'positions': positions,
        'voted_positions': voted_positions
    })

@login_required
def vote_for_position(request, position_id):
    position = get_object_or_404(Position, id=position_id)
    
    if Vote.objects.filter(voter=request.user, position=position).exists():
        messages.error(request, 'You have already voted for this position')
        return redirect('election_detail', election_id=position.election.id)
    
    candidates = Candidate.objects.filter(position=position)
    
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate')
        candidate = get_object_or_404(Candidate, id=candidate_id)
        
        Vote.objects.create(
            voter=request.user,
            candidate=candidate,
            position=position
        )
        
        candidate.vote_count += 1
        candidate.save()
        
        messages.success(request, f'Your vote for {position.name} has been recorded!')
        return redirect('election_detail', election_id=position.election.id)
    
    return render(request, 'elections/vote.html', {
        'position': position,
        'candidates': candidates
    })
