from django.urls import path
from app import views

urlpatterns = [
    path('tables/', views.tables, name='tables'),
    path('tables/add/', views.table_add_item, name='table_add_item'),
    path('select_forms/', views.select_forms, name='select_forms'),
    path('select_forms/add/', views.select_forms_add_item, name='select_forms_add_item'),
    path('side_bar/', views.side_bar_home, name='side_bar_home'),
    path('side_bar/orders/', views.side_bar_orders, name='side_bar_orders'),
    path('side_bar/products/', views.side_bar_products, name='side_bar_products'),
    path('side_bar/customers/', views.side_bar_customers, name='side_bar_customers'),
    path('file_upload/', views.file_upload, name='file_upload'),
    path('image_gallery/', views.image_gallery, name='image_gallery'),
    path('graph/', views.graph, name='graph'),
    path('progress/', views.progress, name='progress'),
    path('progress_setup/', views.progress_setup, name='progress_setup'),
    path('progress_processing/', views.progress_processing, name='progress_processing'),
    path('progress_get/', views.progress_get, name='progress_get'),
    path('implementations/', views.implementations, name='implementations'),
    path('youtube_dl/', views.youtube_dl, name='youtube_dl'),
    path('youtube_dl_img/', views.youtube_dl_img, name='youtube_dl_img'),
]
