"""TEST polls app."""
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


def create_question(question_text, days, closed):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    closed = timezone.now() + datetime.timedelta(days=closed)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=closed)


class QuestionModelTests(TestCase):
    """Test about question polls"""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        close_time = time - datetime.timedelta(days=1)
        future_question = Question(pub_date=time, end_date=close_time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        close_time = time + datetime.timedelta(days=1)
        old_question = Question(pub_date=time, end_date=close_time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        close_time = time
        recent_question = Question(pub_date=time, end_date=close_time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_can_vote_with_old_question(self):
        """can_vote() return False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1)
        close_time = time - datetime.timedelta(days=3)
        old_question = Question(pub_date=time, end_date=close_time)
        self.assertIs(old_question.can_vote(), False)

    def test_can_vote_with_future_question(self):
        """can_vote() return False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        close_time = time - datetime.timedelta(days=1)
        future_question = Question(pub_date=time, end_date=close_time)
        self.assertIs(future_question.can_vote(), False)

    def test_can_vote_with_recent_question(self):
        """can_vote() return True for questions whose pub_date is within last day."""
        time = timezone.now() - datetime.timedelta(days=1)
        close_time = time + datetime.timedelta(days=5)
        recent_question = Question(pub_date=time, end_date=close_time)
        self.assertIs(recent_question.can_vote(), True)

    def test_is_published_with_old_question(self):
        """is_published() return False for question whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1)
        close_time = time + datetime.timedelta(days=1)
        old_question = Question(pub_date=time, end_date=close_time)
        self.assertIs(old_question.is_published(), True)

    def test_is_published_with_future_question(self):
        """is_published() return False for question whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        close_time = time - datetime.timedelta(days=1)
        future_question = Question(pub_date=time, end_date=close_time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_recent_question(self):
        """is_published() return False for question whose pub_date is within last day."""
        time = timezone.now() - datetime.timedelta(days=1)
        close_time = time
        recent_question = Question(pub_date=time, end_date=close_time)
        self.assertIs(recent_question.is_published(), True)


class QuestionIndexViewTests(TestCase):
    """Test the index page."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the index page."""
        create_question(question_text="Past question.", days=-30, closed=-20)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed on the index page."""
        create_question(question_text="Future question.", days=30, closed=20)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions are displayed."""
        create_question(question_text="Past question.", days=-3, closed=-20)
        create_question(question_text="Future question.", days=30, closed=50)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", days=-30, closed=-40)
        create_question(question_text="Past question 2.", days=-5, closed=-7)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


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
