from django.contrib import admin
from .models import *
# Register your models here.

class LikeInline(admin.TabularInline):
    model = Like
class TweetAdmin(admin.ModelAdmin):
    inlines = [LikeInline]
    save_on_top =True
    search_fields = ["id","text","user__email","user__username","images","videos"]

class LikeAdmin(admin.ModelAdmin):
    class Meta:
        model = Like

admin.site.register(Tweet,TweetAdmin)
admin.site.register(Like,LikeAdmin)
