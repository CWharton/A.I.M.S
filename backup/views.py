import datetime
import gzip
import shutil
import tempfile
from subprocess import Popen
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render


@login_required
def backup_view(request):
    return render(request, 'backup.html')


@login_required
def backup(request, uncompress=False):
    tmp_file = Path(tempfile.gettempdir() + '/dumped_data.json')
    tmp_file_gz = Path(tempfile.gettempdir() + '/aims_data.json.gz')

    cmd = 'python manage.py dumpdata -o {}'.format(tmp_file)

    with open(tmp_file, 'w') as f:
        p_open = Popen(cmd, shell=True)
        p_open.wait()

    # Compress
    if not uncompress:
        with open(tmp_file, 'rb') as f_in:
            with gzip.open(tmp_file_gz, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    output = 'aims_backup_{}.json'.format(datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))

    file = open(tmp_file if uncompress else tmp_file_gz, 'rb')
    return FileResponse(file, as_attachment=True, filename=output if uncompress else output+'.gz')


@login_required
def restore(request):
    tmp_file = Path(tempfile.gettempdir() + '/dumped_data.json')

    cmd = 'python manage.py loaddata -e auth.permission -e contenttypes.contenttype {}'.format(tmp_file)

    with open(tmp_file, 'w') as f:
        p_open = Popen(cmd, shell=True)
        p_open.wait()

    return render(request, 'backup.html')
