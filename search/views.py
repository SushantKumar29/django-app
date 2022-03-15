from django.shortcuts import render
from media.models import Media
from django.core.paginator import Paginator


SEARCH_TYPE_MAPPING = {
    'medias': Media,
    'media': Media,
}


def search_view(request, *args, **kwargs):
    query = request.GET.get('query')
    Klass = Media
    media_list = Klass.objects.search(query=query)
    paginator = Paginator(media_list, 16)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'object_list': page_obj,
    }
    template = 'search/results_view.html'
    return render(request, template, context)
