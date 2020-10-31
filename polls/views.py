"""Views for set and manage page."""
from django.contrib.auth import user_logged_out, user_logged_in, user_login_failed
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from mysite.settings import LOGGING
import logging.config

from .models import Question, Choice, Vote

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("polls")


@login_required
def vote(request, question_id):
    """
    For vote choice.

    :param request:
    :param question_id:
    :return:
    """
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    print("current user is", user.id, "login", user.username)
    print("Real name:", user.first_name, user.last_name)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        Vote.objects.update(question=question, choice=selected_choice, user=request.user)
        logger.info(f"user: {user.username} has voting on {get_client_ip(request)} ")
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class IndexView(generic.ListView):
    """For set index page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


@login_required()
def vote_for_poll(request, pk):
    """
    For vote the poll.

    :param request:
    :param pk:
    :return: render detail
    """
    user = request.user
    question = get_object_or_404(Question, pk=pk)
    if question.vote_set.filter(user=user).exists():
        previous_vote = Vote.objects.filter(question=question).filter(user=request.user).first().choice.choice_text
    else:
        previous_vote = "You did not vote yet."
    if not question.can_vote():
        messages.error(request, f'{"You are not allowed to vote this question"}')
        return redirect('polls:index')
    return render(request, 'polls/detail.html', {'question': question, 'previous_vote': previous_vote})


# class DetailView(generic.DetailView): //I change from class base view to method base view.
# model = Question
# template_name = 'polls/detail.html'
# def get_queryset(self):
#     """
#     Excludes any questions that aren't published yet.
#     """
#     return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DeleteView):
    """For set result page."""

    model = Question
    template_name = 'polls/results.html'


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def logged_in_logging(sender, request, user, **kwargs):
    logger.info(f"user: {user.username} has logged in to {get_client_ip(request)}")


@receiver(user_logged_out)
def logged_out_logging(sender, request, user, **kwargs):
    logger.info(f"user: {user.username} has logged out from {get_client_ip(request)} ")


@receiver(user_login_failed)
def logged_in_failed_logging(sender, request, credentials, **kwargs):
    logger.warning(f"user: {request.POST['username']} has login failed with {get_client_ip(request)}")
