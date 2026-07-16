from django.shortcuts import redirect, render
from django.shortcuts import render
from dashboard.models import Participant
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
@login_required
def employee_search(request):
    results = []
    search_type = request.GET.get('search_type')
    query = request.GET.get('query')

    if search_type and query:
        if search_type == "name":
            results = Participant.objects.filter(
                name__icontains=query
            ).values(
                "id",
                "name",
                "Official_ID",
                "designation",
                "office_address",
                "contact",
                "training__title",
                "batch__batch_number",
            )

        elif search_type == "id":
            results = Participant.objects.filter(
                Official_ID__icontains=query
            ).values(
                "id",
                "name",
                "Official_ID",
                "designation",
                "office_address",
                "contact",
                "training__title",
                "batch__batch_number",
            )

    return render(request, "employee_list/employee_search.html", {
        "results": results,
        "search_type": search_type,
        "query": query
    })

# Create your views here.
@login_required
def employee_edit(request, pk):

    participant = get_object_or_404(
        Participant,
        pk=pk
    )

    if request.method == "POST":

        participant.name = request.POST["name"]
        participant.designation = request.POST["designation"]
        participant.office_address = request.POST["office_address"]
        participant.contact = request.POST["contact"]
        participant.save()

        return redirect("employee_list:home")

    return render(
        request,
        "employee_list/employee_edit.html",
        {
            "participant": participant
        }
    )