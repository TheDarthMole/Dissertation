"""
 * Copyright (C) Nicholas Ruffles - All rights reserved
 * Written by Nicholas Ruffles (Nicholas.Ruffles@protonmail.com)
"""
import base64
import http.client

from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase

from apps.containers.models import Container, Image
from apps.learn.models import ExploitType

# Constants
code = open("docker_files/Dockerfiles/Java/LFI/FileReader/src/main/java/FileReader.java").read()
# code_base64 = base64.b32encode(code.encode("utf-8"))
code_base64 = base64.b64encode(bytes(code, 'utf-8')).decode("utf-8")
code_fixed = "aW1wb3J0IGphdmEuaW8uRmlsZTsKaW1wb3J0IGphdmEuaW8uRmlsZU5vdEZvdW5kRXhjZXB0aW9uOwppbXBvcnQgamF2YS51dGlsLlNjYW5uZXI7CgpwdWJsaWMgY2xhc3MgRmlsZVJlYWRlciB7CgogICAgcHJpdmF0ZSBTdHJpbmcgZmlsZU5hbWU7CgogICAgRmlsZVJlYWRlcihTdHJpbmcgZmlsZU5hbWUpIHsKICAgICAgICB0aGlzLmZpbGVOYW1lID0gZmlsZU5hbWU7CiAgICB9CgogICAgLyoqCiAgICAgKiBBIHNpbXBsZSBmaWxlIHJlYWRlcgogICAgICogQHJldHVybiBUaGUgY29udGVudHMgb2YgdGhlIGZpbGUgcHJvdmlkZWQKICAgICAqIEB0aHJvd3MgRmlsZU5vdEZvdW5kRXhjZXB0aW9uIElmIHRoZSBmaWxlIGlzIG5vdCBmb3VuZCwgb3IgaWYgdGhlIGZpbGUgc2hvdWxkIG5vdCBiZSByZWFkCiAgICAgKi8KICAgIHB1YmxpYyBTdHJpbmcgcmVhZEZpbGUoKSB0aHJvd3MgRmlsZU5vdEZvdW5kRXhjZXB0aW9uIHsKICAgICAgICAvLyBPbmx5IHJlYWQgZnJvbSBmaWxlcyBkaXJlY3RseSB3aXRoaW4gdGhlIGFzc2V0cyBkaXJlY3RvcnkKICAgICAgICBTdHJpbmcgcHJlZml4ID0gImFzc2V0cy8iOwoKICAgICAgICBpZiAodGhpcy5maWxlTmFtZS5jb250YWlucygiLyIpKSB7CiAgICAgICAgICAgIHRocm93IG5ldyBGaWxlTm90Rm91bmRFeGNlcHRpb24oKTsKICAgICAgICB9CgogICAgICAgIEZpbGUgZmlsZSA9IG5ldyBGaWxlKHByZWZpeCArIGZpbGVOYW1lKTsKICAgICAgICBTdHJpbmdCdWlsZGVyIHJldFZhbHVlID0gbmV3IFN0cmluZ0J1aWxkZXIoKTsKICAgICAgICBTY2FubmVyIHNjYW5uZXIgPSBuZXcgU2Nhbm5lcihmaWxlKTsKCiAgICAgICAgd2hpbGUgKHNjYW5uZXIuaGFzTmV4dExpbmUoKSkgewogICAgICAgICAgICAvLyBBZGQgdGhlIHRleHQgdG8gdGhlIHJldHVybiBzdHJpbmcKICAgICAgICAgICAgcmV0VmFsdWUuYXBwZW5kKHNjYW5uZXIubmV4dExpbmUoKSk7CgogICAgICAgICAgICAvLyBBZGQgYSBuZXcgbGluZSBjaGFyYWN0ZXIgaWYgdGhlcmUgaXMgYSBuZXcgbGluZSEKICAgICAgICAgICAgaWYgKHNjYW5uZXIuaGFzTmV4dExpbmUoKSkKICAgICAgICAgICAgICAgIHJldFZhbHVlLmFwcGVuZCgiXG4iKTsKICAgICAgICB9CiAgICAgICAgU3lzdGVtLm91dC5wcmludGxuKHJldFZhbHVlKTsKICAgICAgICByZXR1cm4gcmV0VmFsdWUudG9TdHJpbmcoKTsKICAgIH0KCiAgICBwdWJsaWMgc3RhdGljIHZvaWQgbWFpbihTdHJpbmdbXSBhcmdzKSB0aHJvd3MgRmlsZU5vdEZvdW5kRXhjZXB0aW9uIHsKICAgICAgICBGaWxlUmVhZGVyIGZyID0gbmV3IEZpbGVSZWFkZXIoInNhbXBsZS50eHQiKTsKCiAgICAgICAgU3lzdGVtLm91dC5wcmludGxuKGZyLnJlYWRGaWxlKCkpOwogICAgfQp9Cg=="
code_no_compile = "Q29weXJpZ2h0IE5pY2sgUnVmZmxlcyAoQyk="
description = "# Test challenge\n## SubHeading\nCan you find the vulnerability in the file reader??\n\nIf the readFile method smells something " \
              "fishy going on, then it should throw a FileNotFoundException. "


