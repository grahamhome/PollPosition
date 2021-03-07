from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Choice, Question
from django.urls import reverse
from django.db.models import F
from django.views import generic

# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {"question": question, "error_message": "Please make a valid selection."})
    # Use F-statement to get, update and set value in 1 SQL statement (atomically)
    selected_choice.votes = F("votes") + 1
    selected_choice.save()
    # Prevent data from being posted twice, e.g. via Back button
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))