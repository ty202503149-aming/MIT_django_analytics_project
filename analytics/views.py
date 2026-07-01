from django.shortcuts import render
from django.db.models import Avg, Count
import joblib
import pandas as pd
import os

from .models import StudentRecord


def welcome(request):
    # First page users see at "/"
    return render(request, "analytics/welcome.html")


def overview(request):
    stats = {
        "avg_gaming_hours": StudentRecord.objects.aggregate(Avg("gaming_hours"))["gaming_hours__avg"],
        "avg_study_hours": StudentRecord.objects.aggregate(Avg("study_hours"))["study_hours__avg"],
        "avg_sleep_hours": StudentRecord.objects.aggregate(Avg("sleep_hours"))["sleep_hours__avg"],
        "avg_grades": StudentRecord.objects.aggregate(Avg("grades"))["grades__avg"],
        "stress_counts": StudentRecord.objects.values("stress_level").annotate(total=Count("id")),
    }
    return render(request, "analytics/overview.html", {"stats": stats})


def predict(request):
    prediction = None
    errors = []

    if request.method == "POST":
        def to_int(value, field_name):
            if value in (None, ""):
                errors.append(f"{field_name} is required.")
                return None
            try:
                return int(value)
            except ValueError:
                errors.append(f"{field_name} must be an integer.")
                return None

        def to_float(value, field_name):
            if value in (None, ""):
                errors.append(f"{field_name} is required.")
                return None
            try:
                return float(value)
            except ValueError:
                errors.append(f"{field_name} must be a number.")
                return None

        raw_age = request.POST.get("age")
        raw_gender = request.POST.get("gender")
        raw_gaming_hours = request.POST.get("gaming_hours")
        raw_study_hours = request.POST.get("study_hours")
        raw_sleep_hours = request.POST.get("sleep_hours")
        raw_attendance = request.POST.get("attendance")
        raw_gaming_genre = request.POST.get("gaming_genre")
        raw_social_activity = request.POST.get("social_activity")
        raw_device_usage = request.POST.get("device_usage")
        raw_reaction_time_ms = request.POST.get("reaction_time_ms")

        age = to_int(raw_age, "Age")
        gender = raw_gender
        gaming_hours = to_float(raw_gaming_hours, "Gaming hours per week")
        study_hours = to_float(raw_study_hours, "Study hours per week")
        sleep_hours = to_float(raw_sleep_hours, "Sleep hours per night")
        attendance = to_float(raw_attendance, "Attendance (%)")
        gaming_genre = raw_gaming_genre
        social_activity = to_float(raw_social_activity, "Social activity (hours/week)")
        device_usage = to_float(raw_device_usage, "Device usage (hours/day)")
        reaction_time_ms = to_float(raw_reaction_time_ms, "Reaction time (ms)")

        if errors or not gender or not gaming_genre:
            if not gender:
                errors.append("Gender is required.")
            if not gaming_genre:
                errors.append("Gaming genre is required.")

            return render(
                request,
                "analytics/predict.html",
                {
                    "prediction": None,
                    "errors": errors,
                },
            )

        sample = pd.DataFrame([{
            "age": age,
            "gender": gender,
            "gaming_hours": gaming_hours,
            "study_hours": study_hours,
            "sleep_hours": sleep_hours,
            "attendance": attendance,
            "gaming_genre": gaming_genre,
            "social_activity": social_activity,
            "device_usage": device_usage,
            "reaction_time_ms": reaction_time_ms,
        }])

        addiction_model = joblib.load(os.path.join("ml", "addiction_model.joblib"))
        stress_model = joblib.load(os.path.join("ml", "stress_model.joblib"))

        addiction_score = float(addiction_model.predict(sample)[0])
        stress_level = str(stress_model.predict(sample)[0])

        prediction = {
            "addiction_score": round(addiction_score, 2),
            "stress_level": stress_level,
        }

    return render(request, "analytics/predict.html", {"prediction": prediction})