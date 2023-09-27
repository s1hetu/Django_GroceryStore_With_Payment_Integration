# from django.urls import reverse, resolve
# from product.views import HomeView
# from store.views import register, registerbrand, AboutView, FeedbackView, profile
# from django.contrib.auth import views as auth_views
# from django.test import TestCase
#
#
# class TestUrls(TestCase):
#     def test_home_url(self):
#         url = reverse('grocery_store_home')
#         self.assertEqual(resolve(url).func.__name__, HomeView.as_view().__name__)
#
#     def test_register_user_url(self):
#         url = reverse('register-user')
#         self.assertEqual(resolve(url).func.__name__, register.__name__)
#
#     def test_register_brand_url(self):
#         url = reverse('register-brand')
#         self.assertEqual(resolve(url).func.__name__, registerbrand.__name__)
#
#     def test_about_us_url(self):
#         url = reverse('about-us')
#         self.assertEqual(resolve(url).func.__name__, AboutView.as_view().__name__)
#
#     def test_feedback_url(self):
#         url = reverse('give-feedback')
#         self.assertEqual(resolve(url).func.__name__, FeedbackView.as_view().__name__)
#
#     def test_login_url(self):
#         url = reverse('login')
#         self.assertEqual(resolve(url).func.__name__, auth_views.LoginView.as_view().__name__)
#
#     def test_logout_url(self):
#         url = reverse('logout-user')
#         self.assertEqual(resolve(url).func.__name__, auth_views.LogoutView.as_view().__name__)
#
#     def test_user_profile_url(self):
#         url = reverse('user-profile')
#         self.assertEqual(resolve(url).func.__name__, profile.__name__)
#
#     # def test_password_reset_url(self):
#     #     url = reverse('password_reset')
#     #     self.assertEqual(resolve(url).func.__name__, auth_views.PasswordResetView.as_view().__name__)
#     #
#     # def test_password_reset_done_url(self):
#     #     url = reverse('password_reset_done')
#     #     self.assertEqual(resolve(url).func.__name__, auth_views.PasswordResetDoneView.as_view().__name__)
#     #
#     # def test_password_reset_confirm_url(self):
#     #     url = reverse('password_reset_confirm', args=[uidb64, token])
#     #     self.assertEqual(resolve(url).func.__name__, auth_views.PasswordResetConfirmView.as_view().__name__)
#     #
#     # def test_password_reset_complete_url(self):
#     #     url = reverse('password_reset_complete')
#     #     self.assertEqual(resolve(url).func.__name__, auth_views.PasswordResetCompleteView.as_view().__name__)
