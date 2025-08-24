from django.contrib import admin
from .models import Election, Position, Candidate, Vote

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'status']
    list_filter = ['status', 'start_date']
    search_fields = ['title']

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'election', 'max_candidates']
    list_filter = ['election']

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'student_id', 'position', 'vote_count']
    list_filter = ['position__election', 'position']
    search_fields = ['name', 'student_id']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['voter', 'candidate', 'position', 'timestamp']
    list_filter = ['timestamp', 'position']
    readonly_fields = ['voter', 'candidate', 'position', 'timestamp']
