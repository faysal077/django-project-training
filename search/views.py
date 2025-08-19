from django.shortcuts import render
from django.shortcuts import render
from dashboard.models import Training, Participant
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def search_dashboard(request):
    #return render(request, 'search/_search_dashboard_template.html')
    return render(request, 'basee.html')


from django.shortcuts import render
from django.http import JsonResponse
from dashboard.models import Participant


@login_required
def search_by_name(request):
    participants = []
    participant_name = ''
    searched = False

    if request.method == 'POST':
        participant_name = request.POST.get('participant_name', '').strip()
        searched = True

        if participant_name:
            results = Participant.objects.filter(
                name__icontains=participant_name
            ).select_related('training', 'batch') \
             .values(
                'name',
                'Official_ID',
                'designation',
                'office_address',
                'batch__start_date',
                'batch__end_date',
                'batch__batch_number'
             ).order_by('-batch__start_date')

            # Normalize keys for template
            participants = [
                {
                    'name': r['name'],
                    'Official_ID': r['Official_ID'],
                    'designation': r['designation'],
                    'office_address': r['office_address'],
                    'start_date': r['batch__start_date'],
                    'end_date': r['batch__end_date'],
                    'batch_number': r['batch__batch_number'],
                }
                for r in results
            ]

    return render(request, 'search/search_by_name_template.html', {
        'participants': participants,
        'participant_name': participant_name,
        'searched': searched
    })



'''
def search_by_name(request):
    trainings = []
    name = ''
    searched = False

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        searched = True
        if name:
            trainings = Participant.objects.filter(name__icontains=name).select_related('training', 'batch') \
                .values(
                'training__title',
                'batch__start_date',
                'batch__end_date',
                'batch__batch_number'
            ).order_by('-batch__start_date')

            # Rename field keys to match template expectations
            trainings = [
                {
                    'title': t['training__title'],
                    'start_date': t['batch__start_date'],
                    'end_date': t['batch__end_date'],
                    'batch_number': t['batch__batch_number']
                }
                for t in trainings
            ]

    return render(request, 'search/search_by_name_template.html', {
        'trainings': trainings,
        'name': name,
        'searched': searched,
    })

'''
@login_required
def search_by_training(request):
    participants = []
    training_name = ''
    searched = False

    if request.method == 'POST':
        training_name = request.POST.get('training_name', '').strip()
        searched = True

        if training_name:
            results = Participant.objects.filter(
                training__title__icontains=training_name
            ).select_related('training', 'batch') \
                .values(
                'name',
                'designation',
                'batch__start_date',
                'batch__end_date',
                'batch__batch_number'
            ).order_by('-batch__start_date')

            # Normalize keys for template
            participants = [
                {
                    'name': r['name'],
                    'designation': r['designation'],
                    'start_date': r['batch__start_date'],
                    'end_date': r['batch__end_date'],
                    'batch_number': r['batch__batch_number'],
                } for r in results
            ]

    return render(request, 'search/search_by_training_template.html', {
        'participants': participants,
        'training_name': training_name,
        'searched': searched
    })
@login_required
def search_not_taken(request):
    participants = []
    training_name = ''
    searched = False

    if request.method == 'POST':
        training_name = request.POST.get('training_name', '').strip()
        searched = True

        if training_name:
            # Find the training object (assuming title is unique or using icontains)
            training_qs = Training.objects.filter(title__icontains=training_name)

            if training_qs.exists():
                training = training_qs.first()

                # Get IDs of participants who attended the training
                attended_ids = Participant.objects.filter(training=training).values_list('id', flat=True)

                # Get all participants who did NOT attend this training
                participants = Participant.objects.exclude(id__in=attended_ids)

    return render(request, 'search/search_not_taken_template.html', {
        'participants': participants,
        'training_name': training_name,
        'searched': searched
    })
'''
def search_not_taken(request):
    trainings = []
    name = ''
    searched = False

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        searched = True

        if name:
            # Find all training IDs attended by the participant
            attended_ids = Participant.objects.filter(name__icontains=name).values_list('training_id', flat=True)

            # Get trainings not attended
            trainings = Training.objects.exclude(id__in=attended_ids).order_by('-created_at') \
                .values('title', 'created_at', 'organizer', 'training_type', 'id')  # adjust if needed

            # Optionally: convert created_at to start_date if you have a batch model for that info

    return render(request, 'search/search_not_taken_template.html', {
        'name': name,
        'searched': searched,
        'trainings': trainings,
    })

'''
from django.shortcuts import render
from dashboard.models import Participant

@login_required
def search_by_multiple_trainings(request):
    participants = []
    training_names = ''
    searched = False

    if request.method == 'POST':
        training_names = request.POST.get('training_names', '')
        searched = True
        training_list = [t.strip() for t in training_names.split(',') if t.strip()]

        if training_list:
            results = Participant.objects.filter(
                training__title__in=training_list
            ).select_related('training') \
                .values(
                'name',
                'designation',
                'batch_number',
                'training__title'
            )

            # Normalize keys for template
            participants = [
                {
                    'name': r['name'],
                    'designation': r['designation'],
                    'batch_number': r['batch_number'],
                    'training_name': r['training__title'],
                } for r in results
            ]

    return render(request, 'search/search_by_multiple_template.html', {
        'training_names': training_names,
        'participants': participants,
        'searched': searched
    })
