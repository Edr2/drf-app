import json
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Songs
from .serializers import SongsSerializer

# tests for views


class BaseViewTest(APITestCase):
    client = APIClient()

    def login_client(self, username="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse('create-token'),
            data=json.dumps({
                'username': username,
                'password': password
            }),
            content_type='application/json'
        )
        self.token = response.data['token']
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {}'.format(self.token)
        )
        self.client.login(username=username, password=password)
        return self.token

    @staticmethod
    def create_song(title="", artist=""):
        if title != "" and artist != "":
            Songs.objects.create(title=title, artist=artist)

    def login_a_user(self, username="", password=""):
        url = reverse(
            "auth-login",
            kwargs={"version": "v1"})
        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        )

    def setUp(self):
        # create a admin user
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )
        # add test data
        self.create_song("like glue", "sean paul")
        self.create_song("simple song", "konshens")
        self.create_song("love is wicked", "brick and lace")
        self.create_song("jam rock", "damien marley")


class AuthLoginUserTest(BaseViewTest):
    """
    Tests for the auth/login/ endpoint
    """

    def test_login_user_with_valid_credentials(self):
        response = self.login_a_user('test_user', 'testing')
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.login_a_user('anonymous', 'pass')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetAllSongsTest(BaseViewTest):
    def test_get_all_songs(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        token = self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.client.get(
            reverse("songs-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Songs.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthRegisterUserTest(APITestCase):
    """
        Tests for auth/register/ endpoint
        """

    def test_register_a_user_with_valid_data(self):
        url = reverse(
            "auth-register",
            kwargs={"version": "v1"}
        )
        response = self.client.post(
            url,
            data=json.dumps({
                    "username": "new_user",
                    "password": "new_pass",
                    "email": "new_user@mail.com"
            }),
            content_type="application/json"
        )
        # assert status code is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_a_user_with_invalid_data(self):
        url = reverse(
            "auth-register",
            kwargs={"version": "v1"}
        )
        response = self.client.post(
            url,
            data=json.dumps({
                "username": "",
                "password": "",
                "email": ""
            }),
            content_type='application/json'
        )
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)