from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import *
from .models import *
from django.urls import reverse, reverse_lazy
from django.contrib.auth import (
    authenticate, login as auth_login, logout as auth_logout)
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.template.loader import render_to_string
from django.views import generic
from django.views.generic import *


# Create your views here
def user_is_staff(user):
    return user.is_staff


def user_is_admin(user):
    return user.user_roles == '1'


@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        return redirect('list/')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        auth_login(request, user)
        print(request.user.is_authenticated)
        if (request.user.is_authenticated and request.user.approval_status == 'n'):
            return redirect("accounts:profile_complete")
        elif (request.user.is_authenticated and request.user.user_roles == 1):
            return redirect("accounts:dashboard")
        else:
            return redirect("/")

    form = UserLoginForm()

    return render(request, "accounts/login.html", {'form': form})


@login_required
def logout(request):
    auth_logout(request)
    messages.info(request, "You logged out.")
    return redirect('/')


@login_required
def profile_complete(request):
    user = User.objects.get(pk=request.user.pk)
    form = ProfileCompleteForm(instance=user)
    if request.method == 'POST':
        form = ProfileCompleteForm(request.POST, instance=user)
        if form.is_valid():
            form.instance.approval_status = 'p'  # pending
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Your request has been sent, please be patient.'
            )
            return redirect('accounts:profile_complete')
    ctx = {
        'form': form,
    }
    return render(request, 'accounts/profile_complete.html', ctx)


@user_passes_test(user_is_admin, login_url='account:permission_error')
def user_approval(request, pk):
    user = User.objects.get(pk=pk)
    user.approval_status = 'a'
    # TODO: Implement role assignment.
    # assign_role(user, 'role')
    user.save()
    return JsonResponse({'approval_status': 'approved'})


@login_required
def permission_error(request):
    return HttpResponse('You don\'t have right permission to access this page.')


@user_passes_test(user_is_staff, login_url='accounts:login')
def dashboard(request):
    total_Users = User.objects.count()
    total_region = Region.objects.count()
    total_district = District.objects.count()
    total_ward = Ward.objects.count()
    context = {
        'total_users': total_Users,
        'total_regions': total_region,
        'total_districts': total_district,
        'total_wards': total_ward
    }
    return render(request, 'accounts/dashboard.html', context)


class UserListView(ListView):
    model = User
    template_name = "accounts/user_list.html"

    def get_queryset(self):
        return User.objects.all()


class UserUpdateView(UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'accounts/user_edit.html'

    def dispatch(self, *args, **kwargs):
        self.user_id = kwargs['pk']
        return super(UserUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        item = User.objects.get(id=self.user_id)
        return HttpResponse(render_to_string('accounts/user_edit.html', {'item': item}))


def edit_user(request, pk, template_name='accounts/user_edit.html'):
    user = get_object_or_404(User, pk=pk)
    form = UserUpdateForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('accounts:list')
    return render(request, template_name, {'form': form})


def delete_user(request, pk, template_name='accounts/user_list.html'):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('survey_project:list')
    return render(request, template_name, {'object': user})


class UserDetailView(DetailView):
    model = User
    template_name = "accounts/user_detail.html"


def user_form(request):
    form = Add_UserForm(request.POST or None)
    users = User.objects.all()
    if form.is_valid():
        form.save()
        return ("accounts/user_list.html")
    return render(request, "accounts/add_user.html", {'form': form, 'users': users})


def user_update(request, pk):
    username = User.objects.get(pk=pk)
    form = Add_UserForm(request.POST or None, instance=pk)
    users = User.objects.all()
    if form.is_valid():
        form.save()
        return ("accounts/user_list.html")
    return render(request, "accounts/add_user.html", {'form': form, 'users': users})


def user_delete(request, username):
    user = User.objects.get(username=username)
    user.delete()
    return render(request, "accounts/user_list.html")


def save_region_form(request,  form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            mikoa = Region.objects.all()
            data['html_mikoa_list'] = render_to_string('accounts/regions.html', {
                'mikoa': mikoa
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

    ''' form = Add_Region(request.POST or None)
    mikoa = Region.objects.all()
    if form.is_valid():
        form.save()
        return ("accounts/places_list.html")
    return render(request, "accounts/add_region.html", {'form': form, 'regions': mikoa}) '''


def region_create(request):
    if request.method == 'POST':
        form = Add_Region(request.POST)
    else:
        form = Add_Region()
    return save_region_form(request, form, 'accounts/regions.html')

class Region_List(ListView):
    model = Region
    template_name = "accounts/regions.html"

    def get_queryset(self):
        return Region.objects.all()


def places(request):
    queryset = Region.objects.all()
    context = {"Region_list": queryset}
    return render(request, "accounts/places_list.html", context)


def index(request):
    context = {'a': 'a'}
    return render(request, 'index.html', context)


def load_places(request):
    region_id = request.GET.get(region_id)
    districts = District.objects.filter(region_id=region_id).all()
    return render(request, 'accounts/district.html', {'districts': districts})
