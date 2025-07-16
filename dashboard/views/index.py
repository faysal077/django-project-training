from django.shortcuts import render
from dashboard.models import Training, Participant, FinancialClearance
from django.db.models import Q, Count, Sum
from django.utils.safestring import mark_safe
import json

def dashboard_view(request):
    current_fiscal_year = "2024-2025"

    # Total counts
    total_trainings = Training.objects.count()
    total_participants = Participant.objects.count()

    # Fiscal year-specific counts
    trainings_this_year = Training.objects.filter(batches__fiscal_year=current_fiscal_year).distinct().count()
    participants_this_year = Participant.objects.filter(batch__fiscal_year=current_fiscal_year).count()

    # Expenses
    total_expenses = FinancialClearance.objects.aggregate(
        total=Sum('amount_spent')
    )['total'] or 0

    expenses_this_year = FinancialClearance.objects.filter(
        batch__fiscal_year=current_fiscal_year
    ).aggregate(total=Sum('amount_spent'))['total'] or 0

    # Participant chart data (prepare arrays for chart.js / ApexCharts)
    raw_participant_data = (
        Participant.objects
        .values('batch__fiscal_year')
        .annotate(
            total=Count('id'),
            male=Count('id', filter=Q(gender='Male')),
            female=Count('id', filter=Q(gender='Female'))
        )
        .order_by('batch__fiscal_year')
    )

    participant_years = [item['batch__fiscal_year'] for item in raw_participant_data]
    total_participant_counts = [item['total'] for item in raw_participant_data]
    male_counts = [item['male'] for item in raw_participant_data]
    female_counts = [item['female'] for item in raw_participant_data]

    # Financial chart data
    raw_financial_data = (
        FinancialClearance.objects
        .values('batch__fiscal_year')
        .annotate(total=Sum('amount_spent'))
        .order_by('batch__fiscal_year')
    )

    financial_years = [item['batch__fiscal_year'] for item in raw_financial_data]
    financial_spending = [float(item['total'] or 0) for item in raw_financial_data]

    context = {
        # Numeric boxes
        "total_trainings": total_trainings,
        "trainings_this_year": trainings_this_year,
        "total_participants": total_participants,
        "participants_this_year": participants_this_year,
        "total_expenses": total_expenses,
        "expenses_this_year": expenses_this_year,

        # Chart data (serialized as JSON-safe strings)
        "participant_years": mark_safe(json.dumps(participant_years)),
        "participant_total": mark_safe(json.dumps(total_participant_counts)),
        "participant_male": mark_safe(json.dumps(male_counts)),
        "participant_female": mark_safe(json.dumps(female_counts)),

        "financial_years": mark_safe(json.dumps(financial_years)),
        "financial_spent": mark_safe(json.dumps(financial_spending)),
    }

    return render(request, "dashboard/index.html", context)
