from django.contrib import admin
from django.shortcuts import render_to_response, get_object_or_404

from procurement.admin_forms import ComponentAdminForm

# CMM -- Added the Representative model class
from procurement.models import Supplier, Component, Representative


class SupplierAdmin(admin.ModelAdmin):
# CMM -- Remove the representative_name and representative_email from this class as they now
#        belong to Representative and not Supplier
#    list_display = ('name', 'representative_name', 'representative_email', 'is_authorized', 'updated')
    list_display = ('name', 'is_authorized', 'updated')
    filter_horizonal = ('components',)


class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'updated')
    form = ComponentAdminForm
    source_components_template = 'procurement/admin_templates/source_components.html'

    def source_components(self, request, pk):
        component = get_object_or_404(Component, pk=pk)

        return render_to_response(self.source_components_template, {
            'title': 'Source Suppliers for: %s' % component,
            'opts': self.model._meta,
            'component': component,
            'supplier_results': component.suppliers.filter(is_authorized=True),

        })


# CMM -- Add a RepresentativeAdmin class so that representative data can be maintained from the 
#        admin site
class RepresentativeAdmin(admin.ModelAdmin):
    list_display = ('representative_name', 'representative_email', 'supplier', 'updated')


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Component, ComponentAdmin)
# CMM -- Register the RepresentativeAdmin class with the Representative model class
admin.site.register(Representative, RepresentativeAdmin)
