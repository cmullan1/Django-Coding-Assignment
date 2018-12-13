from django.views.generic import FormView, TemplateView

from procurement.forms import ComponentSearchForm
# CMM -- Added Representative model class
from procurement.models import Supplier, Component, Representative


class ComponentSearchView(FormView):
    template_name = 'procurement/source_components.html'
    form_class = ComponentSearchForm

    component = None
    supplier_results = None

    def get_context_data(self):
        context = super().get_context_data()

        try:
            suppliers_last_updated = Supplier.objects.latest('updated').time_since_update
        except Supplier.DoesNotExist:
            suppliers_last_updated = ''

        try:
            components_last_updated = Component.objects.latest('updated').time_since_update
        except Component.DoesNotExist:
            components_last_updated = ''

# CMM -- Added "last updated" information for representatives
        try:
            representatives_last_updated = Representative.objects.latest('updated').time_since_update
        except Representative.DoesNotExist:
            representatives_last_updated = ''

# CMM -- Added count and "last updated" information for representatives
        context.update({
            'page_name': 'Component Search',
            'component': self.component,
            'supplier_results': self.supplier_results,
            'supplier_count': Supplier.objects.all().count(),
            'suppliers_last_updated': suppliers_last_updated,
            'component_count': Component.objects.all().count(),
            'components_last_updated': components_last_updated,
            'representative_count': Representative.objects.all().count(),
            'representatives_last_updated': representatives_last_updated,
        })
        return context

    def form_valid(self, form):
        self.component = form.cleaned_data['component']
        if self.component:
            self.supplier_results = self.component.suppliers.filter(is_authorized=True)

        return super(ComponentSearchView, self).get(self.request)


class DocumentationView(TemplateView):
    template_name = 'procurement/documentation.html'

    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'page_name': 'Documentation',
        })
        return context
