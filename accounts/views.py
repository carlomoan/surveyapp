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
            return redirect('accounts:home')
    ctx = {
        'form': form,
    }
    return render(request, 'accounts/profile_complete.html', ctx)


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


@user_passes_test(lambda user: user.is_staff, login_url='accounts:login')
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
        return redirect('accounts:list')
    return render(request, template_name, {'object': user})


class UserDetailView(DetailView):
    model = User
    template_name = "accounts/user_detail.html"


def user_form(request):
    form = Add_UserForm(request.POST or None)
    users = User.objects.all()
    if form.is_valid():
        form.save()
        messages.info(request, "User created successfully")
        return redirect('accounts:list')
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

class Region_List(ListView):
    model = Region
    template_name = "accounts/regions.html"

    def get_queryset(self):
        return Region.objects.all()

class RegionCreateView(SuccessMessageMixin, CreateView):                                 # createview class to add new stock, mixin used to display message
    model = Region                                                                       # setting 'Stock' model as model
    form_class = Add_Region                                                              # setting 'StockForm' form as form
    template_name = "accounts/add_region.html"                                                   # 'edit_stock.html' used as the template
    success_url = 'accounts/regions.html'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Region has been created successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Region'
        context["savebtn"] = 'Add to Region'
        return context  


class RegionUpdateView(SuccessMessageMixin, UpdateView):                                 # updateview class to edit stock, mixin used to display message
    model = Region                                                                       # setting 'Stock' model as model
    form_class = Add_Region                                                              # setting 'StockForm' form as form
    template_name = "accounts/add_region.html"                                                   # 'edit_stock.html' used as the template
    success_url = "accounts/regions.html"                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Region has been updated successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Region'
        context["savebtn"] = 'Update Region'
        context["delbtn"] = 'Delete Region'
        return context


class RegionDeleteView(View):                                                            # view class to delete stock
    template_name = "accounts/dlt_region.html"                                                 # 'delete_stock.html' used as the template
    success_message = "Region has been deleted successfully"                             # displays message when form is submitted
    
    def get(self, request, pk):
        region = get_object_or_404(Region, pk=pk)
        return render(request, self.template_name, {'object' : region})

    def post(self, request, pk):  
        region = get_object_or_404(Region, pk=pk)
        region.is_deleted = True
        region.save()                                               
        messages.success(request, self.success_message)
        return redirect('region_list')   

class District_List(ListView):
    model = District
    template_name = "accounts/districts.html"

    def get_queryset(self):
        return District.objects.all()

class DistrictCreateView(SuccessMessageMixin, CreateView):                                 # createview class to add new stock, mixin used to display message
    model = District                                                                       # setting 'Stock' model as model
    form_class = Add_District                                                             # setting 'StockForm' form as form
    template_name = "accounts/add_region.html"                                                   # 'edit_stock.html' used as the template
    success_url = 'accounts/districts.html'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "District has been created successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'New District'
        context["savebtn"] = 'Add to District'
        return context  


class DistrictUpdateView(SuccessMessageMixin, UpdateView):                                 # updateview class to edit stock, mixin used to display message
    model = District                                                                       # setting 'Stock' model as model
    form_class = Add_District                                                              # setting 'StockForm' form as form
    template_name = "accounts/add_district.html"                                                   # 'edit_stock.html' used as the template
    success_url = "accounts/districts.html"                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "District has been updated successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit District'
        context["savebtn"] = 'Update District'
        context["delbtn"] = 'Delete District'
        return context


class DistrictDeleteView(View):                                                            # view class to delete stock
    template_name = "accounts/dlt_district.html"                                                 # 'delete_stock.html' used as the template
    success_message = "District has been deleted successfully"                             # displays message when form is submitted
    
    def get(self, request, pk):
        district = get_object_or_404(District, pk=pk)
        return render(request, self.template_name, {'object' : district})

    def post(self, request, pk):  
        district = get_object_or_404(District, pk=pk)
        district.is_deleted = True
        district.save()                                               
        messages.success(request, self.success_message)
        return redirect('district_list')   

class Ward_List(ListView):
    model = Ward
    template_name = "accounts/wards.html"

    def get_queryset(self):
        return Ward.objects.all()

class WardCreateView(SuccessMessageMixin, CreateView):                                 # createview class to add new stock, mixin used to display message
    model = Ward                                                                       # setting 'Stock' model as model
    form_class = Add_Ward                                                             # setting 'StockForm' form as form
    template_name = "accounts/add_ward.html"                                                   # 'edit_stock.html' used as the template
    success_url = 'accounts/wards.html'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Ward has been created successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Ward'
        context["savebtn"] = 'Add to Ward'
        return context  


class WardUpdateView(SuccessMessageMixin, UpdateView):                                 # updateview class to edit stock, mixin used to display message
    model = Ward                                                                       # setting 'Stock' model as model
    form_class = Add_Ward                                                              # setting 'StockForm' form as form
    template_name = "accounts/add_ward.html"                                                   # 'edit_stock.html' used as the template
    success_url = "accounts/wards.html"                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Ward has been updated successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Ward'
        context["savebtn"] = 'Update Ward'
        context["delbtn"] = 'Delete Ward'
        return context

class WardDeleteView(View):                                                            # view class to delete stock
    template_name = "accounts/dlt_ward.html"                                                 # 'delete_stock.html' used as the template
    success_message = "Ward has been deleted successfully"                             # displays message when form is submitted
    
    def get(self, request, pk):
        ward = get_object_or_404(Ward, pk=pk)
        return render(request, self.template_name, {'object' : ward})

    def post(self, request, pk):  
        ward = get_object_or_404(ward, pk=pk)
        ward.is_deleted = True
        ward.save()                                               
        messages.success(request, self.success_message)
        return redirect('ward_list')
        

class Street_List(ListView):
    model = Street
    template_name = "accounts/streets.html"

    def get_queryset(self):
        return Street.objects.all()

class StreetCreateView(SuccessMessageMixin, CreateView):                                 # createview class to add new stock, mixin used to display message
    model = Street                                                                       # setting 'Stock' model as model
    form_class = Add_Area                                                             # setting 'StockForm' form as form
    template_name = "accounts/street_ward.html"                                                   # 'edit_stock.html' used as the template
    success_url = 'accounts/street.html'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Street has been created successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Street'
        context["savebtn"] = 'Add to Street'
        return context  


class StreetUpdateView(SuccessMessageMixin, UpdateView):                                 # updateview class to edit stock, mixin used to display message
    model = Street                                                                       # setting 'Stock' model as model
    form_class = Add_Area                                                             # setting 'StockForm' form as form
    template_name = "accounts/add_street.html"                                                   # 'edit_stock.html' used as the template
    success_url = "accounts/streets.html"                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Street has been updated successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Street'
        context["savebtn"] = 'Update Street'
        context["delbtn"] = 'Delete Street'
        return context

class StreetDeleteView(View):                                                            # view class to delete stock
    template_name = "accounts/dlt_street.html"                                                 # 'delete_stock.html' used as the template
    success_message = "Street has been deleted successfully"                             # displays message when form is submitted
    
    def get(self, request, pk):
        street = get_object_or_404(Street, pk=pk)
        return render(request, self.template_name, {'object' : street})

    def post(self, request, pk):  
        street = get_object_or_404(street, pk=pk)
        street.is_deleted = True
        street.save()                                               
        messages.success(request, self.success_message)
        return redirect('street_list')


def index(request):
    context = {'a': 'a'}
    return render(request, 'index.html', context)

