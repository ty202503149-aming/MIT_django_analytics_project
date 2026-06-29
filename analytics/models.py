from django.db import models


class StudentPerformance(models.Model):
    student_id = models.CharField(max_length=50)

    age = models.IntegerField()
    gender = models.CharField(max_length=10)  # e.g., 'Male', 'Female', 'Other'

    gaming_hours = models.FloatField()        # hours of gaming per day or week
    study_hours = models.FloatField()
    sleep_hours = models.FloatField()

    attendance = models.FloatField()          # e.g., percentage 0–100
    gaming_genre = models.CharField(max_length=100)  # e.g., 'FPS', 'MOBA', 'RPG'

    social_activity = models.FloatField()     # e.g., numeric score or hours
    device_usage = models.FloatField()        # e.g., hours per day

    reaction_time_ms = models.FloatField()    # reaction time in milliseconds
    addiction_score = models.FloatField()     # e.g., scale 0–100
    stress_level = models.FloatField()        # e.g., scale 0–10

    grades = models.FloatField()              # numeric grade or GPA

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id} - {self.grades}"