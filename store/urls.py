from . views import register, registerbrand, FeedbackView, ChangePasswordView, AboutView, profile
# DeleteProfileView
from django.urls import path
from product.views import HomeView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', HomeView.as_view(), name="grocery_store_home"),
    path('register/', register, name='register-user'),
    path('brand-register/', registerbrand, name="register-brand"),
    path('about/', AboutView.as_view(), name='about-us'),
    path('feedback/', FeedbackView.as_view(), name='give-feedback'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('home/', HomeView.as_view(), name="grocery_store_home"),
    path('logout/', auth_views.LogoutView.as_view(template_name='store/logout.html'), name='logout-user'),
    path('profile/', profile, name='user-profile'),
    # path('delete_profile/', DeleteProfileView.as_view(), name='delete-profile'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='store/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='store/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='store/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='store/password_reset_complete.html'),
         name='password_reset_complete'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
