from django.contrib import admin

from mixed.models import Document

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'context', 'is_deleted')

    def get_readonly_fields(self, request, obj=None):
        return ('slug',)

admin.site.register(Document, DocumentAdmin)
