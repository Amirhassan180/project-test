import datetime

from django.contrib import messages
from django.shortcuts import render, redirect

from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from user.models import Profile


def order_detail(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # get order id
        order = Order.objects.get(id=pk)
        # get order items
        order_items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST.get('shipping_status')
            # check if true or false
            if status == "true":
                order.shipped = True
                order.date_shipped = datetime.datetime.now()  # تنظیم تاریخ ارسال
            else:
                order.shipped = False
                order.date_shipped = None

            order.save()

            messages.success(request, 'وضعیت سفارش بروز رسانی شد')
            return redirect('home')

        return render(request, "payment/order_detail.html", {'order': order, 'order_items': order_items})
    else:
        messages.error(request, "دسترسی ندارید")
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)

        if request.POST:
            status = request.POST.get('shipping_status')
            num = request.POST['num']
            # Get the Oder
            order = Order.objects.filter(id=num)
            # grab Date and Time
            new = datetime.datetime.now()  # تنظیم تاریخ ارسال
            # update Order
            order.update(shipped=True, date_shipped=new)

            messages.success(request, 'وضعیت سفارش بروز رسانی شد')
            return redirect('shipped_dash')

        return render(request, "payment/not_shipped_dash.html", {'orders': orders})

    else:
        messages.success(request, "دسترسی ندارید")
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST.get('shipping_status')
            num = request.POST['num']
            # Get the Oder
            order = Order.objects.filter(id=num)
            # update Order
            order.update(shipped=False)

            messages.success(request, 'وضعیت سفارش بروز رسانی شد')
            return redirect('not_shipped_dash')

        return render(request, "payment/shipped_dash.html", {'orders': orders})

    else:
        messages.success(request, "دسترسی ندارید")
        return redirect('home')


def process_order(request):
    if request.method == 'POST':
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_products()
        quantities = cart.get_quantity()
        totals = cart.get_total()  # Assuming it's a method

        # Get billing info from the form
        payment_form = PaymentForm(request.POST or None)

        # Get Shipping Info session data
        my_shipping = request.session.get('my_shipping')

        if not my_shipping:
            messages.error(request, "اطلاعات ارسال در دسترس نیست.")
            return redirect('home')

        # Gather Order info
        full_name = my_shipping.get('shipping_full_name')
        email = my_shipping.get('shipping_email')
        shipping_address = (
            f"Address1 : {my_shipping.get('shipping_address1')}\n"
            f"Address2 : {my_shipping.get('shipping_address2')}\n"
            f"City : {my_shipping.get('shipping_city')}\n"
            f"State : {my_shipping.get('shipping_state')}\n"
            f"ZipCode : {my_shipping.get('shipping_zipCode')}\n"
            f"Country : {my_shipping.get('shipping_country')}\n"
        )

        amount_paid = totals

        # create an Order
        if request.user.is_authenticated:
            # logged in
            user = request.user
            create_order = Order(
                user=user,
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid
            )
            create_order.save()

            # Add Order Items
            order_id = create_order.pk
            for product in cart_products:
                product_id = product.id
                price = product.sale_price if product.is_sale else product.price

                for key, value in quantities.items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(
                            order_id=order_id,
                            product_id=product_id,
                            user=user,
                            quantity=value,
                            price=price,
                        )
                        create_order_item.save()

            # Clear session
            request.session.flush()

            # Clear shopping cart in the database
            Profile.objects.filter(user=request.user).update(old_cart="")

            messages.success(request, "سفارش ثبت شد")
            return redirect('home')

        else:
            create_order = Order(
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid
            )
            create_order.save()

            # Add Order Items
            order_id = create_order.pk
            for product in cart_products:
                product_id = product.id
                price = product.sale_price if product.is_sale else product.price

                for key, value in quantities.items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(
                            order_id=order_id,
                            product_id=product_id,
                            quantity=value,
                            price=price,
                        )
                        create_order_item.save()

            # Clear session
            request.session.flush()

            messages.success(request, "سفارش ثبت شد")
            return redirect('home')

    messages.error(request, "دسترسی ندارید")
    return redirect('home')


def billing_info(request):
    if request.method == "POST":
        # get the cart
        cart = Cart(request)
        cart_products = cart.get_products
        quantities = cart.get_quantity
        totals = cart.get_total()

        if request.user.is_authenticated:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
            billing_form = PaymentForm(request.POST or None)

            request.session['my_shipping'] = request.POST

            return render(request, "payment/billing_info.html", {
                'cart_products': cart_products,
                'quantities': quantities,
                'totals': totals,
                'shipping_form': shipping_form,
                'billing_form': billing_form,
            })

        else:

            shipping_form = ShippingForm(request.POST or None)
            billing_form = PaymentForm(request.POST or None)
            return render(request, "payment/billing_info.html", {
                'cart_products': cart_products,
                'quantities': quantities,
                'totals': totals,
                'shipping_form': shipping_form,
                'billing_form': billing_form,
            })


def checkout(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quantity
    totals = cart.get_total()

    # Determine the shipping form based on the user's authentication status
    if request.user.is_authenticated:
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        except ShippingAddress.DoesNotExist:
            shipping_form = ShippingForm(request.POST or None)
            messages.warning(request, "Shipping address not found. Please fill in the form.")
    else:
        shipping_form = ShippingForm(request.POST or None)

    return render(request, "payment/checkout.html", {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
        'shipping_form': shipping_form,
    })


def payment_success(request):
    return render(request, 'payment/payment_success.html')
