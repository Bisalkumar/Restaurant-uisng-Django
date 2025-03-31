from django.contrib import admin
from Base_App.models import (
    FoodCategory,
    Items,
    AboutUs,
    Feedback,
    BookTable,
    Coupon,
    Offer,
)

admin.site.register(Coupon)
admin.site.register(Offer)
admin.site.register(FoodCategory)
admin.site.register(Items)
admin.site.register(AboutUs)
admin.site.register(Feedback)
admin.site.register(BookTable)
