from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Choice, Question
from django.urls import reverse
from django.db.models import F

# Create your views here.
def index(request):
    context = {"latest_question_list":  Question.objects.order_by('-pub_date')[:5]}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

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