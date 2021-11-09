from django.contrib import admin
from .models import Question, User, Tag, Like, Answer
# Register your models here.

admin.site.register(Question)
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Answer)