class ContainerTestCase(TestCase):
    def setUp(self):
        credentials = {
            'username': 'test_user',
            'password': 'wwGx5ZSZS3jNBvByqECx6H2pWSkqB39Z'
        }
        self.client = Client()
        user_model = get_user_model()
        self.test_exploit = ExploitType(title="example exploit",
                                        slug="example_exploit")
        self.test_exploit.save()

        self.test_challenge = Image(image_name="File Reader",
                                    image="lfi1_fileread",
                                    code=code,
                                    file_location="/source/src/main/java/FileReader.java",
                                    detailed_description=description,
                                    command="mvn test",
                                    rm_flag=True)
        self.test_challenge.save()

        self.user = user_model.objects.create_user(credentials['username'], 'test@example.com', credentials['password'])
        self.client.login(**credentials)

    def test_challenges_exists(self):
        data = self.client.get("/challenges")
        self.assertEqual(data.status_code, http.HTTPStatus.OK)

    def test_challenge_exists(self):
        data = self.client.get("/challenges")
        self.assertContains(data, "File Reader")
        self.assertContains(data, "lfi1_fileread:latest")

    def test_challenge_start(self):
        # Test to make sure that no containers exist already
        containers = Container.objects.filter(owner_id=self.user.id,
                                              container_image=self.test_challenge)
        self.assertEqual(len(containers), 0)

        data = self.client.post("/challenges/start", {"imageID": str(self.test_challenge.id)})
        containers = Container.objects.filter(owner_id=self.user.id,
                                              container_image=self.test_challenge)
        # Test to make sure the api inserted the new entry successfully
        self.assertEqual(len(containers), 1)
        self.assertEqual(data.status_code, http.HTTPStatus.FOUND)

    def test_challenge_contains_description(self):
        data = self.client.post("/challenges/start", {"imageID": str(self.test_challenge.id)})
        containers = Container.objects.filter(owner_id=self.user.id,
                                              container_image=self.test_challenge)
        self.assertEqual(len(containers), 1)
        data1 = self.client.get(f"/challenge/{containers[0].slug}")
        self.assertContains(data1, "<h1>Test challenge</h1>")
        self.assertContains(data1, "<h2>SubHeading</h2>")
        self.assertContains(data1, "<p>Can you find the vulnerability in the file reader??</p>")
        # The code is in base64 before it is decoded
        self.assertContains(data1, code_base64)

    def challenge_test(self, challenge, http_status_code, code_snippet, redirect_url, alert_message):
        data = self.client.post("/challenges/start", {"imageID": str(self.test_challenge.id)})
        container = Container.objects.filter(owner_id=self.user.id,
                                             container_image=challenge
                                             ).first()
        self.assertIsNotNone(container)
        data = self.client.post("/challenges/submit", {"form_b64_code": code_snippet,
                                                       "form_container": container.slug})

        self.assertEqual(data.status_code, http_status_code)
        self.assertIn(redirect_url, data.headers.get("Location"))

        data1 = self.client.get(data.headers.get("Location"))
        self.assertContains(data1, alert_message)

    def test_challenge_submit_fail(self):
        self.challenge_test(self.test_challenge, http.HTTPStatus.FOUND, code_base64,
                            "/challenge/", "Your code did not pass the inspection. There are 1 JUnit failures for "
                                           "File Reader!")

    def test_challenge_submit_pass(self):
        self.challenge_test(self.test_challenge, http.HTTPStatus.FOUND, code_fixed,
                            "/challenges", "Well done! You completed File Reader!")

    def test_challenge_fails_compile(self):
        self.challenge_test(self.test_challenge, http.HTTPStatus.FOUND, code_no_compile,
                            "/challenge/",
                            "Your code failed to compile!")
