from django.contrib import admin
from .models import tabilog
from .models import Images
# Register your models here.
class ImageAdminInline(admin.StackedInline):
    model = Images
    extra = 5

class tabilogAdmin(admin.ModelAdmin):
    inlines = [ImageAdminInline]

admin.site.register(tabilog,tabilogAdmin)
admin.site.register(Images)
