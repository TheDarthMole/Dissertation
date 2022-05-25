"""
 * Copyright (C) Nicholas Ruffles - All rights reserved
 * Written by Nicholas Ruffles (Nicholas.Ruffles@protonmail.com)
"""
import http.client

from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase

from apps.learn.models import Lesson, ExploitType, Difficulty


class LearnTestCase(TestCase):
    def setUp(self):
        credentials = {
            'username': 'test_user',
            'password': 'wwGx5ZSZS3jNBvByqECx6H2pWSkqB39Z'
        }
        user_model = get_user_model()
        self.user = user_model.objects.create_user(credentials['username'], 'test@example.com', credentials['password'])
        self.client = Client()
        self.client.login(**credentials)

        self.test_exploit = ExploitType(title="example exploit",
                                        slug="example_exploit")
        self.test_exploit.save()

        self.lesson = Lesson(title="Sample lesson",
                             slug="sample_lesson",
                             exploit_type=self.test_exploit,
                             overview="Overview here",
                             difficulty=Difficulty.normal,
                             content="# H1 Content\n\n## H2 Content\n\nThis is more content")
        self.lesson.save()

    def test_lessons_exist(self):
        data = self.client.get("/learn")
        self.assertEqual(data.status_code, http.HTTPStatus.OK)
        self.assertContains(data, "Learn")

    def test_lesson_exist(self):
        data = self.client.get(f"/lesson/{self.lesson.slug}")
        self.assertEqual(data.status_code, http.HTTPStatus.OK)

    def test_lesson_contains_lesson(self):
        data = self.client.get(f"/lesson/{self.lesson.slug}")
        self.assertContains(data, "<h1>H1 Content</h1>")
        self.assertContains(data, "<h2>H2 Content</h2>")
        self.assertContains(data, "<p>This is more content</p>")

    def test_lessons_contains_exploits(self):
        data = self.client.get("/learn")
        self.assertContains(data, self.lesson.exploit_type.title)

    def test_lesson_complete(self):
        # Check lesson isn't completed already
        data = self.client.get(f"/lesson/{self.lesson.slug}")
        self.assertContains(data, "Complete lesson")

        # Complete lesson
        data1 = self.client.get(f"/complete_lesson/{self.lesson.slug}")
        self.assertEqual(data1.status_code, http.HTTPStatus.FOUND)

        # Make sure lesson is completed
        data2 = self.client.get(f"/lesson/{self.lesson.slug}")
        self.assertContains(data2, "Lesson already completed!")
