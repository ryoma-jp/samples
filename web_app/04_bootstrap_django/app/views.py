from django.views.decorators.http import require_safe, require_http_methods
from django.shortcuts import render, redirect

from app.models import TableItems, SelectFormItems, UploadFiles, GraphSignalSelector
from app.forms import TableItemsForm, SelectFormItemsForm, UploadFileForm, GraphSignalSelectorForm

from pathlib import Path
import numpy as np
from natsort import natsorted
import math

# Create your views here.

# --- Top page ---
@require_safe
def index(request):
    return render(request, "app/index.html", {})

# --- Tables page ---
@require_safe
def tables(request):
    table_items = TableItems.objects.all()
    return render(request, "app/tables.html", {'table_items': table_items})

@require_http_methods(["GET", "POST", "HEAD"])
def table_add_item(request):
    if (request.method == 'POST'):
        form = TableItemsForm(request.POST)
        if (form.is_valid()):
            table_item = form.save(commit=False)
            table_item.save()
            return redirect('tables')
    else:
        form = TableItemsForm()
    
    return render(request, "app/tables_add_item.html", {'form': form})


# --- Select Forms page ---
@require_http_methods(["GET", "POST", "HEAD"])
def select_forms(request):
    # print(f'[DEBUG] {request.method}, {request.POST}')
    if (request.method == 'POST'):
        if ('save_check_status' in request.POST):
            checkbox = request.POST.getlist('checkbox')
            for item in SelectFormItems.objects.all():
                if (item.item_name in checkbox):
                    item.check_status = 'checked'
                else:
                    item.check_status = 'unchecked'
                item.save()
            return redirect('select_forms')
        elif ('save_radio_status' in request.POST):
            radiobox = request.POST.getlist('radiobox')
            for item in SelectFormItems.objects.all():
                if (item.item_name in radiobox):
                    item.radio_status = 'checked'
                else:
                    item.radio_status = 'unchecked'
                item.save()
            return redirect('select_forms')
        elif ('dropdown' in request.POST):
            dropdown = request.POST.getlist('dropdown')
            for item in SelectFormItems.objects.all():
                if (item.item_name in dropdown):
                    item.dropdown_status = 'checked'
                else:
                    item.dropdown_status = 'unchecked'
                item.save()
            return redirect('select_forms')
        elif ('save_dropdown_item' in request.POST):
            dropdown = request.POST.getlist('dropdownMenuButton1_submit')
            for item in SelectFormItems.objects.all():
                if (item.item_name in dropdown):
                    item.dropdown_status_with_submit = 'checked'
                else:
                    item.dropdown_status_with_submit = 'unchecked'
                item.save()
            return redirect('select_forms')
            
        else:
            return redirect('select_forms')
    else:
        select_items = SelectFormItems.objects.all()
        dropdown_text = 'Item Select'
        for item in select_items:
            if (item.dropdown_status == 'checked'):
                dropdown_text = item.item_name
        
        dropdown_text_with_submit = 'Item Select'
        for item in select_items:
            if (item.dropdown_status_with_submit == 'checked'):
                dropdown_text_with_submit = item.item_name
        
        context = {
            'select_items': select_items,
            'dropdown_text': dropdown_text,
            'dropdown_text_with_submit': dropdown_text_with_submit,
        }
        return render(request, "app/select_forms.html", context)

@require_http_methods(["GET", "POST", "HEAD"])
def select_forms_add_item(request):
    if (request.method == 'POST'):
        form = SelectFormItemsForm(request.POST)
        if (form.is_valid()):
            select_item = form.save(commit=False)
            select_item.save()
            return redirect('select_forms')
    else:
        form = SelectFormItemsForm()
    
    return render(request, "app/select_forms_add_item.html", {'form': form})

# --- Side bar page ---
class SidebarActiveContent():
    def __init__(self):
        self.home = ''
        self.orders = ''
        self.products = ''
        self.customers = ''
        
@require_safe
def side_bar_home(request):
    sidebar_status = SidebarActiveContent()
    sidebar_status.home = 'active'
    
    context = {
        'sidebar_status': sidebar_status
    }
    return render(request, "app/side_bar_home.html", context)

@require_safe
def side_bar_orders(request):
    sidebar_status = SidebarActiveContent()
    sidebar_status.orders = 'active'
    
    context = {
        'sidebar_status': sidebar_status
    }
    return render(request, "app/side_bar_orders.html", context)

