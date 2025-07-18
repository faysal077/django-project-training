from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from dashboard.models import Training, Batch
from dashboard.forms import BatchForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from dashboard.models import Training, Batch
from dashboard.forms import BatchForm


def add_batch(request, training_id):
    training = get_object_or_404(Training, pk=training_id)
    batches = Batch.objects.filter(training=training).order_by('-id')  # ✅ still needed for display

    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            batch = form.save(commit=False)
            batch.training = training

            # ✅ Auto-increment batch_number per training
            last_batch = Batch.objects.filter(training=training).order_by('-batch_number').first()
            batch.batch_number = last_batch.batch_number + 1 if last_batch else 1

            # ✅ Fiscal year calculated from start_date
            start_date = batch.start_date
            if start_date:
                start_year = start_date.year
                start_month = start_date.month
                fiscal_start = start_year if start_month >= 7 else start_year - 1
                batch.fiscal_year = f"{fiscal_start}-{fiscal_start + 1}"

            batch.save()
            messages.success(request, f"✅ Batch #{batch.batch_number} added successfully.")
            return redirect('dashboard:add_batch', training_id=training.id)
        else:
            messages.error(request, "❌ Please correct the errors below.")
    else:
        form = BatchForm()

    return render(request, 'dashboard/add_batch.html', {
        'training': training,
        'form': form,
        'batches': batches  # ✅ Now the batches will be shown again
    })
'''
def add_batch(request, training_id):
    training = get_object_or_404(Training, pk=training_id)

    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            batch = form.save(commit=False)
            batch.training = training

            # Auto-generate batch_number
            last_batch = Batch.objects.filter(training=training).order_by('-batch_number').first()
            batch.batch_number = last_batch.batch_number + 1 if last_batch else 1

            # Calculate fiscal year from start_date
            start_date = batch.start_date
            if start_date:
                start_year = start_date.year
                start_month = start_date.month
                fiscal_start = start_year if start_month >= 7 else start_year - 1
                batch.fiscal_year = f"{fiscal_start}-{fiscal_start + 1}"

            batch.save()
            messages.success(request, f"Batch #{batch.batch_number} added successfully.")
            return redirect('dashboard:add_batch', training_id=training.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BatchForm()

    return render(request, 'dashboard/add_batch.html', {
        'training': training,
        'form': form,
    })

'''
'''
def add_batch(request, training_id):
    training = get_object_or_404(Training, pk=training_id)
    batches = Batch.objects.filter(training_id=training.id).order_by('-id')

    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            batch = form.save(commit=False)
            batch.training = training
            batch.save()
            messages.success(request, "✅ Batch added successfully.")
            return redirect('dashboard:add_batch', training_id=training.id)
        else:
            messages.error(request, "❌ Please correct the errors below.")
    else:
        form = BatchForm()

    context = {
        'training': training,
        'form': form,
        'batches': batches
    }
    return render(request, 'dashboard/add_batch.html', context)
'''

# views/batch.py
from django.shortcuts import render, get_object_or_404
from dashboard.models import Batch, Training

def list_batches(request, training_id):
    training = get_object_or_404(Training, pk=training_id)
    batches = Batch.objects.filter(training_id=training_id).order_by('-id')

    return render(request, 'dashboard/list_batches_partial.html', {
        'training': training,
        'batches': batches
    })

