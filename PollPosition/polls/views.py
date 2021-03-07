from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Question

# Create your views here.
def index(request):
    context = {"latest_question_list":  Question.objects.order_by('-pub_date')[:5]}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/question.html", {"question": question})

def results(request, question_id):
    return HttpResponse(f"These are the results of Question {question_id}")

def vote(request, question_id):
    return HttpResponse(f"You're voting on Question {question_id}")