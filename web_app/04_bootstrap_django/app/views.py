from django.views.decorators.http import require_safe, require_http_methods
from django.shortcuts import render, redirect

from app.models import TableItems, SelectFormItems
from app.forms import TableItemsForm, SelectFormItemsForm

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
    #print(f'[DEBUG] {request.method}, {request.POST}')
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
    else:
        select_items = SelectFormItems.objects.all()
        return render(request, "app/select_forms.html", {'select_items': select_items})

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
@require_safe
def side_bar(request):
    return render(request, "app/side_bar.html", {})


