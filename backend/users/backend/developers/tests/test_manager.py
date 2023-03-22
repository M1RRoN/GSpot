from developers.models import CompanyUser, Company, CompanyEmployee
from django.test import TestCase


class CompanyQuerySetTests(TestCase):
    def setUp(self):
        self.user = CompanyUser.objects.create(username='test_user1', email='user@test.ru')
        self.user10 = CompanyUser.objects.create(username='test_user10', email='user10@tasd.com')
        self.company1 = Company.objects.create(title='Test Company1', created_by=self.user, email='246@qsdf.en')
        self.company2 = Company.objects.create(title='Test Company2', created_by=self.user10, email='123@qwe.org')
        self.user1 = CompanyUser.objects.create(username='Alice', company=self.company1, email='user1@test.ru')
        self.user2 = CompanyUser.objects.create(username='Bob', company=self.company1, email='user2@test.ru')
        self.user3 = CompanyUser.objects.create(username='Charlie', company=self.company1, email='user3@test.ru')
        self.user4 = CompanyUser.objects.create(username='Charli', company=self.company1, email='user10@test.ru')
        self.employee = CompanyEmployee.objects.create(user_id=self.user1, company=self.company1)
        self.employee2 = CompanyEmployee.objects.create(user_id=self.user2, company=self.company2)
        self.employee2 = CompanyEmployee.objects.create(user_id=self.user3, company=self.company1)
        self.employee2 = CompanyEmployee.objects.create(user_id=self.user4, company=self.company1)


    def test_with_workers_count(self):
        companies = Company.objects.all().order_by('created_at')
        self.assertEqual(companies[0].title, self.company1.title)
        self.assertEqual(companies[0].workers_count, 3)
        self.assertEqual(companies[1].title, self.company2.title)
        self.assertEqual(companies[1].workers_count, 1)

    def test_available_workers_for_company(self):
        users_company1 = CompanyEmployee.objects.available_workers_for_company(self.company1)
        self.assertEqual(len(users_company1), 3)

        users_company2 = CompanyEmployee.objects.available_workers_for_company(self.company2)
        self.assertEqual(len(users_company2), 1)
