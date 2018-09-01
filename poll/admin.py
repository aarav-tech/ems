from django.contrib import admin
from poll.models import *

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(Tag)