from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from dashboard.models import Batch, FinancialClearance, Training
from dashboard.forms import FinancialClearanceForm


def financial_clearance_view(request, training_id, batch_id):
    training = get_object_or_404(Training, pk=training_id)
    batch = get_object_or_404(Batch, pk=batch_id)
    financial_records = FinancialClearance.objects.filter(batch=batch).order_by('-created_at')

    if request.method == 'POST':
        form = FinancialClearanceForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.training = training
            record.batch = batch
            record.save()
            messages.success(request, "Financial clearance submitted successfully.")
            return redirect('dashboard:financial_clearance', training_id=training.id, batch_id=batch.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FinancialClearanceForm()

    context = {
        'training': training,
        'batch': batch,
        'financial_records': financial_records,
        'form': form
    }
    return render(request, 'dashboard/finance/clearance.html', context)
