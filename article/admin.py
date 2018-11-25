from django.contrib import admin
from .models import doc
# Register your models here.
class ApplyTinyMCEtoAdmin(admin.ModelAdmin):
    class Media:
         js = (
            "https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/lazysizes/4.1.4/lazysizes.min.js",
         )
admin.site.register(doc,ApplyTinyMCEtoAdmin)
