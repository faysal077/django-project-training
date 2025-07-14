'''

from django.shortcuts import render, redirect, get_object_or_404
from dashboard.models import Training
from dashboard.forms import TrainingForm
from django.contrib import messages


def list_trainings(request):
    trainings = Training.objects.order_by('-created_at')
    return render(request, "dashboard/trainings/list.html", {"trainings": trainings})


def add_training(request):
    if request.method == "POST":
        form = TrainingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Training added successfully.")
            return redirect("dashboard:training_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TrainingForm()

    return render(request, "dashboard/trainings/add.html", {"form": form})

'''
from django.shortcuts import render, redirect
from dashboard.models import Training
from dashboard.forms import TrainingForm
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string


def list_trainings(request):
    trainings = Training.objects.order_by('-created_at')
    return render(request, "dashboard/add_training.html", {"trainings": trainings})


def add_training(request):
    if request.method == "POST":
        form = TrainingForm(request.POST)
        if form.is_valid():
            form.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                trainings = Training.objects.order_by('-created_at')
                html = render_to_string("dashboard/_training_list.html", {"trainings": trainings})
                return JsonResponse({"success": True, "html": html})
            else:
                messages.success(request, "Training added successfully.")
                return redirect("dashboard:training_list")
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "errors": form.errors})
            else:
                messages.error(request, "Please correct the errors below.")
    else:
        form = TrainingForm()

    trainings = Training.objects.order_by('-created_at')
    return render(request, "dashboard/add_training.html", {"form": form, "trainings": trainings})
