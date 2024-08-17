from django.urls import path

from . import views

urlpatterns = [
    path('registration', views.employee_registration, name='employee-registration'),
    path('list', views.employee_list, name='employee-list'),
    path('load-upazilla', views.load_upazilla, name='load-upazilla'),
    path('profile/<employee_id>', views.employee_profile, name='employee_profile'),
    path('edit/<employee_id>', views.employee_edit, name='employee_edit'),
    path('delete/<employee_id>', views.employee_delete, name='employee_delete'),
]

