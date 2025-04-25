from django.contrib import admin
from .models import Order, OrderItem
from django.utils.html import format_html
from django.urls import reverse

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 
                   'postal_code', 'city', 'total_price', 'created', 'status']
    list_filter = ['created', 'updated', 'status']
    search_fields = ['first_name', 'last_name', 'email', 'address']
    list_editable = ['status']
    inlines = [OrderItemInline]
    list_per_page = 20
    date_hierarchy = 'created'
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']

    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')
    mark_as_processing.short_description = 'Mark selected orders as Processing'

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
    mark_as_shipped.short_description = 'Mark selected orders as Shipped'

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = 'Mark selected orders as Delivered'

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = 'Mark selected orders as Cancelled'

    def view_on_site(self, obj):
        return reverse('orders:admin_order_detail', args=[obj.id])

    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }
        js = ('js/admin_order_actions.js',)
