from django.contrib import admin

from .models import Education, UserWebSkill, WebSkill, WorkExperience


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'position', 'company', 'is_current')
    search_fields = ('position', 'company', 'description', 'user__username', 'user__nombreMostrado')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'degree', 'institution', 'is_current')
    search_fields = ('degree', 'institution', 'field_of_study', 'user__username', 'user__nombreMostrado')


@admin.register(WebSkill)
class WebSkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_system', 'created_by')
    search_fields = ('name',)


@admin.register(UserWebSkill)
class UserWebSkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'skill', 'created_at')
    search_fields = ('user__username', 'user__nombreMostrado', 'skill__name')
