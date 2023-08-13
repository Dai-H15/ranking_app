from django.contrib import admin
from . import models
# Register your models here.

class RankingModelAdmin(admin.ModelAdmin):
    list_display = ("name","posted_by","ranking","score","reason","want_to")
    search_fields = ("posted_by","name")
    list_filter = ('name', 'posted_by',"Ranking_title")

class SettingModelAdmin(admin.ModelAdmin):
    list_display = ("Ranking_title","Num_of_people","is_open","publicity","calculated")
    search_fields = ("Ranking_title",)
    list_filter = ('is_open', 'publicity',"Ranking_title","calculated")

class User_dataModelAdmin(admin.ModelAdmin):
    list_display = ("name","staff_code","score",)
    search_fields = ("name",)
    


admin.site.register(models.User_data,User_dataModelAdmin)
admin.site.register(models.Setting,SettingModelAdmin)
admin.site.register(models.Ranking,RankingModelAdmin)
