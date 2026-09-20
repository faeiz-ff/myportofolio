from datetime import date

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from django.core import serializers

from main.models import Experience, Project, Blog


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

        self.blog = Blog.objects.create(
            title="Dear Diary",
            text=(
                "If compsci has a million fans, then I am one of them. If "
                "compsci has ten fans then I am one of them. If compsci has "
                "only one fan then that is me. If compsci has no fans, then "
                "that means I am no longer on earth. If the world is against "
                "compsci, then I am against the world."
            ),
            created_at=date(2026, 7, 3),
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{
                            reverse("main:experience:show")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience),
                         "Mahasiswa Universitas Indonesia")
        self.assertEqual(self.experience.category, "full-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:experience:show"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Full-Time")
        self.assertContains(response, "saat ini")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:experience:show"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_project_model(self):
        self.assertEqual(self.project.title, "Simpl saja")
        self.assertEqual(self.project.get_time_range_str,
                         "Oct 2025 - Jan 2026")
        self.assertFalse(self.project.is_ongoing)

    def test_project_page(self):
        response = self.client.get(reverse("main:project:show"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project.html")
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_project_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:project:show"))

        self.assertContains(
            response,
            "Nantikan proyek terbaru saya yang sangat ambisius dan menarik bagi para investor."
        )

    def test_blog_page(self):
        response = self.client.get(reverse("main:blog:show"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog.html")
        self.assertContains(response, self.blog.title)
        self.assertContains(response, self.blog.created_at_str)

    def test_blog_post_page(self):
        response = self.client.get(
            reverse("main:blog:show_post", kwargs={'title': self.blog.title}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog_post.html")
        self.assertContains(response, self.blog.title)
        self.assertContains(response, self.blog.text)
        self.assertContains(response, self.blog.created_at_str)

    @staticmethod
    def deserialize(response):
        instances = serializers.deserialize("json", response.content.decode("utf-8"))
        instances = [instance.object for instance in instances]

        return instances

    def test_api_json(self):
        response: HttpResponse = self.client.get(reverse("main:api:get_experiences_json"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue("application/json" in response._content_type_for_repr)
        projects = MainTest.deserialize(response)
        self.assertEqual(projects[0].title, self.experience.title)

        response: HttpResponse = self.client.get(reverse("main:api:get_projects_json"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue("application/json" in response._content_type_for_repr)
        projects = MainTest.deserialize(response)
        self.assertEqual(projects[0].title, self.project.title)

        response: HttpResponse = self.client.get(reverse("main:api:get_blogs_json"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue("application/json" in response._content_type_for_repr)
        projects = MainTest.deserialize(response)
        self.assertEqual(projects[0].title, self.blog.title)







