from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from account.models import State, District, ProjectPIDetail, ProjectDetail,FinancialDetail,InstituteDetail,ReleaseBuget,UsedBalance
# Register your models here.


admin.site.register(ProjectPIDetail)
admin.site.register(ProjectDetail)
admin.site.register(FinancialDetail)
admin.site.register(InstituteDetail)
# admin.site.register(ReleaseBuget)
admin.site.register(UsedBalance)


class StateAdmin(ImportExportModelAdmin):
    search_fields = ['id','name']

class DistrictAdmin1(admin.ModelAdmin):
    list_display = ('id','state','name',)
   

class DistrictAdmin(ImportExportModelAdmin,DistrictAdmin1):
    pass



@admin.register(ReleaseBuget)
class ReleaseBugetAdmin(admin.ModelAdmin):
    readonly_fields = ('release_no',)