from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(QuestionCategory)
admin.site.register(Question)
admin.site.register(Quiz)