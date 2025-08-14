# from django.shortcuts import render
# from dashboard.models import Training, Participant, FinancialClearance
# from django.db.models import Q, Count, Sum
# from django.utils.safestring import mark_safe
# import json
# from django.contrib.auth.decorators import login_required
#
# @login_required
# def dashboard_view(request):
#     current_fiscal_year = "2024-2025"
#
#     # Total counts
#     total_trainings = Training.objects.count()
#     total_participants = Participant.objects.count()
#
#     # Fiscal year-specific counts
#     trainings_this_year = Training.objects.filter(batches__fiscal_year=current_fiscal_year).distinct().count()
#     participants_this_year = Participant.objects.filter(batch__fiscal_year=current_fiscal_year).count()
#
#     # Expenses
#     total_expenses = FinancialClearance.objects.aggregate(
#         total=Sum('amount_spent')
#     )['total'] or 0
#
#     expenses_this_year = FinancialClearance.objects.filter(
#         batch__fiscal_year=current_fiscal_year
#     ).aggregate(total=Sum('amount_spent'))['total'] or 0
#
#     # Participant chart data (prepare arrays for chart.js / ApexCharts)
#     raw_participant_data = (
#         Participant.objects
#         .values('batch__fiscal_year')
#         .annotate(
#             total=Count('id'),
#             male=Count('id', filter=Q(gender='Male')),
#             female=Count('id', filter=Q(gender='Female'))
#         )
#         .order_by('batch__fiscal_year')
#     )
#
#     participant_years = [item['batch__fiscal_year'] for item in raw_participant_data]
#     total_participant_counts = [item['total'] for item in raw_participant_data]
#     male_counts = [item['male'] for item in raw_participant_data]
#     female_counts = [item['female'] for item in raw_participant_data]
#
#     # Financial chart data
#     raw_financial_data = (
#         FinancialClearance.objects
#         .values('batch__fiscal_year')
#         .annotate(total=Sum('amount_spent'))
#         .order_by('batch__fiscal_year')
#     )
#
#     financial_years = [item['batch__fiscal_year'] for item in raw_financial_data]
#     financial_spending = [float(item['total'] or 0) for item in raw_financial_data]
#
#     context = {
#         # Numeric boxes
#         "total_trainings": total_trainings,
#         "trainings_this_year": trainings_this_year,
#         "total_participants": total_participants,
#         "participants_this_year": participants_this_year,
#         "total_expenses": total_expenses,
#         "expenses_this_year": expenses_this_year,
#
#         # Chart data (serialized as JSON-safe strings)
#         "participant_years": mark_safe(json.dumps(participant_years)),
#         "participant_total": mark_safe(json.dumps(total_participant_counts)),
#         "participant_male": mark_safe(json.dumps(male_counts)),
#         "participant_female": mark_safe(json.dumps(female_counts)),
#
#         "financial_years": mark_safe(json.dumps(financial_years)),
#         "financial_spent": mark_safe(json.dumps(financial_spending)),
#     }
#
#     return render(request, "dashboard/index.html", context)

################
### WORKED ###
################
# from django.shortcuts import render
# from django.db.models import Q, Count, Sum
# from dashboard.models import Training, Participant, FinancialClearance, Batch
#
# def dashboard_view(request):
#     fiscal_year_filter = request.GET.get("fiscal_year", "All")
#
#     fiscal_years = [
#         "All",
#         "2020-2021",
#         "2021-2022",
#         "2023-2024",
#         "2024-2025",
#         "2025-2026",
#     ]
#
#     # Base Querysets
#     trainings_qs = Training.objects.all()
#     participants_qs = Participant.objects.all()
#     expenses_qs = FinancialClearance.objects.all()
#
#     # Apply Fiscal Year Filter if selected
#     if fiscal_year_filter != "All":
#         trainings_qs = trainings_qs.filter(batches__fiscal_year=fiscal_year_filter).distinct()
#         participants_qs = participants_qs.filter(batch__fiscal_year=fiscal_year_filter)
#         expenses_qs = expenses_qs.filter(batch__fiscal_year=fiscal_year_filter)
#
#     context = {
#         "fiscal_years": fiscal_years,
#         "selected_year": fiscal_year_filter,
#         "total_trainings": trainings_qs.count(),
#         "total_participants": participants_qs.count(),
#         "total_expenses": expenses_qs.aggregate(total=Sum('amount_spent'))['total'] or 0,
#         "total_batches": Batch.objects.filter(
#             fiscal_year=fiscal_year_filter if fiscal_year_filter != "All" else None
#         ).count() if fiscal_year_filter != "All" else Batch.objects.count()
#     }
#
#     return render(request, "dashboard/index.html", context)

# dashboard/views.py
######################################################################################
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

# Dashboard page
def dashboard_view(request):
    fiscal_years = [
        "All",
        "2025-2026",
        "2024-2025",
        "2023-2024",
        "2022-2023",
        "2021-2022",
    ]
    return render(request, "dashboard/index.html", {"fiscal_years": fiscal_years})


# API for cards
def dashboard_data(request):
    fiscal_year = request.GET.get("fiscal_year", "All")

    batches = Batch.objects.all()
    trainings = Training.objects.all()
    participants = Participant.objects.all()
    expenses = FinancialClearance.objects.all()

    if fiscal_year != "All":
        batches = batches.filter(fiscal_year=fiscal_year)
        trainings = trainings.filter(batches__fiscal_year=fiscal_year).distinct()
        participants = participants.filter(batch__fiscal_year=fiscal_year)
        expenses = expenses.filter(batch__fiscal_year=fiscal_year)

    cards = {
        "trainings": trainings.count(),
        "batches": batches.count(),
        "participants": participants.count(),
        "expenses": expenses.aggregate(total=Sum("amount_spent"))["total"] or 0,
    }

    return JsonResponse({"cards": cards})


