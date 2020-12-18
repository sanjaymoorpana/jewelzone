from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Gold_jewelry)
admin.site.register(Diamond_jewelry)
admin.site.register(Platinum_jewelry)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Transaction)