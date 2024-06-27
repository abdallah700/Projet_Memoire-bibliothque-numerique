from django.contrib import admin

# Register your models here.

from bookstore.models import User, Book, Reservation, Chat, CancelledReservation

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Reservation)
admin.site.register(Chat)
admin.site.register(CancelledReservation)
