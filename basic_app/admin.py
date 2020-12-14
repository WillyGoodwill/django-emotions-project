from django.contrib import admin
from basic_app.models import Emotions, Stock,AboutMyView
# Register your models here.
admin.site.register(Emotions)
admin.site.register(Stock)
admin.site.register(AboutMyView)
