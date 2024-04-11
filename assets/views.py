import datetime
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from assets.forms import ManufacturerForm, StatusForm, TypeForm, SubTypeForm, AssetTypeForm, NoteForm, \
    AssetCheckInForm, AssetSafeForm, AssetChangeForm, AssetCreateForm, AssetDeleteForm
from assets.models import Asset, Manufacturer, Status, Type, SubType, AssetChangeLog, AssetCheckIn, PrintQueue
from software.forms import AssetLicenseForm


@login_required
def asset_create(request):
    form = AssetTypeForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            return HttpResponseRedirect('/assets/create/' + request.POST['type'].lower())
        messages.error(request, 'Select a valid Asset Type')
    return render(request, 'assets/select_type.html', {"asset": None, "form": form})


@login_required
def asset_create_by_type(request, list_type=None):
    asset_type = Type.objects.filter(name__iexact=list_type)[0:1].get()
    if asset_type is None:
        return HttpResponseRedirect(reverse('assets:create'))
    form = AssetCreateForm(list_type, request.POST or None)
    form.initial = {'type': asset_type}

    if form.is_valid():
        asset = form.save(commit=False)
        asset.created_by = request.user
        asset.modified_by = request.user
        asset.save()
        # Log event
        log_asset_event(request, asset, 'Asset created')
        return HttpResponseRedirect(reverse('assets:edit', args=[asset.id]))

    return render(request, 'assets/create.html', {"asset": None, "form": form, "asset_type": asset_type})


@login_required
def asset_edit(request, asset_id=None):
    asset = get_object_or_404(Asset, pk=asset_id)
    networks = asset.networks.all().order_by('name')
    licenses = asset.licenses.all()
    notes = asset.notes.all()
    log = asset.change_log.all()

    if request.POST:
        form_safe = AssetSafeForm(asset.type.name, request.POST, instance=asset)
        form_change = AssetChangeForm(request.POST, instance=asset)
        if form_safe.is_valid() and form_change.is_valid():
            asset = form_change.save(commit=False)
            asset_safe = form_safe.save(commit=False)

            asset.type = asset_safe.type
            asset.sub_type = asset_safe.sub_type
            asset.manufacturer = asset_safe.manufacturer
            asset.model = asset_safe.model
            asset.serial = asset_safe.serial
            asset.other_serial = asset_safe.other_serial
            asset.inventory_number = asset_safe.inventory_number
            asset.purchased = asset_safe.purchased

            asset.modified_by = request.user
            asset.save()
            # Log event
            log_asset_event(request, asset, 'Asset updated')
            # Message
            messages.success(request, 'Updated asset.')
        else:
            messages.warning(request, 'Please correct form errors to proceed.')
    else:
        form_safe = AssetSafeForm(asset.type.name, instance=asset)
        form_change = AssetChangeForm(instance=asset)

    form_note = NoteForm()
    form_note.initial = {'asset': asset}
    form_license = AssetLicenseForm()
    form_license.initial = {'asset': asset}

    site_url = os.getenv('APP_URL', "http://aims.killeenauto.local")

    return render(request, 'assets/post.html',
                  {'asset': asset,
                   'form': form_safe,
                   'form_change': form_change,
                   'form_note': form_note,
                   'form_license': form_license,
                   'networks': networks,
                   'connections': [],
                   'licenses': licenses,
                   'notes': notes,
                   'log': log,
                   'check_url': site_url + "/assets/" + str(asset.id) + "/checkin/"}
                  )


@login_required
def asset_check_in(request, asset_id=None):
    asset = get_object_or_404(Asset, pk=asset_id)
    networks = asset.networks.all().order_by('name')

    if request.POST:
        form = AssetCheckInForm(request.POST, instance=asset)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.modified_by = request.user
            asset.save()
            # Log event
            log_asset_event(request, asset, 'Asset status/location updated')
            # Message
            messages.success(request, 'Updated asset.')
        else:
            messages.warning(request, 'Please correct form errors to proceed.')
    else:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # ip = get_client_ip(request)
        # ip = request.ip
        form = AssetCheckInForm(instance=asset)
        log = AssetCheckIn(asset=asset, ip=ip, created_by=request.user)
        log.save()

    form_note = NoteForm()
    form_note.initial = {'asset': asset}
    return render(request, 'assets/check_in.html',
                  {'asset': asset, 'networks': networks, 'form': form, 'form_note': form_note, })


