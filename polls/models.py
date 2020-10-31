"""Manage models question and choice."""
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Class for set and save question."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date close')

    def __str__(self):
        """:return question text."""
        return self.question_text

    def was_published_recently(self):
        """
        For get to know that the question was just published.

        :return: recently date
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """
        For get to know that the question is published.

        :return:
        """
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """
        For know that the question can vote.

        :return:
        """
        now = timezone.now()
        return self.end_date >= now >= self.pub_date

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    is_published.boolean = True
    is_published.short_description = 'Is published?'

    can_vote.boolean = True
    can_vote.short_description = 'Can vote?'


class Choice(models.Model):
    """For set question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        For show choice text.

        :return: text choice
        """
        return self.choice_text


class Vote(models.Model):
    """For save the user vote from question"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

