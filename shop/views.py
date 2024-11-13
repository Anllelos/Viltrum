from django.shortcuts import render, get_object_or_404, redirect
from users.forms import SponsorProductsForm  # Importamos el formulario existente
from .models import Product
from django.contrib.auth.decorators import login_required
from users.models import SponsorProducts

def product_list(request):
    products = SponsorProducts.objects.filter(is_active=True)
    return render(request, 'shop/product_list.html', {'products': products})
def product_detail(request, pk):
    """Muestra los detalles de un producto individual."""
    product = SponsorProducts.objects.filter(pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_product(request):
    """Permite a los patrocinadores agregar un nuevo producto."""
    if request.method == 'POST':
        form = SponsorProductsForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.sponsor = request.user
            product.save()
            return redirect('shop:product_list')
    else:
        form = SponsorProductsForm()
    return render(request, 'shop/add_product.html', {'form': form})