@require_safe
def side_bar_products(request):
    sidebar_status = SidebarActiveContent()
    sidebar_status.products = 'active'
    
    context = {
        'sidebar_status': sidebar_status
    }
    return render(request, "app/side_bar_products.html", context)

@require_safe
def side_bar_customers(request):
    sidebar_status = SidebarActiveContent()
    sidebar_status.customers = 'active'
    
    context = {
        'sidebar_status': sidebar_status
    }
    return render(request, "app/side_bar_customers.html", context)

# --- File Upload page ---
@require_http_methods(["GET", "POST", "HEAD"])
def file_upload(request):
    # print('-------------------------------')
    # print(request)
    # print(request.POST)
    # print(request.FILES)
    # print('-------------------------------')
    if (request.method == 'POST'):
        form = UploadFileForm(request.POST, request.FILES)
        if (form.is_valid()):
            form.save()
            return redirect('file_upload')
        else:
            print('[INFO] UploadFileForm is invalid')
            upload_file_form = UploadFileForm()
    else:
        upload_file_form = UploadFileForm()
    
    uploaded_files = UploadFiles.objects.all()
    context = {
        'upload_file_form': upload_file_form,
        'uploaded_files': uploaded_files,
    }
    return render(request, "app/file_upload.html", context)

# --- Image Gallery page ---
@require_http_methods(["GET", "POST", "HEAD"])
def image_gallery(request):
    # print('-------------------------------')
    # print(request)
    # print(request.POST)
    # print('-------------------------------')
    
    if (request.method == 'POST'):
        if ('images_per_page' in request.POST):
            request.session['images_per_page'] = int(request.POST['images_per_page'])
            request.session['select_page'] = 1  # Reset
        
        if ('select_page' in request.POST):
            request.session['select_page'] = int(request.POST['select_page'])
        
        return redirect('image_gallery')
    
    image_file_list = request.session.get('image_file_list', None)  # default=None
    images_per_page = request.session.get('images_per_page', 50)    # default=50
    select_page = request.session.get('select_page', 1)             # default=1
    max_page = math.ceil(len(image_file_list) / images_per_page)
    idx = select_page * images_per_page
    page_list = np.arange(0, max_page) + 1
    
    if (image_file_list is None):
        image_path = Path('media', 'images')
        image_file_list = natsorted(list(image_path.glob('**/*.*')), key=lambda x:x.name)
        image_file_list = [f'/{str(x)}' for x in image_file_list]
        request.session['image_file_list'] = image_file_list
    image_files = image_file_list[idx:idx+images_per_page]
    
    gallery_form = {
        'images_per_page': {
            'default': images_per_page,
            'items': [50, 100, 150, 200],
        },
        'select_page': {
            'now': select_page,
            'list': page_list,
            'max': max_page,
        }
    }
    context = {
        'gallery_form': gallery_form,
        'image_files': image_files,
    }
    return render(request, "app/image_gallery.html", context)

# --- Graph page ---
@require_http_methods(["GET", "POST", "HEAD"])
def graph(request):
    def _cos(n_data=20):
        T = 2 * np.pi
        
        x = np.linspace(0, T, n_data)
        y = np.cos(x)
        
        return x, y
    
    def _sin(n_data=20):
        T = 2 * np.pi
        
        x = np.linspace(0, T, n_data)
        y = np.sin(x)
        
        return x, y
    
    try:
        signal = GraphSignalSelector.objects.get(pk=1)
    except:
        signal = None
    
    if (request.method == 'POST'):
        if (signal is not None):
            signal.signal = request.POST['signal']
            signal.save()
        else:
            GraphSignalSelector.objects.create(signal=request.POST['signal'])
        return redirect('graph')
    
    if (signal is not None):
        form = GraphSignalSelectorForm(initial={'signal': signal.signal})
        signal_type = signal.signal
    else:
        form = GraphSignalSelectorForm()
        signal_type = 'sin'   # default
    
    if (signal_type == 'sin'):
        x, y = _sin()
    else:  # elif (signal_type == 'cos'):
        x, y = _cos()

    context = {
        'form': form,
        'graph_x': list(x),
        'graph_y': list(y),
    }
    return render(request, "app/graph.html", context)


