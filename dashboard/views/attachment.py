from django.shortcuts import render, redirect, get_object_or_404
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
    }
    return render(request, 'dashboard/attachments/list.html', context)


def upload_attachment(request, training_id, batch_id):
    training = get_object_or_404(Training, pk=training_id)
    batch = get_object_or_404(Batch, pk=batch_id)

    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.training = training
            attachment.batch = batch
            attachment.save()
            messages.success(request, 'Attachment uploaded successfully.')
            return redirect('dashboard:list_attachments', training_id=training_id, batch_id=batch_id)
        else:
            messages.error(request, 'Failed to upload attachment. Please check the form.')
    else:
        form = AttachmentForm()

    context = {
        'form': form,
        'training': training,
        'batch': batch,
    }
    return render(request, 'dashboard/attachments/upload.html', context)
