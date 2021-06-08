from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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


@login_required
def project_create(request):
    if request.method == 'POST':
        form = Add_ProjectForm(request.POST)
        photos = ImagesForm(request.POST, request.FILES.getlist('picture'))
        scenes = VideosForm(request.POST, request.FILES.getlist('video'))
        docs = AttachmentsForm(
            request.POST, request.FILES.getlist('attachments'))
        if form.is_valid and photos.is_valid and scenes.is_valid and docs.is_valid:
            new_project = form.save(commit=False)
            new_project.author = request.user
            new_project.save()

            for photo in photos:
                # Do something with each file.
                photoform = form.save(commit=False)
                photoform.save()

            for scene in scenes:
                # Do something with each file.
                sceneform = form.save(commit=False)
                sceneform.save()

            for doc in docs:
                # Do something with each file.
                docform = form.save(commit=False)
                docform.save()

            return redirect('survey_project:list')
    form = Add_ProjectForm()
    photos = ImagesForm()
    scenes = VideosForm()
    docs = AttachmentsForm()
    context = {'form': form, 'photos': photos, 'scenes': scenes, 'docs': docs}
    return render(request, 'survey_project/project_add.html', context)


@login_required
def edit_project(request, pk, template_name='survey_project/project_edit.html'):
    project = get_object_or_404(SurveyProject, pk=pk)
    form = Add_ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('survey_project:list')
    return render(request, template_name, {'form': form})


@login_required
def delete_project(request, pk, template_name='survey_project/project_delete.html'):
    project = get_object_or_404(SurveyProject, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('survey_project:list')
    return render(request, template_name, {'object': tool})


@method_decorator(login_required, name='dispatch')
class ProjectDetailView(DetailView):
    model = SurveyProject
    template_name = "survey_project/project_details.html"


@method_decorator(login_required, name='dispatch')
class EquipmentListView(ListView):
    model = Equipment
    template_name = "survey_project/equipment.html"


@method_decorator(login_required, name='dispatch')
def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('survey_project:equipment_list')
    form = EquipmentForm()
    return render(request, 'survey_project/equipment_add.html', {'form': form})


@method_decorator(login_required, name='dispatch')
def edit_equipment(request, pk, template_name='survey_project/equipment_edit.html'):
    tool = get_object_or_404(Equipment, pk=pk)
    form = EquipmentForm(request.POST or None, instance=tool)
    if form.is_valid():
        form.save()
        return redirect('survey_project:equipment_list')
    return render(request, template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
def delete_equipment(request, pk, template_name='survey_project/equipment_delete.html'):
    tool = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        tool.delete()
        return redirect('survey_project:equipment_list')
    return render(request, template_name, {'object': tool})


@method_decorator(login_required, name='dispatch')
class EquipmentDetailView(DetailView):
    model = Equipment
    template_name = "survey_project/equipment_detail.html"


@method_decorator(login_required, name='dispatch')
class StoreListView(ListView):
    model = Store
    template_name = "survey_project/store.html"


@method_decorator(login_required, name='dispatch')
def add_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('survey_project:store_list')
    form = StoreForm()
    return render(request, 'survey_project/store_add.html', {'form': form})


@method_decorator(login_required, name='dispatch')
def edit_store(request, pk, template_name='survey_project/edit_store.html'):
    item = get_object_or_404(Store, pk=pk)
    form = StoreForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('survey_project:store_list')
    return render(request, template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
def delete_store(request, pk, template_name='survey_project/delete_store.html'):
    item = get_object_or_404(Store, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('survey_project:store_list')
    return render(request, template_name, {'object': item})


@method_decorator(login_required, name='dispatch')
class StoreDetailView(DetailView):
    model = Equipment
    template_name = "survey_project/storeinfo_detail.html"


@method_decorator(login_required, name='dispatch')
class WellsListView(ListView):
    model = WellInfo
    template_name = "survey_project/wells.html"


@method_decorator(login_required, name='dispatch')
def add_well(request):
    if request.method == 'POST':
        form = WellInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('survey_project:development_info_list')
    form = WellInfoForm()
    return render(request, 'survey_project/well_add.html', {'form': form})


@method_decorator(login_required, name='dispatch')
def edit_well(request, pk, template_name='survey_project/well_edit.html'):
    well = get_object_or_404(WellInfo, pk=pk)
    form = WellInfoForm(request.POST or None, instance=well)
    if form.is_valid():
        form.save()
        return redirect('survey_project:development_info_list')
    return render(request, template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
def delete_well(request, pk, template_name='survey_project/well_delete.html'):
    well = get_object_or_404(WellInfo, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('survey_project:development_info_list')
    return render(request, template_name, {'object': well})


@method_decorator(login_required, name='dispatch')
class WellDetailView(DetailView):
    model = WellInfo
    template_name = "survey_project/well_detail.html"