# API for charts
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


######################################################################################
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.db.models import Count, Sum, Q
# from dashboard.models import Training, Participant, FinancialClearance, Batch
#
# def dashboard_view(request):
#     # Fiscal year dropdown list
#     fiscal_years = [
#         "All",
#         "2025-2026",
#         "2024-2025",
#         "2023-2024",
#         "2022-2023",
#         "2021-2022",
#     ]
#
#     # === CHART DATA (all fiscal years) ===
#     participant_chart = (
#         Participant.objects.values("batch__fiscal_year")
#         .annotate(
#             total=Count("id"),
#             male=Count("id", filter=Q(gender="Male")),
#             female=Count("id", filter=Q(gender="Female")),
#         )
#         .order_by("batch__fiscal_year")
#     )
#
#     financial_chart = (
#         FinancialClearance.objects.values("batch__fiscal_year")
#         .annotate(total_spent=Sum("amount_spent"))
#         .order_by("batch__fiscal_year")
#     )
#
#     training_chart = (
#         Batch.objects.values("fiscal_year")
#         .annotate(total_trainings=Count("training", distinct=True))
#         .order_by("fiscal_year")
#     )
#
#     batch_chart = (
#         Batch.objects.values("fiscal_year")
#         .annotate(total_batches=Count("id"))
#         .order_by("fiscal_year")
#     )
#
#     context = {
#         "fiscal_years": fiscal_years,
#
#         # Participants
#         "participant_years": [d["batch__fiscal_year"] for d in participant_chart],
#         "participant_total": [d["total"] for d in participant_chart],
#         "participant_male": [d["male"] for d in participant_chart],
#         "participant_female": [d["female"] for d in participant_chart],
#
#         # Financials
#         "financial_years": [d["batch__fiscal_year"] for d in financial_chart],
#         "financial_spent": [d["total_spent"] or 0 for d in financial_chart],
#
#         # Trainings
#         "training_years": [d["fiscal_year"] for d in training_chart],
#         "training_counts": [d["total_trainings"] for d in training_chart],
#
#         # Batches
#         "batch_years": [d["fiscal_year"] for d in batch_chart],
#         "batch_counts": [d["total_batches"] for d in batch_chart],
#     }
#     return render(request, "dashboard/index.html", context)
#
#
# def dashboard_data(request):
#     fiscal_year = request.GET.get("fiscal_year", "All")
#
#     # === CARD DATA (filtered by fiscal year) ===
#     batches = Batch.objects.all()
#     trainings = Training.objects.all()
#     participants = Participant.objects.all()
#     expenses = FinancialClearance.objects.all()
#
#     if fiscal_year != "All":
#         batches = batches.filter(fiscal_year=fiscal_year)
#         trainings = trainings.filter(batches__fiscal_year=fiscal_year).distinct()
#         participants = participants.filter(batch__fiscal_year=fiscal_year)
#         expenses = expenses.filter(batch__fiscal_year=fiscal_year)
#
#     cards = {
#         "trainings": trainings.count(),
#         "batches": batches.count(),
#         "participants": participants.count(),
#         "expenses": expenses.aggregate(total=Sum("amount_spent"))["total"] or 0,
#     }
#
#     return JsonResponse({"cards": cards})
#
#
# from django.db.models import Count, Sum, Q, F, Value
# from django.db.models.functions import Coalesce
#
# def dashboard_charts(request):
#     # === Participant Chart ===
#     participant_chart = (
#         Participant.objects
#         .values(fiscal_year=Coalesce("batch__fiscal_year", Value("N/A")))
#         .annotate(
#             total=Count("id"),
#             male=Count("id", filter=Q(gender="Male")),
#             female=Count("id", filter=Q(gender="Female")),
#         )
#         .order_by("fiscal_year")
#     )
#
#     # === Financial Chart ===
#     financial_chart = (
#         FinancialClearance.objects
#         .values(fiscal_year=Coalesce("batch__fiscal_year", Value("N/A")))
#         .annotate(total_spent=Coalesce(Sum("amount_spent"), 0))
#         .order_by("fiscal_year")
#     )
#
#     # === Trainings Chart ===
#     training_chart = (
#         Batch.objects
#         .values(fiscal_year=Coalesce("fiscal_year", Value("N/A")))
#         .annotate(total_trainings=Count("training", distinct=True))
#         .order_by("fiscal_year")
#     )
#
#     # === Batches Chart ===
#     batch_chart = (
#         Batch.objects
#         .values(fiscal_year=Coalesce("fiscal_year", Value("N/A")))
#         .annotate(total_batches=Count("id"))
#         .order_by("fiscal_year")
#     )
#
#     return JsonResponse({
#         "participants": {
#             "years": [d["fiscal_year"] for d in participant_chart],
#             "total": [d["total"] for d in participant_chart],
#             "male": [d["male"] for d in participant_chart],
#             "female": [d["female"] for d in participant_chart],
#         },
#         "financials": {
#             "years": [d["fiscal_year"] for d in financial_chart],
#             "spent": [float(d["total_spent"]) for d in financial_chart],  # convert Decimal to float
#         },
#         "trainings": {
#             "years": [d["fiscal_year"] for d in training_chart],
#             "counts": [d["total_trainings"] for d in training_chart],
#         },
#         "batches": {
#             "years": [d["fiscal_year"] for d in batch_chart],
#             "counts": [d["total_batches"] for d in batch_chart],
#         },
#     })