from django.urls import path, include
from . import views

app_name = 'survey_project'

urlpatterns = [
    path('', views.projects, name='list'),
    path('project/create/', views.project_create, name='project_add'),
    path('project/edit/<int:pk>/', views.edit_project, name='project_edit'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(),
         name='project_detail'),
    path('project/delete/<int:pk>/', views.delete_project, name='project_delete'),
    path('equipment/create/', views.add_equipment, name='equipment_add'),
    path('equipment/', views.EquipmentListView.as_view(), name='equipment_list'),
    path('equipment/edit/<int:pk>/', views.edit_equipment, name='equipment_edit'),
    path('equipment/<int:pk>/', views.EquipmentDetailView.as_view(),
         name='equipment_detail'),
    path('equipment/delete/<int:pk>/',
         views.delete_equipment, name='equipment_delete'),
    path('well/create/', views.add_well, name='development_info_add'),
    path('well/list/', views.WellsListView.as_view(),
         name='development_info_list'),
    path('well/edit/<int:pk>/', views.edit_well, name='development_info_edit'),
    path('well/<int:pk>/', views.WellDetailView.as_view(),
         name='development_info_detail'),
    path('well/delete/<int:pk>/', views.delete_well,
         name='development_info_delete'),
    path('store/', views.StoreListView.as_view(), name='store_list'),
    path('store/create/', views.add_store, name='store_add'),
    path('store/edit/<int:pk>/', views.edit_store, name='store_edit'),
    path('store/<int:pk>/', views.StoreDetailView.as_view(), name='store_detail'),
    path('store/delete/<int:pk>/', views.delete_store, name='store_delete')

]
