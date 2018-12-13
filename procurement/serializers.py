from rest_framework import serializers
# CMM -- Also import the Representative model class
from procurement.models import Component, Supplier, Representative


# CMM -- Added the RepresentativeSerializer class
class RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representative
        exclude = ('created', 'updated', 'supplier')


# CMM -- Modified the SupplierSerializer class so that the representative
#        data will also appear in the JSON objects returned by the APIs.
class SupplierSerializer(serializers.ModelSerializer):
    representatives = RepresentativeSerializer(source='representative_set', required=False, many=True)

    class Meta:
        model = Supplier
        exclude = ('created', 'updated')


class ComponentSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='__str__', read_only=True)
    suppliers = SupplierSerializer(many=True, read_only=True)

    class Meta:
        model = Component
        exclude = ('created', 'updated')

