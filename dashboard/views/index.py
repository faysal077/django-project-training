from django.shortcuts import render
from dashboard import models
from dashboard.models import Training, Participant, FinancialClearance
from django.db.models import Q, Count, Sum


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

    # Participant chart data
    participant_chart_data = (
        Participant.objects
        .values('batch__fiscal_year')
        .annotate(
            total_participants=Count('id'),
            male_participants=Count('id', filter=Q(gender='Male')),
            female_participants=Count('id', filter=Q(gender='Female'))
        )
        .order_by('batch__fiscal_year')
    )

    # Financial chart data
    financial_chart_data = (
        FinancialClearance.objects
        .values('batch__fiscal_year')
        .annotate(total_spent=Sum('amount_spent'))
        .order_by('batch__fiscal_year')
    )

    context = {
        "total_trainings": total_trainings,
        "trainings_this_year": trainings_this_year,
        "total_participants": total_participants,
        "participants_this_year": participants_this_year,
        "total_expenses": total_expenses,
        "expenses_this_year": expenses_this_year,
        "participant_chart_data": list(participant_chart_data),
        "financial_chart_data": list(financial_chart_data),
    }

    return render(request, "dashboard/index.html", context)
