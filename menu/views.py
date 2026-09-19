from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import MenuItem, Category
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test

def menu_list(request):
    categories = Category.objects.all()
    return render(request, 'menu/menu_list.html', {'categories': categories})

def item_detail(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    return render(request, 'menu/item_detail.html', {'item': item})

def search_menu(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = MenuItem.objects.filter(
            Q(name__icontains=query) | Q(ingredients__icontains=query)
        )
    return render(request, 'menu/search_results.html', {'results': results, 'query': query})

from .forms import MenuItemForm

def is_owner(user):
    return user.is_staff

@user_passes_test(is_owner)

def item_create(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu:menu_list')
    else:
        form = MenuItemForm()
    return render(request, 'menu/item_form.html', {'form': form, 'title': 'إضافة وجبة جديدة'})

@user_passes_test(is_owner)

def item_update(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('menu:item_detail', pk=item.pk)
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'menu/item_form.html', {'form': form, 'title': 'تعديل الوجبة'})

@user_passes_test(is_owner)

def item_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('menu:menu_list')
    return render(request, 'menu/item_confirm_delete.html', {'item': item})