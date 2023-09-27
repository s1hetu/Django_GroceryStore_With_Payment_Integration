from django.test import TestCase, Client
from django.urls import reverse
from store.models import Customer, Brand
from django.contrib.auth.models import User
import pytest
from pytest_django.asserts import assertTemplateUsed, assertRedirects


class BaseTest(TestCase):
    def setUp(self):
        # for user login
        self.login_url = reverse('login')

        # for user registration
        self.register_user_url = reverse('register-user')
        # for brand register
        self.register_brand_url = reverse('register-brand')

        self.customer = {
            'username': 'lalita',
            'email': 'lali@gmail.com',
            'password1': 'lalshah11@L',
            'password2': 'lalshah11@L',
            'mobile_no': '+912345676542',
            'age': 34,
            'gender': 'Female'
        }

        self.brand = {
            'username': 'ram',
            'email': 'rams1@gmail.com',
            'password1': 'ramshah11@R',
            'password2': 'ramshah11@R',
            'brand': 'ram'
        }

        return super().setUp()


class RegisterTest(BaseTest):
    # check is template is working
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/register.html')

    # check for registering user
    def test_register_user(self):
        response = self.client.post(self.register_user_url, self.customer)
        self.assertTrue(Customer.objects.filter(mobile_no=self.customer['mobile_no']).exists())
        self.assertEqual(response.status_code, 302)



    # check for registering brand
    def test_register_brand(self):
        response = self.client.post(self.register_brand_url, self.brand)
        Brand.objects.filter(brand=self.brand['brand'])
        self.assertEqual(response.status_code, 302)

    # get register brand page
    def test_register_brand_get(self):
        response = self.client.get(self.register_brand_url, self.brand)
        self.assertEqual(response.status_code, 200)


class LoginTest(BaseTest):
    # check is template is working
    def setUp(self):
        super().setUp()

        # set user for customer
        self.user1 = User.objects.create_user(username=self.customer['username'], password=self.customer['password1'])
        self.user1.email = self.customer['email']
        self.user1.save()

        self.cust1 = Customer(user=self.user1)
        self.cust1.mobile_no = self.customer['mobile_no']
        self.cust1.age = self.customer['age']
        self.cust1.gender = self.customer['gender']
        self.cust1.save()

        # set user for brand
        self.user2 = User.objects.create_user(username=self.brand['username'], password=self.brand['password1'])
        self.user2.email = self.brand['email']
        self.user2.save()

        self.brand1 = Brand(user=self.user2)
        self.brand1.brand = self.brand['brand']
        self.cust1.save()

    def test_view_page_correctly(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/login.html')

    # check if user can login
    def test_login_user(self):
        response = self.client.post(self.login_url,
                                    {'username': self.customer['username'], 'password': self.customer['password1']})
        self.assertEqual(response.status_code, 302)

    # check if brand can login
    def test_login_brand(self):
        response = self.client.post(self.login_url,
                                    {'username': self.brand['username'], 'password': self.brand['password1']})
        self.assertEqual(response.status_code, 302)


# ----------------------------------------------- Using Pytest ----------------------------------------------------------


class TestProfile:
    @pytest.mark.django_db
    def test_view_page_correctly(self, create_customer):
        # for user profile
        self.user_profile = reverse('user-profile')
        customer, client = create_customer()
        response = client.get(self.user_profile)
        assert response.status_code == 200
        assertTemplateUsed(response, 'store/profile.html')
        response = client.post(self.user_profile,
                               data={'age': 56, 'username': customer.user.username, 'mobile_no': '+919089899090'})
        assert response.status_code == 302
        assertRedirects(response, reverse('user-profile'), 302, 200)


class TestLogoutUser:
    @pytest.mark.django_db
    def test_view_page_correctly(self, create_customer):
        # for logout user
        self.logout_user = reverse('logout-user')
        customer, client = create_customer()
        response = client.get(self.logout_user)
        assert response.status_code == 200
        assertTemplateUsed(response, 'store/logout.html')


class TestLogoutUserW:
    def test_view_page_correctly(self, client):
        # for logout user
        self.logout_user = reverse('logout-user')
        # client, customer = create_customer()
        response = client.get(self.logout_user)
        assert response.status_code == 200
        assertTemplateUsed(response, 'store/logout.html')


class TestInvalidCustomer:
    @pytest.mark.django_db
    def test_invalid_data(self, client):
        u = User.objects.create_user(username='laila', password='lailashah11@L')
        c = Customer.objects.create(user=u, age='5', mobile_no='+909090909090')
        response = client.post(reverse('register-user'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'store/register.html')


class TestInvalidBrand:
    @pytest.mark.django_db
    def test_invalid_data(self, client):
        u = User.objects.create_user(username='laila', password='lailashah11@L')
        b = Brand.objects.create(user=u, brand='sopo')
        response = client.post(reverse('register-brand'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'store/register_brand.html')