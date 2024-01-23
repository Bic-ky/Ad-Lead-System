from import_export import resources, fields
from django.contrib import admin
from .models import Province, District, Municipality, Company, Officer, Newspaper
from import_export.admin import ImportExportModelAdmin

class ProvinceResource(resources.ModelResource):
    class Meta:
        model = Province

class DistrictResource(resources.ModelResource):
    class Meta:
        model = District

class MunicipalityResource(resources.ModelResource):
    class Meta:
        model = Municipality

class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company

class OfficerResource(resources.ModelResource):
    class Meta:
        model = Officer

class NewspaperResource(resources.ModelResource):
    class Meta:
        model = Newspaper

@admin.register(Province)
class ProvinceAdmin(ImportExportModelAdmin):
    resource_class = ProvinceResource

@admin.register(District)
class DistrictAdmin(ImportExportModelAdmin):
    resource_class = DistrictResource

@admin.register(Municipality)
class MunicipalityAdmin(ImportExportModelAdmin):
    resource_class = MunicipalityResource

@admin.register(Company)
class CompanyAdmin(ImportExportModelAdmin):
    resource_class = CompanyResource

@admin.register(Officer)
class OfficerAdmin(ImportExportModelAdmin):
    resource_class = OfficerResource

@admin.register(Newspaper)
class NewspaperAdmin(ImportExportModelAdmin):
    resource_class = NewspaperResource
