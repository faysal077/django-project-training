from dashboard.models import Training
from dashboard.forms import TrainingForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required

# def list_trainings(request):
#     trainings = Training.objects.order_by('-created_at')
#     return render(request, "dashboard/add_training.html", {"trainings": trainings})

def list_trainings(request):
    trainings = Training.objects.filter(
        created_by=request.user
    ).order_by('-created_at')

    return render(
        request,
        "dashboard/add_training.html",
        {"trainings": trainings}
    )


@login_required
def add_training(request):
    if request.method == "POST":
        form = TrainingForm(request.POST)
        if form.is_valid():
            training = form.save(commit=False)
            training.created_by = request.user
            training.save()

            messages.success(request, "Training added successfully")
            return redirect('dashboard:add_training')

        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "errors": form.errors})
            else:
                messages.error(request, "Please correct the errors below.")

    else:
        form = TrainingForm()

        # ✅ FILTERING LOGIC (THIS WAS MISSING)
        # trainings = Training.objects.order_by('-created_at')
        trainings = Training.objects.filter(
            created_by=request.user
        ).order_by('-created_at')

        title = request.GET.get("title")
        training_type = request.GET.get("training_type")

        if title:
            trainings = trainings.filter(title__icontains=title)

        if training_type:
            trainings = trainings.filter(training_type=training_type)

        return render(
            request,
            "dashboard/add_training.html",
            {
                "form": form,
                "trainings": trainings
            }
    )



# 🔹 UPDATE TRAINING
@login_required
def update_training(request, training_id):
    # training = get_object_or_404(Training, id=training_id)
    training = get_object_or_404(
        Training,
        id=training_id,
        created_by=request.user
    )

    if request.method == "POST":
        form = TrainingForm(request.POST, instance=training)
        if form.is_valid():
            training = form.save(commit=False)
            # training.owner = request.user
            training.created_by = request.user
            training.save()
            messages.success(request, "✅ Training updated successfully")
            return redirect("dashboard:training_list")
    else:
        form = TrainingForm(instance=training)

    return render(request, "dashboard/update_training.html", {
        "form": form,
        "training": training
    })


# 🔹 DELETE TRAINING
@login_required
def delete_training(request, training_id):
    # training = get_object_or_404(Training, id=training_id)
    training = get_object_or_404(
        Training,
        id=training_id,
        created_by=request.user
    )

    if request.method == "POST":
        training.delete()
        messages.success(request, "🗑 Training deleted successfully")
        return redirect("dashboard:training_list")

    return render(request, "dashboard/confirm_delete.html", {
        "object": training,
        "type": "Training"
    })
