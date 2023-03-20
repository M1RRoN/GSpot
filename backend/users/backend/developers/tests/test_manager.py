from developers.managers import CompanyQuerySet
from developers.models import CompanyUser
from django.test import TestCase


class CompanyEmployeeManagerTestCase(TestCase):
    def setUp(self):
        self.user1 = CompanyUser.objects.create(
            username='test_user1',
            first_name='Test',
            last_name='User',
            email='test1@test.com',
        )
        self.user2 = CompanyUser.objects.create(
            username='test_user2',
            first_name='Test',
            last_name='User',
            email='test2@test.com',
        )
        self.user3 = CompanyUser.objects.create(
            username='test_user3',
            first_name='Test',
            last_name='User',
            email='test3@test.com',
        )

    def test_get_workers_count(self):
        workers = CompanyUser.objects.get_workers_count()
        self.assertEqual(workers.count(), 3)

        companies = Company.objects.get_workers_count()
        for company in companies.values('id', 'name', 'workers_count'):
            print(company['id'], company['name'], company['workers_count'])
