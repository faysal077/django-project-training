from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
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
            return JsonResponse({"success": True, "message": "✅ Financial clearance submitted successfully."})
        else:
            return JsonResponse({"success": False, "message": "❌ Validation failed."})
    else:
        form = FinancialClearanceForm()

    context = {
        'training': training,
        'batch': batch,
        'financial_records': financial_records,
        'form': form,
    }
    return render(request, 'dashboard/finance.html', context)
