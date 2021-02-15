from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from .forms import *
from .models import *

# Create your views here.
@login_required
def projects(request):
    queryset = SurveyProject.objects.all()
    context = {"Projects": queryset}
    return render(request, "survey_project/index.html", context)


def project_create(request):
    if request.method == 'POST':
        new_project_form = Add_ProjectForm(request.POST)
        if new_project_form.is_valid:
            new_project = new_project_form.save(commit=False)
            new_project.recorded_by = request.accounts.user
            new_project.save()
            return redirect('survey_project:list')
    new_project_form = Add_ProjectForm()
    context = {'new_project_form': new_project_form}
    return render(request, 'survey_project/project_add.html', context)

def edit_project(request, pk, template_name='survey_project/project_edit.html'):
    project = get_object_or_404(SurveyProject, pk=pk)
    form = Add_ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('survey_project:list')
    return render(request, template_name, {'form':form})

def delete_project(request, pk, template_name='survey_project/project_delete.html'):
    project = get_object_or_404(SurveyProject, pk=pk)
    if request.method=='POST':
        project.delete()
        return redirect('survey_project:list')
    return render(request, template_name, {'object':tool})


class ProjectDetailView(DetailView):
    model = SurveyProject
    template_name = "survey_project/project_detail.html"



''' def update_store(request):
    if request.method == 'POST':
        store_form = StoreUpdateForm(request.POST)
        if store_form.is_valid:
            store = store_form.save(commit=False)
            store.recorded_by = request.accounts.user
            store.save()
    store_form = StoreUpdateForm()
    context = {'store_form': store_form}
    return render(request, 'survey_project/add_store.html', context)


def add_wellinfo(request):
    if request.method == 'POST':
        well_form = WellInfoForm(request.POST)
        if well_form.is_valid:
            well = well_form.save(commit=False)
            well.recorded_by = request.accounts.user
            well.save()
    well_form = WellInfoForm()
    context = {'well_form': well_form}
    return render(request, 'survey_project/add_wellinfo.html', context) '''


class EquipmentListView(ListView):
    model = Equipment
    template_name = "survey_project/equipment.html"

def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('survey_project:equipment_list')
    form = EquipmentForm()
    return render(request,'survey_project/equipment_add.html',{'form': form})


def edit_equipment(request, pk, template_name='survey_project/equipment_edit.html'):
    tool = get_object_or_404(Equipment, pk=pk)
    form = EquipmentForm(request.POST or None, instance=tool)
    if form.is_valid():
        form.save()
        return redirect('survey_project:equipment_list')
    return render(request, template_name, {'form':form})

def delete_equipment(request, pk, template_name='survey_project/equipment_delete.html'):
    tool = get_object_or_404(Equipment, pk=pk)
    if request.method=='POST':
        tool.delete()
        return redirect('survey_project:equipment_list')
    return render(request, template_name, {'object':tool})


class EquipmentDetailView(DetailView):
    model = Equipment
    template_name = "survey_project/equipment_detail.html"


class StoreListView(ListView):
    model = Store
    template_name = "survey_project/store.html"

def add_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('survey_project:store_list')
    form = StoreForm()
    return render(request,'survey_project/store_add.html',{'form': form})


def edit_store(request, pk, template_name='survey_project/edit_store.html'):
    item = get_object_or_404(Store, pk=pk)
    form = StoreForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('survey_project:store_list')
    return render(request, template_name, {'form':form})

def delete_store(request, pk, template_name='survey_project/delete_store.html'):
    item = get_object_or_404(Store, pk=pk)
    if request.method=='POST':
        item.delete()
        return redirect('survey_project:store_list')
    return render(request, template_name, {'object':item})

class StoreDetailView(DetailView):
    model = Equipment
    template_name = "survey_project/storeinfo_detail.html"


class WellsListView(ListView):
    model = WellInfo
    template_name = "survey_project/wells.html"

def add_well(request):
    if request.method == 'POST':
        form = WellInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('survey_project:development_info_list')
    form = WellInfoForm()
    return render(request,'survey_project/well_add.html',{'form': form})


def edit_well(request, pk, template_name='survey_project/well_edit.html'):
    well = get_object_or_404(WellInfo, pk=pk)
    form = WellInfoForm(request.POST or None, instance=well)
    if form.is_valid():
        form.save()
        return redirect('survey_project:development_info_list')
    return render(request, template_name, {'form':form})

def delete_well(request, pk, template_name='survey_project/well_delete.html'):
    well = get_object_or_404(WellInfo, pk=pk)
    if request.method=='POST':
        item.delete()
        return redirect('survey_project:development_info_list')
    return render(request, template_name, {'object':well})

class WellDetailView(DetailView):
    model = WellInfo
    template_name = "survey_project/well_detail.html"
