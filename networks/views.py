from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from assets.models import Asset
from networks.forms import NetworkForm, AssetNetworkForm
from networks.models import Network, AssetNetwork


@login_required
def network_list(request):
    queryset = Network.objects.all().order_by('name')

    paginator = Paginator(queryset, 25)
    page = request.GET.get('page')
    try:
        view_list = paginator.page(page)
    except PageNotAnInteger:
        view_list = paginator.page(1)
    except EmptyPage:
        view_list = paginator.page(paginator.num_pages)

    return render(request, 'network/list.html', {'list': view_list})


@login_required
def network_create(request):
    form = NetworkForm(request.POST or None)

    if request.POST:
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.modified_by = request.user
            item.save()
            return HttpResponseRedirect(reverse('networks:list'))

    return render(request, 'network/post.html', {'form': form})


@login_required
def network_edit(request, network_id=None):
    network = get_object_or_404(Network, pk=network_id)
    if request.POST:
        form = NetworkForm(request.POST, instance=network)
        if form.is_valid():
            network = form.save(commit=False)
            network.modified_by = request.user
            network.save()
            # Message
            messages.success(request, 'Updated network.')
        else:
            messages.warning(request, 'Please correct form errors to proceed.')
    else:
        form = NetworkForm(instance=network)
    return render(request, 'network/post.html', {'network': network, 'form': form})


# Asset network
# ----------------------------------------------------------------------------------------------------
@login_required
def asset_network_create(request, asset_id):
    asset = get_object_or_404(Asset, pk=asset_id)
    form = AssetNetworkForm(request.POST or None)
    form.initial = {'asset': asset}

    if request.POST:
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.modified_by = request.user
            item.save()
            return HttpResponseRedirect(reverse('assets:edit', args=[asset.id]))

    return render(request, 'asset_network/post.html', {'form': form, 'asset': asset})


@login_required
def asset_network_edit(request, asset_network_id=None):
    asset_network = get_object_or_404(AssetNetwork, pk=asset_network_id)
    if request.POST:
        form = AssetNetworkForm(request.POST, instance=asset_network)
        if form.is_valid():
            asset_network = form.save(commit=False)
            asset_network.modified_by = request.user
            asset_network.save()
            # Message
            messages.success(request, 'Updated network.')
            return HttpResponseRedirect(reverse('assets:edit', args=[asset_network.asset.id]))
        else:
            messages.warning(request, 'Please correct form errors to proceed.')
    else:
        form = AssetNetworkForm(instance=asset_network)
    return render(request, 'asset_network/post.html', {'asset_network': asset_network, 'form': form, 'asset': asset_network.asset})
