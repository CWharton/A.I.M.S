import re

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse

from assets.models import Asset


def search(request):
    query_string = ''
    paged_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['id', 'name', 'serial', 'other_serial', 'manufacturer__name', 'model', 'location', 'networks__ipv4_address', 'networks__mac_address', ])

        found_entries = Asset.objects.filter(entry_query).distinct()  # .order_by('-pub_date')

        paginator = Paginator(found_entries, 50)
        page = request.GET.get('page')
        try:
            paged_entries = paginator.page(page)
        except PageNotAnInteger:
            paged_entries = paginator.page(1)
        except EmptyPage:
            paged_entries = paginator.page(paginator.num_pages)

    return render(request, 'search/search.html', {'query_string': query_string, 'found_entries': paged_entries})


def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def some_view(request):
    query_string = request.GET['q']
    entry_query = get_query(query_string, ['model'])

    found_entries = Asset.objects.filter(entry_query).distinct()
    return JsonResponse(found_entries)
