from datetime import date

from django.test import TestCase
from django.urls import reverse

from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            category="full-time",
            title="Mahasiswa Universitas Indonesia",
            description="susah masuk, lebih susah keluar.",
            started_at=date(2025, 8, 1),
            ended_at=None,
        )

        self.project = Project.objects.create(
            title="Simpl saja",
            git_link="https://github.com/faeiz-ff/simpl",
            other_link="https://bahasa-simpl.pages.dev",
            description="basic description",
            started_at=date(2025, 10, 1),
            ended_at=date(2026, 1, 1),
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{
                            reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience),
                         "Mahasiswa Universitas Indonesia")
        self.assertEqual(self.experience.category, "full-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Full-Time")
        self.assertContains(response, "saat ini")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_project_model(self):
        self.assertEqual(self.project.title, "Simpl saja")
        self.assertEqual(self.project.get_time_range_str,
                         "Oct 2025 - Jan 2026")
        self.assertFalse(self.project.is_ongoing)

    def test_project_page(self):
        response = self.client.get(reverse("main:show_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project.html")
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_project_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_project"))

        self.assertContains(
            response,
            "Nantikan proyek terbaru saya yang sangat ambisius dan menarik bagi para investor."
        )
