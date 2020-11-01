"""TEST can vote in polls app."""
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from polls.models import Question


def create_question(question_text, days, closed):
    """
    Create a question with the given `question_text`.

    And published the given number of `days` offset to now
    (negative for questions published in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    closed = timezone.now() + datetime.timedelta(days=closed)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=closed)


class VotingTests(TestCase):
    """Test with voting"""

    def test_only_login_can_vote(self):
        user = User.objects.create_user(username='lilslimethug', password='12345678', email='eelonino@gmail.com')
        question = create_question(question_text='vote me', days=1, closed=40)
        choice = question.choice_set.create(choice_text="check")
        response = self.client.post(reverse('login'), {'username': 'lilslimethug', 'password': '12345678'}, follow=True)
        question.vote_set.create(user=user, question=question, choice=choice)
        self.assertEqual(response.status_code, 200)

    def test_not_login_can_not_vote(self):
        user = User.objects.create_user(username='lilslimethug', password='12345678', email='eelonino@gmail.com')
        question = create_question(question_text='vote me', days=1, closed=40)
        choice = question.choice_set.create(choice_text="check")
        question.vote_set.create(user=user, question=question, choice=choice)
        url = reverse("polls:detail", args=(question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)