from django.contrib import admin
from .models import Target


class TargetAdmin(admin.ModelAdmin):
    fields = ('target_description', 'target', 'start_date', 'end_date', 'done', 'priority')
    list_display = ('target_description', 'target', 'start_date', 'end_date', 'done', 'priority')


admin.site.register(Target, TargetAdmin)
