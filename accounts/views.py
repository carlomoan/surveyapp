from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import *
from .models import *
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth import (
    authenticate, login as auth_login, logout as auth_logout)
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages.views import SuccessMessageMixin
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
        elif (request.user.is_authenticated and request.user.approval_status == 'a'):
            if request.user.user_roles == 1:
                return redirect("accounts:dashboard")
            elif request.user.user_roles == 2:
                return redirect("accounts:home")
            elif request.user.user_roles == 3:
                return redirect("accounts:home")
            else:
                return redirect("accounts:home")
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
            return redirect('accounts:home')
    ctx = {
        'form': form,
    }
    return render(request, 'accounts/profile_complete.html', ctx)


@login_required
def user_approval(request, pk):
    user = User.objects.get(pk=pk)
    user.approval_status = 'a'
    # TODO: Implement role assignment.
    # assign_role(user, 'role')
    user.save()
    return HttpResponseRedirect(reverse('accounts:list'))


@login_required
def permission_error(request):
    return HttpResponse('You don\'t have right permission to access this page.')


@login_required
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


@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = "accounts/user_list.html"

    def get_queryset(self):
        return User.objects.all()


@method_decorator(login_required, name='dispatch')
class EditUserView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "accounts/user_edit.html"
    success_url = ""
    success_message = "User has been Updated successfully"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class UpdateUserView(UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = "accounts/user_edit.html"
    success_url = ""
    success_message = "User has been Updated successfully"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def delete_user(request, pk, template_name='accounts/user_list.html'):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('accounts:list')
    return render(request, template_name, {'object': user})


@method_decorator(login_required, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = "accounts/user_detail.html"


@login_required
def user_form(request):
    form = Add_UserForm(request.POST or None)
    users = User.objects.all()
    if form.is_valid():
        form.save()
        messages.info(request, "User created successfully")
        return redirect('accounts:list')
    return render(request, "accounts/add_user.html", {'form': form, 'users': users})


@method_decorator(login_required, name='dispatch')
def user_delete(request, username):
    user = User.objects.get(username=username)
    user.delete()
    return render(request, "accounts/user_list.html")


@method_decorator(login_required, name='dispatch')
class Region_List(ListView):
    model = Region
    template_name = "accounts/regions.html"

    def get_queryset(self):
        return Region.objects.all()


# createview class to add new stock, mixin used to display message
@method_decorator(login_required, name='dispatch')
class RegionCreateView(SuccessMessageMixin, CreateView):
    # setting 'Stock' model as model
    model = Region
    # setting 'StockForm' form as form
    form_class = Add_Region
    # 'edit_stock.html' used as the template
    template_name = "accounts/add_region.html"
    # redirects to 'inventory' page in the url after submitting the form
    success_url = 'accounts/regions.html'
    # displays message when form is submitted
    success_message = "Region has been created successfully"

    # used to send additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Region'
        context["savebtn"] = 'Add to Region'
        return context


# updateview class to edit stock, mixin used to display message
@method_decorator(login_required, name='dispatch')
class RegionUpdateView(SuccessMessageMixin, UpdateView):
    # setting 'Stock' model as model
    model = Region
    # setting 'StockForm' form as form
    form_class = Add_Region
    # 'edit_stock.html' used as the template
    template_name = "accounts/add_region.html"
    # redirects to 'inventory' page in the url after submitting the form
    success_url = "accounts/regions.html"
    # displays message when form is submitted
    success_message = "Region has been updated successfully"

    # used to send additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Region'
        context["savebtn"] = 'Update Region'
        context["delbtn"] = 'Delete Region'
        return context


# view class to delete stock
@method_decorator(login_required, name='dispatch')
class RegionDeleteView(View):
    # 'delete_stock.html' used as the template
    template_name = "accounts/dlt_region.html"
    # displays message when form is submitted
    success_message = "Region has been deleted successfully"

    def get(self, request, pk):
        region = get_object_or_404(Region, pk=pk)
        return render(request, self.template_name, {'object': region})

    def post(self, request, pk):
        region = get_object_or_404(Region, pk=pk)
        region.is_deleted = True
        region.save()
        messages.success(request, self.success_message)
        return redirect('region_list')


@method_decorator(login_required, name='dispatch')
class District_List(ListView):
    model = District
    template_name = "accounts/districts.html"

    def get_queryset(self):
        return District.objects.all()


# createview class to add new stock, mixin used to display message
@method_decorator(login_required, name='dispatch')
class DistrictCreateView(SuccessMessageMixin, CreateView):
    # setting 'Stock' model as model
    model = District
    # setting 'StockForm' form as form
    form_class = Add_District
    # 'edit_stock.html' used as the template
    template_name = "accounts/add_region.html"
    # redirects to 'inventory' page in the url after submitting the form
    success_url = 'accounts/districts.html'
    # displays message when form is submitted
    success_message = "District has been created successfully"

    # used to send additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New District'
        context["savebtn"] = 'Add to District'
        return context


# updateview class to edit stock, mixin used to display message
@method_decorator(login_required, name='dispatch')
class DistrictUpdateView(SuccessMessageMixin, UpdateView):
    # setting 'Stock' model as model
    model = District
    # setting 'StockForm' form as form
    form_class = Add_District
    # 'edit_stock.html' used as the template
    template_name = "accounts/add_district.html"
    # redirects to 'inventory' page in the url after submitting the form
    success_url = "accounts/districts.html"
    # displays message when form is submitted
    success_message = "District has been updated successfully"

    # used to send additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit District'
        context["savebtn"] = 'Update District'
        context["delbtn"] = 'Delete District'
        return context


# view class to delete stock
@method_decorator(login_required, name='dispatch')
class DistrictDeleteView(View):
    # 'delete_stock.html' used as the template
    template_name = "accounts/dlt_district.html"
    # displays message when form is submitted
    success_message = "District has been deleted successfully"

    def get(self, request, pk):
        district = get_object_or_404(District, pk=pk)
        return render(request, self.template_name, {'object': district})

    def post(self, request, pk):
        district = get_object_or_404(District, pk=pk)
        district.is_deleted = True
        district.save()
        messages.success(request, self.success_message)
        return redirect('district_list')


@method_decorator(login_required, name='dispatch')
class Ward_List(ListView):
    model = Ward
    template_name = "accounts/wards.html"

    def get_queryset(self):
        return Ward.objects.all()


# createview class to add new stock, mixin used to display message
@method_decorator(login_required, name='dispatch')
class WardCreateView(SuccessMessageMixin, CreateView):
    # setting 'Stock' model as model
    model = Ward
    # setting 'StockForm' form as form
    form_class = Add_Ward
    # 'edit_stock.html' used as the template
    template_name = "accounts/add_ward.html"
    # redirects to 'inventory' page in the url after submitting the form
    success_url = 'accounts/wards.html'
    # displays message when form is submitted
    success_message = "Ward has been created successfully"

    # used to send additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Ward'
        context["savebtn"] = 'Add to Ward'
        return context


# updateview class to edit stock, mixin used to display message
@method_decorator(login_required, name='dispatch')
class WardUpdateView(SuccessMessageMixin, UpdateView):
    # setting 'Stock' model as model
    model = Ward
    # setting 'StockForm' form as form
    form_class = Add_Ward
    # 'edit_stock.html' used as the template
    template_name = "accounts/add_ward.html"
    # redirects to 'inventory' page in the url after submitting the form
    success_url = "accounts/wards.html"
    # displays message when form is submitted
    success_message = "Ward has been updated successfully"

    # used to send additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Ward'
        context["savebtn"] = 'Update Ward'
        context["delbtn"] = 'Delete Ward'
        return context


# view class to delete stock
@method_decorator(login_required, name='dispatch')
class WardDeleteView(View):
    # 'delete_stock.html' used as the template
    template_name = "accounts/dlt_ward.html"
    # displays message when form is submitted
    success_message = "Ward has been deleted successfully"

    def get(self, request, pk):
        ward = get_object_or_404(Ward, pk=pk)
        return render(request, self.template_name, {'object': ward})

    def post(self, request, pk):
        ward = get_object_or_404(ward, pk=pk)
        ward.is_deleted = True
        ward.save()
        messages.success(request, self.success_message)
        return redirect('ward_list')


def index(request):
    context = {'a': 'a'}
    return render(request, 'index.html', context)
