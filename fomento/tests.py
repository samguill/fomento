from random import random

from django.urls import reverse
from django_seed import Seed
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from fomento.api.views import FomentoViewSet
from fomento.models import Fomento
from account.models import Account
from django.contrib.auth.models import Group, Permission, ContentType

seeder = Seed.seeder()


class FomentoAPITestCase(APITestCase):

    def test_forbidden(self):
        url = reverse('fomento-list')
        response = self.client.get(url, format="json")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_status_ok(self):
        seeder.add_entity(Account, 1, {
            'username': 'samguill',
            'email': 'samguill@inkacode.pe',
            'password': '_password'
        })
        seeder.add_entity(Fomento, 1)
        seeder.execute()

        view = FomentoViewSet.as_view({'get': 'list'})

        factory = APIRequestFactory()
        user = Account.objects.get(username='samguill')
        request = factory.get('api/fomento/')
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class FomentoTestCase(TestCase):
    n = 20

    def create_objects(self):
        seeder.add_entity(Fomento, self.n)
        return seeder.execute()

    def test_list_fomento(self):
        self.create_objects()
        self.assertEquals(self.n, Fomento.objects.count())
