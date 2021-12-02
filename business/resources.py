from import_export import resources
from .models import *

class SaleResource(resources.ModelResource):
    class Meta:
        model = Sale
        fields = '__all__'
        exclude = ['business']