from django.contrib import admin
from .models import BoardModel,Comment,Reaction,Favorite

admin.site.register(BoardModel)
admin.site.register(Comment)
admin.site.register(Reaction)
admin.site.register(Favorite)
