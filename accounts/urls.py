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
    path('region/add', views.RegionCreate.as_view(), name='add_region'),
    path('region/list', views.RegionList.as_view(), name='region_list'),
    path('region/update/<int:pk>', views.RegionUpdate.as_view(), name='update_region'),
    path('region/read/<int:pk>', views.RegionDetail.as_view(), name='read_region'),
    path('region/delete/<int:pk>', views.RegionDelete.as_view(), name='delete_region'),
    path('user/profile_complete', views.profile_complete, name='profile_complete'),
    path('user/edit/<int:pk>', views.edit_user, name='edit'),
    path('user/delete/<int:pk>', views.user_delete, name='delete'),
    path('user/update/<int:pk>', views.UserUpdateView.as_view(), name='update'),
    path('user/permission-error/', views.permission_error, name='permission_error'),
    path('user/detail/<int:pk>', views.UserDetailView.as_view(), name='user_detail'),
    path('user/approval/<int:pk>/', views.user_approval, name='user_approval'),

]
