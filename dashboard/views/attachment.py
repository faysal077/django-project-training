from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from dashboard.models import Attachment, Batch, Training
from dashboard.forms import AttachmentForm


def list_attachments(request, training_id, batch_id):
    training = get_object_or_404(Training, pk=training_id)
    batch = get_object_or_404(Batch, pk=batch_id)
    attachments = Attachment.objects.filter(batch=batch).order_by('-created_at')

    context = {
        'training': training,
        'batch': batch,
        'attachments': attachments,
        'form': AttachmentForm(),  # To use in modal
    }
    return render(request, 'dashboard/attachments.html', context)


@csrf_exempt
def upload_attachment(request, training_id, batch_id):
    if request.method == 'POST':
        training = get_object_or_404(Training, pk=training_id)
        batch = get_object_or_404(Batch, pk=batch_id)
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.training = training
            attachment.batch = batch
            attachment.save()
            return JsonResponse({'success': True, 'message': 'Attachment uploaded successfully.'})
        return JsonResponse({'success': False, 'message': 'Invalid form data.'})
    return JsonResponse({'success': False, 'message': 'Only POST allowed.'})
