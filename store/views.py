from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import Product, Category, Brand


# Create your views here.

def search(request):
    # Determine if they filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        # Query the Products DB Model
        searched = Product.objects.filter(name__icontains=searched)  # به حروف کوچک و بزرگ حساس نیست
        # Test for Null
        if not searched:
            messages.success(request, "محصولی وجود ندارد")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})


def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'store': products})


def product_details(request, id):
    products = get_object_or_404(Product, id=id)
    # بازیابی تمام تصاویر مرتبط با محصول
    images = products.images.all()

    main_image = images.filter(is_main=True).first()  # بازیابی تصویر اصلی

    return render(request, 'product-details.html',
                  {
                      'store': products,
                      'images': images,
                      'main_image': main_image,
                  })


def category(request, name):
    name = name.replace('-', ' ')

    category = get_object_or_404(Category, name=name)
    products = Product.objects.filter(category=category)

    if not products.exists():
        messages.success(request, 'هیچ محصولی در این دسته‌بندی وجود ندارد.')
        return redirect('home')

    return render(request, 'index.html', {'store': products, 'category': category})


def category_summary(request, ):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})


def product_by_brand(request, product_brand):
    brand = get_object_or_404(Brand, name=product_brand)
    products = Product.objects.filter(brand=brand)

    if not products.exists():
        messages.success(request, 'هیچ محصولی با این نام وجود ندارد.')
        return redirect('home')

    return render(request, 'index.html', {'store': products})
