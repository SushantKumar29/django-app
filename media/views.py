from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Media
from .forms import MediaForm


@login_required
def media_list_view(request):
    media_list = Media.objects.filter(user=request.user)
    paginator = Paginator(media_list, 16)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "object_list": page_obj

    }
    return render(request, "media/list.html", context=context)


@login_required
def media_create_view(request):
    form = MediaForm(request.POST or None, request.FILES or None)
    context = {
        "form": form
    }
    if form.is_valid():
        media_obj = form.save(commit=False)
        media_obj.user = request.user
        media_obj.save()
        context = {
            'object': media_obj,
            'form': MediaForm(),
            'created': True
        }
        return redirect(media_obj.get_absolute_url())
    return render(request, "media/create.html", context=context)


def media_search_view(request):
    query_dict = request.GET
    query = query_dict.get('query')
    qs = Media.objects.search(query=query, user=request.user)
    context = {
        "object_list": qs
    }
    return render(request, "media/search.html", context=context)


@login_required
def media_detail_view(request, id=None):
    media_obj = get_object_or_404(Media, id=id, user=request.user)
    form = MediaForm(request.POST or None,
                     request.FILES or None, instance=media_obj)
    print(request.FILES)
    # try:
    #     media_obj = Media.objects.get(id=id)
    # except Media.DoesNotExist:
    #     raise Http404
    # except:
    #     raise Http404
    context = {
        'form': form,
        "object": media_obj,
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Update Success'

    return render(request, "media/detail.html", context=context)
