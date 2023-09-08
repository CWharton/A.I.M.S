import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from assets.models import AssetCheckIn, Asset
from networks.models import AssetNetwork, Network


@login_required
def subnet_ip_select(request):
    queryset = Network.objects.all().order_by('name')

    return render(request, 'subnet_ip_select.html', {'list': queryset})


@login_required
def subnet_ip_report(request, network_id=None):
    network = get_object_or_404(Network, pk=network_id)
    queryset = AssetNetwork.objects.filter(network=network_id).filter(asset__status__name='In Use').all().order_by(
        'name')

    init_ip_list = network.ipv4_address.split('.')
    init_ip_list.pop(len(init_ip_list) - 1)

    list_set = []
    for x in range(0, 254):
        x = x + 1
        ip_address = '.'.join(init_ip_list) + '.%d' % x
        item = {'ipv4_address': ip_address}

        selected = {}
        for obj in queryset:
            if ip_address == obj.ipv4_address:
                selected = obj

        if selected:
            item['name'] = selected.asset.equipment
            item['location'] = selected.asset.location
            item['serial'] = selected.asset.serial
            item['type'] = selected.asset.type.name
            item['sub_type'] = selected.asset.sub_type.name

        list_set.append(item)

    return render(request, 'subnet_ip_report.html', {'network': network, 'list': list_set})


@login_required
def audit_report(request):
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    date_from = datetime.datetime.now().date() - datetime.timedelta(days=90) if date_from == '' else date_from
    date_to = datetime.datetime.now().date() if date_to == '' else date_to

    query_date_to = datetime.datetime.strptime(str(date_to), "%Y-%m-%d") + datetime.timedelta(days=1)
    checkin = AssetCheckIn.objects.filter(created__range=[date_from, query_date_to]).values('asset_id')
    missing_assets = Asset.objects.filter(Q(omit_audit=False) | Q(omit_audit__isnull=True))\
        .exclude(id__in=checkin).all().order_by('name')

    return render(request, 'audit.html',
                  {'assets': missing_assets, 'date_from': str(date_from), 'date_to': str(date_to)})


@login_required
def inventory_report(request):
    queryset = Asset.objects.all().order_by('name')

    return render(request, 'inventory_report.html', {'assets': queryset})
