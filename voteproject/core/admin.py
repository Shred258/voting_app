
# Register your models here.


from django.contrib import admin
from .models import Poll, Choice, Vote

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('title', 'voting_deadline', 'created_by')
    search_fields = ('title',)

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)
admin.site.register(Vote)
