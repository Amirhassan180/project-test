from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from store.models import Product
from .cart import Cart


# Create your views here.


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products
    cart_quantity = cart.get_quantity
    cart_total = cart.get_total
    return render(request, "cart_summary.html",
                  {'cart_products': cart_products,
                   'cart_quantity': cart_quantity,
                   'cart_total': cart_total
                   })


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)

        len_carts = cart.__len__()

        resource = JsonResponse({'product name': product.name, 'len_cart': len_carts})
        return resource


def cart_delete(request):
    # get the cart
    cart = Cart(request)
    # text for post
    if request.POST.get('action') == 'post':
        # get product_id in session cart
        product_id = int(request.POST.get('product_id'))
        # Call delete function in cart
        cart.delete(product=product_id)
        messages.success(request, 'از سبد خرید حذف شد')

        resource = JsonResponse({'product': product_id})
        return resource


def cart_update(request):
    # get the cart
    cart = Cart(request)
    # text for post
    if request.POST.get('action') == 'post':
        # get product_id in session cart
        product_id = int(request.POST.get('product_id'))
        # get product_qty in session cart
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)
        messages.success(request, 'سبد خرید شما ویرایش شد')

        resource = JsonResponse({'qty': product_qty})
        return resource
        # return redirect('cart_summary')
