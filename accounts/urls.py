from django.urls import path, include, re_path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),

    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    path('users', views.UserListView.as_view(), name='list'),
    path('user/add', views.user_form, name='add'),
    path('user/profile_complete', views.profile_complete, name='profile_complete'),
    path('user/update/<int:pk>', views.UpdateUserView.as_view(), name='update'),
    path('user/edit/<int:pk>', views.EditUserView.as_view(), name='edit'),
    path('user/delete/<int:pk>', views.user_delete, name='delete'),
    path('user/permission-error/', views.permission_error, name='permission_error'),
    path('user/detail/<int:pk>', views.UserDetailView.as_view(), name='user_detail'),
    path('user/approval/<int:pk>/', views.user_approval, name='user_approval'),

    path('region/add', views.RegionCreateView.as_view(), name='add_region'),
    path('region/list', views.Region_List.as_view(), name='region_list'),
    path('region/update/<int:pk>',
         views.RegionUpdateView.as_view(), name='update_region'),
    path('region/delete/<int:pk>',
         views.RegionDeleteView.as_view(), name='delete_region'),

    path('district/add', views.DistrictCreateView.as_view(), name='add_district'),
    path('district/list', views.District_List.as_view(), name='district_list'),
    path('district/update/<int:pk>',
         views.DistrictUpdateView.as_view(), name='update_district'),
    path('district/delete/<int:pk>',
         views.DistrictDeleteView.as_view(), name='delete_district'),


]
