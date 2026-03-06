from django.contrib import admin

from .models import JobApplication, JobOffer


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company_name', 'location', 'created_by', 'created_at')
    search_fields = ('title', 'company_name', 'location', 'description')
    list_filter = ('created_at',)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'offer', 'applicant', 'created_at')
    search_fields = ('offer__title', 'applicant__username', 'applicant__nombreMostrado')
    list_filter = ('created_at',)
