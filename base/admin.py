from django.contrib import admin
from .models import News,Question,Option,AttemptQuestion
# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    list_display = ('created_at','title', 'description', 'image', 'url','questions_generated')
    list_filter = ('questions_generated',)
    search_fields = ('title', 'description')
    

admin.site.register(News, NewsAdmin)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(AttemptQuestion)
