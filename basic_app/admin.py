from django.contrib import admin
from basic_app.models import Emotions, Stock,AboutMyView,AboutMyViewOthers,AboutMyViewFuture
# Register your models here.
# class EmotionsAdmin(admin.ModelAdmin):
#     readonly_fields = ("created",)

admin.site.register(Emotions)
admin.site.register(Stock)
admin.site.register(AboutMyView)
admin.site.register(AboutMyViewOthers)
admin.site.register(AboutMyViewFuture)
