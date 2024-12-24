from django.contrib import admin

from .models import ShippingAddress, Order, OrderItem

# Register your models here.

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)


# create order Item inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


# Extend our order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    inlines = [OrderItemInline]


# unRegister Order Model
admin.site.unregister(Order)

# Register Order Model And OrderAdmin
admin.site.register(Order, OrderAdmin)
