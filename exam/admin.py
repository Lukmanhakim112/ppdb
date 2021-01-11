from django.contrib import admin
from . import models

admin.site.register(models.Exam)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Record)
admin.site.register(models.Score)
