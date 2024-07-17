from django.contrib import admin
from .models import Publisher, Book, Member, Order, Review


class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'category', 'publisher'), ('num_pages', 'price', 'num_reviews')]
    list_display = ('title', 'category', 'price')


class OrderAdmin(admin.ModelAdmin):
    fields = ['books', ('member', 'status', 'order_date')]
    list_display = ('id', 'member', 'status', 'order_date', 'total_items')


admin.site.register(Publisher)
# admin.site.register(Book)
admin.site.register(Book, BookAdmin)
admin.site.register(Member)
# admin.site.register(Order)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
