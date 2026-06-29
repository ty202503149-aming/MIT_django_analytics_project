from django.shortcuts import render
from .models import StudentPerformance


def analytics_home(request):
    return render(request, 'analytics/home.html')

def train_model(request):
    return render(request, 'analytics/train.html')

def predict(request):
    return render(request, 'analytics/predict.html')

def analytics_home(request):
    performances = StudentPerformance.objects.all().order_by('-created_at')
    return render(request, 'analytics/home.html', {'performances': performances})