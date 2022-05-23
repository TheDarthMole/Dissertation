from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from apps.containers.models import Image, CompletedImage
from apps.learn.models import ExploitType, Lesson, CompletedLesson
import http.client


class ProgressionTest(TestCase):
    def setUp(self):
        credentials = {
            'username': 'test_user',
            'password': 'wwGx5ZSZS3jNBvByqECx6H2pWSkqB39Z'
        }
        self.client = Client()
        user_model = get_user_model()
        self.user = user_model.objects.create_user(credentials['username'], 'test@example.com', credentials['password'])
        self.client.login(**credentials)
        self.test_exploit = ExploitType(title="example exploit",
                                        slug="example_exploit")
        self.test_exploit.save()

        self.lesson = Lesson(title="What is a LFI?",
                             slug="what_is_lfi",
                             exploit_type=self.test_exploit,
                             owner=self.user,
                             overview="Overview",
                             content="Content")
        self.lesson.save()

        self.test_challenge = Image(image_name="File Reader",
                                    image="lfi1_fileread",
                                    code="CodeHere",
                                    file_location="/source/src/main/java/FileReader.java",
                                    detailed_description="Description",
                                    exploit_type=self.test_exploit,
                                    command="mvn test",
                                    rm_flag=True,
                                    pre_lesson=self.lesson)
        self.test_challenge.save()

    def test_progression_exists(self):
        data = self.client.get("/progression")
        self.assertEqual(data.status_code, http.HTTPStatus.OK)

    def test_contains_lesson(self):
        data = self.client.get("/progression")
        self.assertContains(data, self.lesson.title)

    def test_contains_challenge(self):
        data = self.client.get("/progression")
        self.assertContains(data, self.test_challenge.image_name)

    def completion_percentage(self, percentage):
        data = self.client.get("/progression")
        self.assertContains(data, percentage)

    def test_original_completion_is_zero(self):
        self.completion_percentage("example exploit - 0.0%</h3>")

    def test_progression_works(self):
        self.completion_percentage("example exploit - 0.0%</h3>")
        CompletedLesson(user=self.user, lesson=self.lesson,
                        completed=True).save()

        self.completion_percentage("example exploit - 50.0%</h3>")
        CompletedImage(user=self.user, image=self.test_challenge,
                       completed=True).save()

        self.completion_percentage("example exploit - 100.0%</h3>")
