from django.urls import path
from app import views

urlpatterns = [
    path('tables.html', views.tables, name='tables'),
    path('add_table_item.html', views.table_add_item, name='table_add_item'),
    path('select_forms.html', views.select_forms, name='select_forms'),
    path('add_select_form_item.html', views.select_forms_add_item, name='select_forms_add_item'),
    path('side_bar.html', views.side_bar, name='side_bar'),
]
