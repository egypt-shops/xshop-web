from django.contrib import admin


from .models import Shop, Invoice, Order, OrderItem, PricingPlan, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


class PricingPlanInline(admin.TabularInline):
    model = PricingPlan
    extra = 1
    max_num = 1


class ShopAdmin(admin.ModelAdmin):
    model = Shop
    inlines = [ProductInline, PricingPlanInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class InvoiceAdmin(admin.ModelAdmin):
    model = Invoice


class Orderadmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemInline, ]

admin.site.register(Shop, ShopAdmin)
admin.site.register(Order, Orderadmin)
admin.site.register(Invoice, InvoiceAdmin)