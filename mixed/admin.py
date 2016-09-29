from django.contrib import admin

from mixed.models import CustomConverter, Document


class CustomConverterAdmin(admin.ModelAdmin):
    list_display = ('name', 'output', 'output_type',)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'user', 'is_deleted',)

    def get_readonly_fields(self, request, obj=None):
        return ('slug',)


admin.site.register(Document, DocumentAdmin)
admin.site.register(CustomConverter, CustomConverterAdmin)
