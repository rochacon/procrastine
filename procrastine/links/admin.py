from django.contrib import admin

from links.models import Link

class LinkAdmin(admin.ModelAdmin):
    actions = ['inactive_selected']
    fields = ('url',)
    search_fields = ('url',)

    def get_actions(self, request):
        actions = super(LinkAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
        return actions

    def inactive_selected(self, request, queryset):
        queryset.update(is_active=False)
    inactive_selected.short_description = u'Delete selected'

    def queryset(self, request):
        qs = super(LinkAdmin, self).queryset(request)
        return qs.filter(owner=request.user, is_active=True)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

admin.site.register(Link, LinkAdmin)


