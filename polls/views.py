from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.urls import reverse
from .models import Question, Choice

def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]

    # Longer form using template + HttpResponse directly
    # context = {
    #     'latest_questions': latest_questions
    # }
    # template = loader.get_template('polls/index.html')
    # return HttpResponse(template.render(context, request))

    # Shorter form using shortcuts
    return render(request, 'polls/index.html', {
        'latest_questions': latest_questions
    })

def show(request, question_id):
    # Longer form using try/except directly
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")

    # short form ...
    # get_list_or_404 will use .filter
    # get_object_or_404 uses .get
    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'polls/show.html', {
        'question': question,
    })

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {
        'question': question
    })

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selection = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/show.html', {
            'question': question,
            'error_message': 'Please select an answer choice.'
        })
    else:
        selection.votes += 1
        selection.save()

        # After dealing with POST data, use HttpResponseRedirect.
        # This prevents data from being posted twice if a user hits the back button.
        # reverse() allows us to build a url similar to in the tempalte.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
