from django.test import TestCase,  Client
from django.contrib.auth import get_user_model
from apps.containers.models import Image, CompletedImage
from apps.learn.models import ExploitType, Lesson
import http.client


class ScoreboardTest(TestCase):

    def setUp(self) -> None:
        credentials1 = {
            'username': 'test_user1',
            'password': 'wwGx5ZSZS3jNBvByqECx6H2pWSkqB39Z'
        }
        credentials2 = {
            'username': 'test_user2',
            'password': 'wwGx5ZSZS3jNBvByqECx6H2pWSkqB39Z'
        }
        self.client = Client()
        user_model = get_user_model()
        self.user1 = user_model.objects.create_user(credentials1['username'],
                                                    'test1@example.com', credentials1['password'])
        self.user2 = user_model.objects.create_user(credentials2['username'],
                                                    'test2@example.com', credentials2['password'])
        self.client.login(**credentials1)
        self.test_exploit = ExploitType(title="example exploit",
                                        slug="example_exploit")
        self.test_exploit.save()

        self.lesson = Lesson(title="What is a LFI?",
                             slug="what_is_lfi",
                             exploit_type=self.test_exploit,
                             owner=self.user1,
                             overview="Overview",
                             content="Content")
        self.lesson.save()

        self.test_challenge = Image(image_name="File Reader",
                                    image="lfi1_fileread",
                                    code="CodeHere",
                                    point_reward=30,
                                    file_location="/source/src/main/java/FileReader.java",
                                    detailed_description="Description",
                                    exploit_type=self.test_exploit,
                                    command="mvn test",
                                    rm_flag=True,
                                    pre_lesson=self.lesson)
        self.test_challenge.save()

    def test_scoreboard_exists(self):
        data = self.client.get("/scoreboard")
        self.assertEqual(data.status_code, http.HTTPStatus.OK)

    def test_users_on_scoreboard(self):
        data = self.client.get("/scoreboard")
        self.assertContains(data, self.user1.username)
        self.assertContains(data, self.user2.username)

    def test_challenge_score_works(self):
        self.assertEqual(self.user1.points, 0)
        CompletedImage(user=self.user1,
                       image=self.test_challenge,
                       completed=True).save()
        self.assertEqual(self.user1.points, self.test_challenge.point_reward)

    def test_total_progress(self):
        data = self.client.get("/scoreboard")
        self.assertContains(data, "0%</span>")

        CompletedImage(user=self.user1,
                       image=self.test_challenge,
                       completed=True).save()
        data = self.client.get("/scoreboard")
        self.assertContains(data, "50%</span>")

        CompletedImage(user=self.user1,
                       image=self.test_challenge,
                       completed=True).save()
        data = self.client.get("/scoreboard")
        self.assertContains(data, "100%</span>")


