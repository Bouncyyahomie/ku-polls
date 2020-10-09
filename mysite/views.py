"""Set view default page."""
from django.shortcuts import redirect


def index(request):
    """
    Index request and return to page.
    :param request:
    :return for redirect to index
    """
    return redirect('polls:index')
