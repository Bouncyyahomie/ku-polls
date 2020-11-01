"""TEST polls app."""
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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


class QuestionDetailViewTests(TestCase):
    """Test the detail page."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future returns a 302 not found."""
        future_question = create_question(question_text='Future question.', days=5, closed=10)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        past_question = create_question(question_text='Past Question.', days=-5, closed=-10)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
