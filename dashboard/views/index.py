from django.shortcuts import render
# from urllib3 import request
from dashboard.models import Training, Participant, FinancialClearance
from django.db.models import Q, Count, Sum
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Sum, Q, Value
from django.db.models.functions import Coalesce
from dashboard.models import Training, Batch, Participant, FinancialClearance

# Dashboard page
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Sum, Q, Value
from django.db.models.functions import Coalesce
from dashboard.models import Training, Batch, Participant, FinancialClearance
from django.db.models import DecimalField
from django.db.models import Sum

# trainings = Training.objects.filter(
#     created_by=request.user
# )

# batches = Batch.objects.filter(
#     training__created_by=request.user
# )

# participants = Participant.objects.filter(
#     training__created_by=request.user
# )

# expenses = FinancialClearance.objects.filter(
#     training__created_by=request.user
# )


@login_required
# Dashboard page
def dashboard_view(request):
    fiscal_years = [
        "All",
        "2026-2027",
        "2025-2026",
        "2024-2025",
        "2023-2024",
        "2022-2023",
        "2021-2022",
    ]
    return render(request, "dashboard/index.html", {"fiscal_years": fiscal_years})


# API for cards
@login_required
def dashboard_data(request):
    fiscal_year = request.GET.get("fiscal_year", "All")

    # batches = Batch.objects.all()
    # trainings = Training.objects.all()
    # participants = Participant.objects.all()
    # expenses = FinancialClearance.objects.all()

    batches = Batch.objects.filter(
        training__created_by=request.user
    )

    trainings = Training.objects.filter(
        created_by=request.user
    )

    participants = Participant.objects.filter(
        training__created_by=request.user
    )

    expenses = FinancialClearance.objects.filter(
        training__created_by=request.user
    )

    if fiscal_year != "All":
        batches = batches.filter(fiscal_year=fiscal_year)
        trainings = trainings.filter(batches__fiscal_year=fiscal_year).distinct()
        participants = participants.filter(batch__fiscal_year=fiscal_year)
        expenses = expenses.filter(batch__fiscal_year=fiscal_year)

    cards = {
        "trainings": trainings.count(),
        "batches": batches.count(),
        "participants": participants.count(),
        "expenses": expenses.aggregate(
            total=Sum("amount_spent")
        )["total"] or 0,
    }

    return JsonResponse({"cards": cards})


# API for charts
@login_required
def dashboard_charts(request):
    # === Participant Chart ===
    participant_chart = (
        Participant.objects
        .values(fy=Coalesce("batch__fiscal_year", Value("N/A")))
        .annotate(
            total=Count("id"),
            male=Count("id", filter=Q(gender="Male")),
            female=Count("id", filter=Q(gender="Female")),
        )
        .order_by("fy")
    )

    # === Financial Chart ===
    financial_chart = (
        FinancialClearance.objects
        .values(fy=Coalesce("batch__fiscal_year", Value("N/A")))
        .annotate(total_spent=Coalesce(Sum("amount_spent"), Value(0), output_field=DecimalField()))
        .order_by("fy")
    )

    # === Trainings Chart ===
    training_chart = (
        Batch.objects
        .values(fy=Coalesce("fiscal_year", Value("N/A")))
        .annotate(total_trainings=Count("training", distinct=True))
        .order_by("fy")
    )

    # === Batches Chart ===
    batch_chart = (
        Batch.objects
        .values(fy=Coalesce("fiscal_year", Value("N/A")))
        .annotate(total_batches=Count("id"))
        .order_by("fy")
    )

    return JsonResponse({
        "participants": {
            "years": [d["fy"] for d in participant_chart],
            "total": [d["total"] for d in participant_chart],
            "male": [d["male"] for d in participant_chart],
            "female": [d["female"] for d in participant_chart],
        },
        "financials": {
            "years": [d["fy"] for d in financial_chart],
            "spent": [float(d["total_spent"]) for d in financial_chart],
        },

        "trainings": {
            "years": [d["fy"] for d in training_chart],
            "counts": [d["total_trainings"] for d in training_chart],
        },
        "batches": {
            "years": [d["fy"] for d in batch_chart],
            "counts": [d["total_batches"] for d in batch_chart],
        },
    })


