from django.contrib import admin
from .models import Action

@admin.register(Action)
class ActionAdminConfig(admin.ModelAdmin):
   list_display = ('user', 'action_type', 'target_object', 'created_at')
   list_filter = ('created_at', 'action_type')
   search_fields = ('body',)

   def get_queryset(self, request):
        queryset = super(ActionAdminConfig, self).get_queryset(request)
        queryset = queryset.prefetch_related('target_object')
        return queryset
