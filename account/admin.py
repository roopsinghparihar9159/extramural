from django.contrib import admin
from account.models import State, District, ProjectPIDetail, ProjectDetail,FinancialDetail,InstituteDetail,ReleaseBuget,UsedBalance
# Register your models here.

admin.site.register(State)
admin.site.register(District)
admin.site.register(ProjectPIDetail)
admin.site.register(ProjectDetail)
admin.site.register(FinancialDetail)
admin.site.register(InstituteDetail)
# admin.site.register(ReleaseBuget)
admin.site.register(UsedBalance)

@admin.register(ReleaseBuget)
class ReleaseBugetAdmin(admin.ModelAdmin):
    readonly_fields = ('release_no',)