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


class QuestionModelTests(TestCase):
    """Test about question polls."""

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


