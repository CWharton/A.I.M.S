from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from users.forms import UserForm


@login_required
def user_list(request):
    queryset = User.objects.all().order_by('first_name')

    paginator = Paginator(queryset, 25)
    page = request.GET.get('page')
    try:
        view_list = paginator.page(page)
    except PageNotAnInteger:
        view_list = paginator.page(1)
    except EmptyPage:
        view_list = paginator.page(paginator.num_pages)

    return render(request, 'user/list.html', {'list': view_list})


@login_required
def user_create(request):
    form = UserForm(request.POST or None)

    if request.POST:
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.modified_by = request.user
            item.save()

    return render(request, 'user/post.html', {'form': form})


@login_required
def user_edit(request, user_id=None):
    user = get_object_or_404(User, pk=user_id)
    if request.POST:
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.modified_by = request.user
            user.save()
            # Message
            messages.success(request, 'Updated user.')
        else:
            messages.warning(request, 'Please correct form errors to proceed.')
    else:
        form = UserForm(instance=user)
    return render(request, 'user/post.html', {'select_user': user, 'form': form})