@login_required
def shelf(request, asset_id=None):
    asset = get_object_or_404(Asset, pk=asset_id)
    status = get_object_or_404(Status, pk=2)

    asset.location = "I.T. Office"
    asset.status = status
    asset.save()

    networks = asset.networks.all()
    for network in networks:
        network.ipv4_address = ""
        network.save()

    messages.success(request, 'Asset shelved.')
    return redirect('assets:check-in', asset_id)


@login_required
def asset_list(request, list_type=None):
    if list_type is None:
        queryset = Asset.objects.exclude(decommissioned__isnull=False).all().order_by('name')
    else:
        queryset = Asset.objects.filter(type__name__iexact=list_type).exclude(
            decommissioned__isnull=False).all().order_by('name')

    paginator = Paginator(queryset, 25)
    page = request.GET.get('page')
    try:
        view_list = paginator.page(page)
    except PageNotAnInteger:
        view_list = paginator.page(1)
    except EmptyPage:
        view_list = paginator.page(paginator.num_pages)

    return render(request, 'assets/list.html', {'list_type': list_type, 'list': view_list})


@login_required
def asset_delete(request, asset_id):
    asset = get_object_or_404(Asset, pk=asset_id)

    if request.POST:
        form = AssetDeleteForm(request.POST, instance=asset)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.decommissioned = datetime.date.today()
            asset.decommissioned_by = request.user
            asset.save()
            # Log event
            log_asset_event(request, asset, 'Asset decommissioned')
            # Message
            messages.success(request, 'Asset successfully decommissioned.')
            return HttpResponseRedirect(reverse('assets:edit', args=[asset_id]))
        else:
            messages.warning(request, 'Please correct form errors to proceed.')
    else:
        form = AssetDeleteForm(instance=asset)

    return render(request, 'assets/trash.html', {'asset': asset, 'form': form})


def log_asset_event(request, asset, event):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    log = AssetChangeLog(asset=asset, log=event, ip=ip, created_by=request.user)
    log.save()


# Print Queue
# ----------------------------------------------------------------------------------------------------

@login_required
def print_queue(request, asset_id=None):
    asset = get_object_or_404(Asset, pk=asset_id)
    queue = PrintQueue(asset=asset, created_by=request.user)
    queue.save()
    messages.success(request, 'Asset added to print queue.')
    return redirect('assets:edit', asset_id)


@login_required
def print_queue_list(request):
    queryset = PrintQueue.objects.filter(created_by=request.user).all()
    return render(request, 'print-queue/list.html', {'list': queryset})


@login_required
def print_queue_delete(request, print_queue_id=None):
    p_queue = get_object_or_404(PrintQueue, pk=print_queue_id)
    p_queue.delete()
    return redirect('assets:print-queue-list')


# Manufacturer
# ----------------------------------------------------------------------------------------------------
@login_required
def manufacturer_list(request):
    queryset = Manufacturer.objects.all().order_by('name')

    paginator = Paginator(queryset, 25)
    page = request.GET.get('page')
    try:
        view_list = paginator.page(page)
    except PageNotAnInteger:
        view_list = paginator.page(1)
    except EmptyPage:
        view_list = paginator.page(paginator.num_pages)

    return render(request, 'manufacturer/list.html', {'list': view_list})


@login_required
def manufacturer_create(request):
    form = ManufacturerForm(request.POST or None)

    if form.is_valid():
        item = form.save(commit=False)
        item.created_by = request.user
        item.modified_by = request.user
        item.save()
        return HttpResponseRedirect(reverse('assets:manufacturer_list'))

    return render(request, 'manufacturer/post.html', {"form": form})


@login_required
def manufacturer_edit(request, manufacturer_id=None):
    manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)
    if request.POST:
        form = ManufacturerForm(request.POST, instance=manufacturer)
        if form.is_valid():
            manufacturer = form.save(commit=False)
            manufacturer.modified_by = request.user
            manufacturer.save()
            # Message
            messages.success(request, 'Updated manufacturer.')
            return HttpResponseRedirect(reverse('assets:manufacturer_list'))
        else:
            messages.warning(request, 'Please correct form errors to proceed.')
    else:
        form = ManufacturerForm(instance=manufacturer)
    return render(request, 'manufacturer/post.html', {"form": form, "manufacturer": manufacturer})


