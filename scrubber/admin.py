from django.contrib import admin

from .models import sentence
from .models import task
from .models import hit

# Register your models here.
admin.site.register(sentence);
admin.site.register(task);
admin.site.register(hit);
