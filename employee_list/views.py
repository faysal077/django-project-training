from django.shortcuts import render
from django.shortcuts import render
from dashboard.models import Participant
from django.contrib.auth.decorators import login_required


@login_required
def employee_search(request):
    results = []
    search_type = request.GET.get('search_type')
    query = request.GET.get('query')

    if search_type and query:
        if search_type == "name":
            results = Participant.objects.filter(
                name__icontains=query
            ).values("name", "Official_ID")

        elif search_type == "id":
            results = Participant.objects.filter(
                Official_ID__icontains=query
            ).values("name", "Official_ID")

    return render(request, "employee_list/employee_search.html", {
        "results": results,
        "search_type": search_type,
        "query": query
    })

# Create your views here.
