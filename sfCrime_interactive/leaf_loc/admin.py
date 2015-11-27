from django.contrib import admin

# Register your models here.
from leaflet.admin import LeafletGeoAdmin
from .models import Dummy
from .models import LazySpot

admin.site.register(LazySpot, LeafletGeoAdmin)