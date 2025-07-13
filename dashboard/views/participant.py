from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from dashboard.models import Training, Batch, Participant
from dashboard.forms import ParticipantForm
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from dashboard.models import Training, Batch, Participant
from dashboard.forms import ParticipantForm
from django.contrib import messages
from django.http import JsonResponse

def list_participants(request, training_id, batch_id):
    training = get_object_or_404(Training, id=training_id)
    batch = get_object_or_404(Batch, id=batch_id)
    participants = Participant.objects.filter(training=training, batch=batch)

    form = ParticipantForm()

    return render(request, "dashboard/list_participants.html", {
        "training": training,
        "batch": batch,
        "participants": participants,
        "form": form,
    })


def add_participant(request, training_id, batch_id, batch_number):
    training = get_object_or_404(Training, id=training_id)
    batch = get_object_or_404(Batch, id=batch_id)

    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            official_id = form.cleaned_data['Official_ID']
            existing = Participant.objects.filter(training_id=training_id, Official_ID=official_id)
            if existing.exists():
                existing_batch = existing.first().batch_number
                messages.warning(request, f"This person is already enrolled in Batch No: {existing_batch}")
            else:
                participant = form.save(commit=False)
                participant.training = training
                participant.batch = batch
                participant.batch_number = batch_number
                participant.total_training_hours = batch.total_training_hours
                participant.save()
                messages.success(request, "Participant added successfully.")
                return redirect('dashboard:participant_list', training_id=training_id, batch_id=batch_id)
    else:
        form = ParticipantForm()

    return render(request, "dashboard/add_participant.html", {
        "form": form,
        "training": training,
        "batch": batch,
        "batch_number": batch_number,
    })


# AJAX-based participant lookup
def search_participant_by_id(request):
    official_id = request.GET.get('Official_ID')
    try:
        participant = Participant.objects.filter(Official_ID=official_id).latest('id')
        return JsonResponse({
            "exists": True,
            "name": participant.name,
            "designation": participant.designation,
            "office_address": participant.office_address,
            "gender": participant.gender,
            "contact": participant.contact,
            "email": participant.email,
            "Official_ID": participant.Official_ID,
        })
    except Participant.DoesNotExist:
        return JsonResponse({"exists": False})
'''
def add_participant(request, training_id, batch_id):
    training = get_object_or_404(Training, pk=training_id)
    batch = get_object_or_404(Batch, pk=batch_id)

    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.training = training
            participant.batch = batch
            participant.batch_number = batch.batch_number
            participant.total_training_hours = batch.total_training_hours or 0

            # Check if already exists
            exists = Participant.objects.filter(
                training=training,
                Official_ID=participant.Official_ID
            ).exists()

            if exists:
                messages.error(request, f"This person is already registered for this training.")
            else:
                participant.save()
                messages.success(request, "Participant added successfully.")
                return redirect('dashboard:list_participants', training_id=training.id, batch_id=batch.id)
    else:
        form = ParticipantForm()

    context = {
        'training': training,
        'batch': batch,
        'form': form,
    }
    return render(request, 'dashboard/participants/add.html', context)
'''

def edit_participant(request, participant_id):
    participant = get_object_or_404(Participant, pk=participant_id)
    training = participant.training
    batch = participant.batch

    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant updated successfully.")
            return redirect('dashboard:list_participants', training_id=training.id, batch_id=batch.id)
    else:
        form = ParticipantForm(instance=participant)

    context = {
        'form': form,
        'participant': participant
    }
    return render(request, 'dashboard/participants/edit.html', context)


def delete_participant(request, participant_id):
    participant = get_object_or_404(Participant, pk=participant_id)
    training_id = participant.training.id
    batch_id = participant.batch.id
    participant.delete()
    messages.success(request, "Participant deleted successfully.")
    return redirect('dashboard:list_participants', training_id=training_id, batch_id=batch_id)
