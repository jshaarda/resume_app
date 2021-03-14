from django.contrib import admin
from .models import Skill, Contribution, Project, Job

class SkillAdmin(admin.ModelAdmin):
    """Administration object for Skill model.
    Defines:
     - fields to be displayed in list view (list_display)
    """
    list_display = ('name', 'experience')

class ContributionAdmin(admin.ModelAdmin):
    """Administration object for Contribution model.
    Defines:
     - fields to be displayed in list view (list_display)
    """
    list_display = ('description',)

class ProjectAdmin(admin.ModelAdmin):
    """Administration object for Project model.
    Defines:
     - fields to be displayed in list view (list_display)
    """
    list_display = ('name', 'get_skill')

class JobAdmin(admin.ModelAdmin):
    """Administration object for Job model.
    Defines:
     - fields to be displayed in list view (list_display)
    """
    list_display = ('name', 'get_skill', 'get_project', 'description', 'type', 'company', 'client', 'start_date', 'end_date', 'get_contribution')  
    
# Register your models here.
admin.site.register(Skill, SkillAdmin)
admin.site.register(Contribution, ContributionAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Job, JobAdmin)