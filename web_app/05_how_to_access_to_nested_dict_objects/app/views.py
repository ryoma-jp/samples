from django.views.decorators.http import require_safe, require_http_methods
from django.shortcuts import HttpResponse, render, redirect, get_object_or_404

from app.models import TableItems, SelectFormItems, UploadFiles, Progress
from app.forms import TableItemsForm, SelectFormItemsForm, UploadFileForm

from pathlib import Path
import numpy as np
from natsort import natsorted
import math
import json
import time

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
    
    image_loading = request.session.get('image_loading', None)  # default=None
    if (image_loading is None):
        image_loading = True
        request.session['image_loading'] = image_loading
        context = {
            'image_loading': image_loading,
        }
        return render(request, "app/image_gallery.html", context)
    
    image_file_list = request.session.get('image_file_list', None)  # default=None
    images_per_page = request.session.get('images_per_page', 50)    # default=50
    select_page = request.session.get('select_page', 1)             # default=1
    
    if (image_file_list is None):
        image_path = Path('media', 'images')
        image_file_list = natsorted(list(image_path.glob('**/*.*')), key=lambda x:x.name)
        image_file_list = [f'/{str(x)}' for x in image_file_list]
        request.session['image_file_list'] = image_file_list
        
        request.session['image_loading'] = False    # Image loading is done
    
    max_page = math.ceil(len(image_file_list) / images_per_page)
    idx = select_page * images_per_page
    page_list = np.arange(0, max_page) + 1
    image_files = image_file_list[idx:idx+images_per_page]
    
    image_loading = request.session.get('image_loading', None)  # default=None
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
        'image_loading': image_loading,
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
    
    if (request.method == 'POST'):
        request.session['signal'] = request.POST['select_signal']
        return redirect('graph')
    
    signal_type = request.session.get('signal', 'sin')  # default='sin'
    
    if (signal_type == 'sin'):
        x, y = _sin()
    else:  # elif (signal_type == 'cos'):
        x, y = _cos()

    context = {
        'signal': {
            'now': signal_type,
            'list': ['sin', 'cos'],
        },
        'graph_x': list(x),
        'graph_y': list(y),
    }
    return render(request, "app/graph.html", context)


# --- Progress page ---
@require_http_methods(["GET", "POST", "HEAD"])
def progress(request):
    context = {}
    return render(request, "app/progress.html", context)

@require_http_methods(["GET"])
def progress_setup(request):
    progress = Progress.objects.create()
    return HttpResponse(progress.pk)

@require_http_methods(["GET"])
def progress_processing(request):
    
    if 'progress_pk' in request.GET:
        progress_pk = request.GET.get("progress_pk")
        for i in range(100):
            time.sleep(0.1)
            if (i % 10 == 0):
                progress = get_object_or_404(Progress, pk=progress_pk)
                progress.now += 10
                if (progress.now >= progress.max):
                    progress.status = progress.STATUS_DONE
                progress.save()
        return redirect('progress')
    else:
        return HttpResponse("ERROR")
    

@require_http_methods(["GET"])
def progress_get(request):
    """
      指定されたプライマリキー(progress_pk)の処理進捗を返す
      progress_pk==-1の場合は，データベースに登録済みの全処理の進捗を返す
    """
    # print(f'[DEBUG] {request.GET}')
    if 'progress_pk' in request.GET:
        progress_pk = int(request.GET.get("progress_pk"))
        # print(f'[DEBUG] progress_pk = {progress_pk}')
        if (progress_pk == -1):
            progress = Progress.objects.all()
            context = {
                'num': len(progress),
                'pk': [],
                'persent':[],
                'status':[],
            }
            for progress_ in progress:
                context['pk'].append(progress_.id)
                context['persent'].append(f'{int(100 * progress_.now / progress_.max)}')
                context['status'].append(progress_.status)
            # print(f'[DEBUG]\n{context}')
            
        else:
            progress = get_object_or_404(Progress, pk=progress_pk)
            persent = f'{int(100 * progress.now / progress.max)}'
            print(f'[INFO] persent = {persent}%')
            
            context = {
                'num': 1,
                'pk': progress_pk,
                'persent': persent,
                'status': progress.status,
            }
        
        return HttpResponse(json.dumps(context, ensure_ascii=False, indent=2))
        
    else:
        return HttpResponse("ERROR")

# --- Implementations page ---
@require_http_methods(["GET", "POST", "HEAD"])
def implementations(request):

    nested_dict = {
        'key1': {
            'key1-1': {
                'val_A': '11A',
                'val_B': '11B',
                'val_C': '11C',
                'val_D': '11D',
                'val_E': '11E',
            },
            'key1-2': {
                'val_A': '12A',
                'val_B': '12B',
                'val_C': '12C',
            },
            'key1-3': {
                'val_A': '13A',
                'val_B': '13B',
                'val_C': '13C',
                'val_D': '13D',
            },
            'key1-4': {
                'val_A': '14A',
                'val_B': '14B',
            },
        },
        'key2': {
            'key2-1': {
                'val_A': '21A',
                'val_B': '21B',
            },
            'key2-2': {
                'val_A': '22A',
                'val_B': '22B',
                'val_C': '22C',
                'val_D': '22D',
            },
            'key2-3': {
                'val_A': '23A',
                'val_B': '23B',
                'val_C': '23C',
                'val_D': '23D',
                'val_E': '23E',
            },
        },
        'key3': {
            'key3-1': {
                'val_A': '31A',
                'val_B': '31B',
            },
            'key3-2': {
                'val_A': '32A',
                'val_B': '32B',
                'val_C': '32C',
                'val_D': '32D',
                'val_E': '32E',
            },
        },
    }
    
    if (request.method == 'POST'):
        if ('implementation_nd_key1' in request.POST.keys()):
            request.session['implementation_nd_key1'] = request.POST['implementation_nd_key1']
            
            if ('implementation_nd_key2' in request.session.keys()):
                del request.session['implementation_nd_key2']
            if ('implementation_nd_key3' in request.session.keys()):
                del request.session['implementation_nd_key3']
            
            return redirect('implementations')
            
        if ('implementation_nd_key2' in request.POST.keys()):
            request.session['implementation_nd_key2'] = request.POST['implementation_nd_key2']
            
            if ('implementation_nd_key3' in request.session.keys()):
                del request.session['implementation_nd_key3']
            
            return redirect('implementations')
    
        if ('implementation_nd_key3' in request.POST.keys()):
            request.session['implementation_nd_key3'] = request.POST['implementation_nd_key3']
            return redirect('implementations')
    

    key1 = request.session.get('implementation_nd_key1', None)
    key2 = request.session.get('implementation_nd_key2', None)
    key3 = request.session.get('implementation_nd_key3', None)
    
    context = {
        'nested_dict': nested_dict,
        'implementation_nd_key1': key1,
        'implementation_nd_key2': key2,
        'implementation_nd_key3': key3,
    }
    return render(request, "app/implementations.html", context)
