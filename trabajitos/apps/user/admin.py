from django.contrib import admin
from models import Alert, Job, Find, Search, Account, JobAlert

class AlertAdmin(admin.ModelAdmin):
    list_display = ('words', 'provinces','user')

class JobAlertAdmin(admin.ModelAdmin):
    pass

class JobAdmin(admin.ModelAdmin):
    list_display = ('find','url','title','company')

class FindAdmin(admin.ModelAdmin):
    list_display = ('search','date','time','total','efective')

class SearchAdmin(admin.ModelAdmin):
    list_display = ('words', 'provinces','user')

class AccountAdmin(admin.ModelAdmin):
    pass

admin.site.register(Alert, AlertAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobAlert, JobAlertAdmin)
admin.site.register(Find, FindAdmin)
admin.site.register(Search, SearchAdmin)
admin.site.register(Account, AccountAdmin)
