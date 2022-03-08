from django.http import HttpResponse
from django.template.loader import render_to_string


def home_view(request):
    HTML_STRING = render_to_string("home_view.html", context={})

    # Send response
    return HttpResponse(HTML_STRING)
