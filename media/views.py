from codecs import lookup
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Media
from .forms import MediaForm


@login_required
def media_list_view(request):
    qs = Media.objects.all()
    context = {
        "object_list": qs,

    }
    return render(request, "media/list.html", context=context)


@login_required
def media_create_view(request):
    form = MediaForm(request.POST or None, request.FILES or None)
    context = {
        "form": form
    }
    if form.is_valid():
        media_obj = form.save()
        context = {
            'object': media_obj,
            'form': MediaForm(),
            'created': True
        }
        return redirect(media_obj.get_absolute_url)
    return render(request, "media/create.html", context=context)


def media_search_view(request):
    query_dict = request.GET
    query = query_dict.get('query')
    qs = Media.objects.search(query=query)
    context = {
        "object_list": qs
    }
    return render(request, "media/search.html", context=context)


def media_detail_view(request, id=None):
    media_obj = None

    try:
        media_obj = Media.objects.get(id=id)
    except Media.DoesNotExist:
        raise Http404
    except:
        raise Http404
    context = {
        "object": media_obj,
    }

    return render(request, "media/detail.html", context=context)
