from django.contrib import admin

from .models import Stock, Product


class ProductInline(admin.TabularInline):
    model = Stock.products.through
    verbose_name = 'Product'
    verbose_name_plural = 'Products'

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    inlines = [ProductInline,]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
