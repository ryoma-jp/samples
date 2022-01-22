from django.views.decorators.http import require_safe, require_http_methods
from django.shortcuts import render, redirect

from app.models import TableItems, SelectFormItems, UploadFiles
from app.forms import TableItemsForm, SelectFormItemsForm, UploadFileForm

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
    
    context = {
        'upload_file_form': upload_file_form,
    }
    return render(request, "app/file_upload.html", context)

