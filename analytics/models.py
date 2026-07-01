# analytics/models.py

from django.db import models

class StudentRecord(models.Model):
    student_id = models.IntegerField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    gaming_hours = models.FloatField()
    study_hours = models.FloatField()
    sleep_hours = models.FloatField()
    attendance = models.FloatField()
    gaming_genre = models.CharField(max_length=50)
    social_activity = models.FloatField()
    device_usage = models.FloatField()
    reaction_time_ms = models.FloatField()
    addiction_score = models.FloatField()
    stress_level = models.CharField(max_length=10)
    grades = models.FloatField()

    def __str__(self):
        return f"{self.student_id} - {self.gender} - {self.age}"