# Status
# ----------------------------------------------------------------------------------------------------
@login_required
def status_list(request):
    queryset = Status.objects.all().order_by('name')

    paginator = Paginator(queryset, 25)
    page = request.GET.get('page')
    try:
        view_list = paginator.page(page)
    except PageNotAnInteger:
        view_list = paginator.page(1)
    except EmptyPage:
        view_list = paginator.page(paginator.num_pages)

    return render(request, 'status/list.html', {'list': view_list})


@login_required
def status_create(request):
    form = StatusForm(request.POST or None)

    if form.is_valid():
        item = form.save(commit=False)
        item.created_by = request.user
        item.modified_by = request.user
        item.save()
        return HttpResponseRedirect(reverse('assets:status_list'))

    return render(request, 'status/post.html', {"form": form})


@login_required
def status_edit(request, status_id=None):
    status = get_object_or_404(Status, pk=status_id)
    if request.POST:
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            status = form.save(commit=False)
            status.modified_by = request.user
            status.save()
            # Message
            messages.success(request, 'Updated status.')
            return HttpResponseRedirect(reverse('assets:status_list'))
        else:
            messages.warning(request, 'Please correct form errors to proceed.')
    else:
        form = StatusForm(instance=status)
    return render(request, 'status/post.html', {"form": form, "status": status})


# Type
# ----------------------------------------------------------------------------------------------------
@login_required
def type_list(request):
    queryset = Type.objects.all().order_by('name')

    paginator = Paginator(queryset, 25)
    page = request.GET.get('page')
    try:
        view_list = paginator.page(page)
    except PageNotAnInteger:
        view_list = paginator.page(1)
    except EmptyPage:
        view_list = paginator.page(paginator.num_pages)

    return render(request, 'type/list.html', {'list': view_list})


@login_required
def type_create(request):
    form = TypeForm(request.POST or None)

    if form.is_valid():
        item = form.save(commit=False)
        item.created_by = request.user
        item.modified_by = request.user
        item.save()
        return HttpResponseRedirect(reverse('assets:type_list'))

    return render(request, 'type/post.html', {"form": form})


@login_required
def type_edit(request, type_id=None):
    type_item = get_object_or_404(Type, pk=type_id)
    if request.POST:
        form = TypeForm(request.POST, instance=type_item)
        if form.is_valid():
            type_item = form.save(commit=False)
            type_item.modified_by = request.user
            type_item.save()
            # Message
            messages.success(request, 'Updated type.')
            return HttpResponseRedirect(reverse('assets:type_list'))
        else:
            messages.warning(request, 'Please correct form errors to proceed.')
    else:
        form = TypeForm(instance=type_item)
    return render(request, 'type/post.html', {"form": form, "type_item": type_item})


# Sub-Type
# ----------------------------------------------------------------------------------------------------
@login_required
def subtype_list(request):
    queryset = SubType.objects.all().order_by('type__name', 'name')

    paginator = Paginator(queryset, 25)
    page = request.GET.get('page')
    try:
        view_list = paginator.page(page)
    except PageNotAnInteger:
        view_list = paginator.page(1)
    except EmptyPage:
        view_list = paginator.page(paginator.num_pages)

    return render(request, 'subtype/list.html', {'list': view_list})


@login_required
def subtype_create(request):
    form = SubTypeForm(request.POST or None)

    if form.is_valid():
        item = form.save(commit=False)
        item.created_by = request.user
        item.modified_by = request.user
        item.save()
        return HttpResponseRedirect(reverse('assets:subtype_list'))

    return render(request, 'subtype/post.html', {"form": form})


@login_required
def subtype_edit(request, subtype_id=None):
    subtype = get_object_or_404(SubType, pk=subtype_id)
    if request.POST:
        form = SubTypeForm(request.POST, instance=subtype)
        if form.is_valid():
            subtype = form.save(commit=False)
            subtype.modified_by = request.user
            subtype.save()
            # Message
            messages.success(request, 'Updated type.')
            return HttpResponseRedirect(reverse('assets:subtype_list'))
        else:
            messages.warning(request, 'Please correct form errors to proceed.')
    else:
        form = SubTypeForm(instance=subtype)
    return render(request, 'subtype/post.html', {"form": form, "subtype": subtype})


# Note
# ----------------------------------------------------------------------------------------------------
@login_required
def note_create(request, asset_id):
    asset = get_object_or_404(Asset, pk=asset_id)
    form = NoteForm(request.POST or None)
    form.initial = {'asset': asset}

    if request.POST:
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return HttpResponseRedirect(reverse('assets:edit', args=[asset_id]))

    return HttpResponseRedirect(reverse('assets:edit', args=[asset_id]))
