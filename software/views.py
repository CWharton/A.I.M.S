from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from assets.models import Asset
from software.forms import SoftwareForm, AssetLicenseForm
from software.models import Software, AssetLicense


@login_required
def software_list(request):
    queryset = Software.objects.all().order_by('name')

    paginator = Paginator(queryset, 25)
    page = request.GET.get('page')
    try:
        view_list = paginator.page(page)
    except PageNotAnInteger:
        view_list = paginator.page(1)
    except EmptyPage:
        view_list = paginator.page(paginator.num_pages)

    return render(request, 'software/list.html', {'list': view_list})


@login_required
def software_create(request):
    form = SoftwareForm(request.POST or None)

    if form.is_valid():
        item = form.save(commit=False)
        item.created_by = request.user
        item.modified_by = request.user
        item.save()
        return HttpResponseRedirect(reverse('software:list'))

    return render(request, 'software/post.html', {"form": form})


@login_required
def software_edit(request, software_id=None):
    software = get_object_or_404(Software, pk=software_id)
    if request.POST:
        form = SoftwareForm(request.POST, instance=software)
        if form.is_valid():
            software = form.save(commit=False)
            software.modified_by = request.user
            software.save()
            # Message
            messages.success(request, 'Updated software.')
            return HttpResponseRedirect(reverse('software:list'))
        else:
            messages.warning(request, 'Please correct form errors to proceed.')
    else:
        form = SoftwareForm(instance=software)
    return render(request, 'software/post.html', {"form": form, "software": software})


@login_required
def software_delete(request, software_id):
    software = get_object_or_404(Software, pk=software_id)
    software.delete()
    return render(request, 'software/list.html', {})


# Manufacturer
# ----------------------------------------------------------------------------------------------------
@login_required
def asset_license_create(request, asset_id):
    asset = get_object_or_404(Asset, pk=asset_id)
    form = AssetLicenseForm(request.POST or None)

    if form.is_valid():
        item = form.save(commit=False)
        item.created_by = request.user
        item.modified_by = request.user
        item.save()
        return HttpResponseRedirect(reverse('assets:edit', args=[asset.id]))

    return HttpResponseRedirect(reverse('assets:edit', args=[asset.id]))


@login_required
def asset_license_delete(request, asset_id, license_id):
    asset = get_object_or_404(Asset, pk=asset_id)
    asset_license = get_object_or_404(AssetLicense, pk=license_id)
    asset_license.delete()

    return HttpResponseRedirect(reverse('assets:edit', args=[asset.id]))
