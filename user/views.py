import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from store.models import Product
from .forms import RegisterForm, LoginForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from .models import Profile


# Create your views here.
def update_info(request):
    if request.user.is_authenticated:
        # Get current user
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get current user ShippingAddress Info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        # Get Original User Form
        form = UserInfoForm(request.POST or None, instance=current_user)
        # Get User ShippingForm
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if request.method == 'POST':
            if form.is_valid() or shipping_form.is_valid():
                # Save Original Form
                form.save()
                # Save Shipping Form
                shipping_form.save()
                # messages
                messages.success(request, "اطلاعات شما با موفقیت ویرایش شد.")
                return redirect('update_info')
            else:
                messages.error(request, "ویرایش اطلاعات ناموفق بود. لطفاً دوباره تلاش کنید.")
        else:
            return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:
        messages.error(request, 'برای مشاهده این صفحه باید وارد شوید.')
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been updated!')
                login(request, current_user)
                return redirect('update_user')

            else:
                for err in list(form.errors.values()):
                    messages.error(request, err)
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, 'You Must be Logged In To view that Page')
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = UpdateUserForm(request.POST, instance=current_user)
            if form.is_valid():
                form.save()
                login(request, current_user)  # این خط اختیاری است و ممکن است لازم نباشد
                messages.success(request, "اطلاعات شما با موفقیت ویرایش شد.")
                return redirect('update_user')
            else:
                messages.error(request, "ویرایش اطلاعات ناموفق بود. لطفاً دوباره تلاش کنید.")
        else:
            form = UpdateUserForm(instance=current_user)

        return render(request, 'update_user.html', {'form': form})
    else:
        messages.error(request, 'برای مشاهده این صفحه باید وارد شوید.')
        return redirect('home')


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,
                                username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'],
                                )

            if user is not None:  # If authentication is successful
                login(request, user)  # Log in the user

                # Retrieve the current user's profile
                current_user = Profile.objects.get(user=request.user)

                saved_cart = current_user.old_cart  # Get the saved old_cart from the database

                if saved_cart:  # If the saved cart exists

                    # Convert the saved cart from JSON string to a Python dictionary
                    converted_cart = json.loads(saved_cart)

                    # Initialize the cart object
                    cart = Cart(request)

                    # Add each item from the saved cart to the session cart
                    for key, value in converted_cart.items():
                        try:
                            # ارسال شیء محصول به متد db_add
                            cart.db_add(product=key, quantity=value)
                        except Product.DoesNotExist:
                            # مدیریت خطا در صورت عدم وجود محصول
                            messages.error(request, f"محصولی با شناسه {key} یافت نشد.")

                # Show a success message and redirect to the home page
                messages.success(request, f"{user.username}, welcome back!")
                return redirect("home")
            else:
                messages.error(request, "نام کاربری یا رمز عبور نادرست است.")
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_exists = User.objects.filter(
                username=form.cleaned_data['username']).exists()
            if user_exists:
                messages.success(request, "این کاربر قبلا ثبت نام کرده است.")
            else:
                # گرفتن یک کاربر جدید
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['name'],
                    last_name=form.cleaned_data['family'],
                )
                user.save()
                return redirect('home')
    else:
        form = RegisterForm()
    return render(request, "register.html", context={"form": form})


def logout_user(request):
    logout(request)
    return redirect('home')
