from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.jobs.models import JobApplication, JobOffer


class JobsTests(TestCase):
    def test_apply_offer_does_not_create_application_for_owner(self):
        owner = get_user_model().objects.create_user(
            username='empresa_owner',
            email='empresa_owner@test.com',
            password='testpass123',
        )
        offer = JobOffer.objects.create(
            created_by=owner,
            company_name='Empresa QA',
            title='Backend Developer',
            description='Oferta de prueba',
            location='Remoto',
        )
        self.client.force_login(owner)

        response = self.client.post(reverse('jobs:apply_offer', args=[offer.pk]))

        self.assertRedirects(response, reverse('jobs:job_detail', args=[offer.pk]))
        self.assertFalse(JobApplication.objects.filter(offer=offer, applicant=owner).exists())
