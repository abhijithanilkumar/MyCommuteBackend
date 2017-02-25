from django.contrib import admin
from webserver.models import *

# Register your models here.

admin.site.register(Commuter)
admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Trip)
