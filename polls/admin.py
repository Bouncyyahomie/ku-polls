"""Admin page for manage polls."""
from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.StackedInline):
    """For manage choice in admin."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """For manage question in admin."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently', 'is_published', 'can_vote', 'end_date')
    list_filter = ['pub_date', 'end_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
