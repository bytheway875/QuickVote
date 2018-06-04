from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
# from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Question, Choice

# def index(request):
#     latest_questions = Question.objects.order_by('-pub_date')[:5]
#
#     # Longer form using template + HttpResponse directly
#     # context = {
#     #     'latest_questions': latest_questions
#     # }
#     # template = loader.get_template('polls/index.html')
#     # return HttpResponse(template.render(context, request))
#
#     # Shorter form using shortcuts
#     return render(request, 'polls/index.html', {
#         'latest_questions': latest_questions
#     })

class IndexView(generic.ListView):
    template_name = 'polls/index.html' # by default, looks for 'polls/question_list.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# def show(request, question_id):
#     # Longer form using try/except directly
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#
#     # short form ...
#     # get_list_or_404 will use .filter
#     # get_object_or_404 uses .get
#     question = get_object_or_404(Question, pk=question_id)
#
#     return render(request, 'polls/show.html', {
#         'question': question,
#     })

class ShowView(generic.DetailView):
    model = Question
    template_name = 'polls/show.html' # by default, looks for 'polls/question_detail.html'

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {
#         'question': question
#     })

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html' # by default, looks for 'polls/question_detail.html'

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
        selection.votes = F('votes') + 1 # F() generates a SQL expression
        selection.save()
        selection.refresh_from_db()

        # After dealing with POST data, use HttpResponseRedirect.
        # This prevents data from being posted twice if a user hits the back button.
        # reverse() allows us to build a url similar to in the tempalte.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
