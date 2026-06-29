from django.contrib import admin
from .models import StudentPerformance

@admin.register(StudentPerformance)
class StudentPerformanceAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'gpa', 'hours_played_per_week', 'created_at')
    search_fields = ('student_id', 'gamer_tag')