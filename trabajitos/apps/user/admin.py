from django.contrib import admin
from models import Alert, Job, Find, Search, Account

class AlertAdmin(admin.ModelAdmin):
    pass

class JobAdmin(admin.ModelAdmin):
    pass

class JobAdmin(admin.ModelAdmin):
    pass

class FindAdmin(admin.ModelAdmin):
    pass

class SearchAdmin(admin.ModelAdmin):
    pass

class AccountAdmin(admin.ModelAdmin):
    pass

admin.site.register(Alert, AlertAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Find, FindAdmin)
admin.site.register(Search, SearchAdmin)
admin.site.register(Account, AccountAdmin)
