import django.contrib.messages
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login

from constants import CHANGE_PASSWORD_TEMPLATE, PASSWORD_CHANGED_SUCCESSFULLY_MESSAGE, PROFILE_TEMPLATE, ABOUT_TEMPLATE, \
    FEEDBACK_TEMPLATE, BRAND_SUCCESSFULLY_CREATED_MESSAGE, REGISTER_BRAND_TEMPLATE, \
    ACCOUNT_CREATED_SUCCESSFULLY_MESSAGE, INVALID_DATA_MESSAGE, REGISTER_USER_TEMPLATE
from .forms import RegistrationForm, CustomerRegister, BrandRegister, ProfileUpdateForm, ProfileUpdateFormUser
from django.shortcuts import redirect
from .models import User
from django.views.generic import ListView
from django.contrib.auth.models import Group
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from .models import Customer
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import View


# class DeleteProfileView(View):
#     def get(self, request):
#         User.objects.get(username=request.user).delete()
#         messages.success(request, "User deleted successfully")
#         return render(request, 'store/delete_profile.html', {})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = CHANGE_PASSWORD_TEMPLATE
    success_message = PASSWORD_CHANGED_SUCCESSFULLY_MESSAGE
    success_url = reverse_lazy('user-profile')


def profile(request):
    user = request.user
    user_details = Customer.objects.filter(user=user).first()
    user_img = user_details.image.url
    customer_form = ProfileUpdateForm(instance=user_details)
    user_form = ProfileUpdateFormUser(instance=user)

    if request.method == 'POST':
        customer_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_details)
        user_form = ProfileUpdateFormUser(request.POST, instance=user)

        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('user-profile')

    context = {'user_form': user_form, 'customer_form': customer_form, 'user_img': user_img, }

    return render(request, PROFILE_TEMPLATE, context)


# class UserProfileView(DetailView):
#     # fields - ['username', 'age', 'gender', 'mobile_no', 'email']
#     template_name = 'store/profile.html'
#
#     def get_object(self):
#         print(self.request.user)
#         return self.request.user


class AboutView(TemplateView):
    template_name = ABOUT_TEMPLATE


class FeedbackView(TemplateView):
    template_name = FEEDBACK_TEMPLATE


def registerbrand(request):
    b_form = BrandRegister()
    u_form = RegistrationForm()

    if request.method == 'POST':

        b_form = BrandRegister(request.POST)
        u_form = RegistrationForm(request.POST)

        if b_form.is_valid() and u_form.is_valid():

            # b_user = b_form.save(commit=False)
            # u_user = u_form.save(commit=False)
            #
            # b_user.brand = b_user.brand.lower()
            # b_user.user = u_user
            # b_user.email = u_user.email

            u_user = u_form.save(commit=False)
            u_user.is_staff = True
            u_user.is_active = False
            u_user.save()
            b_user = b_form.save(commit=False)
            b_user.user = u_user
            b_user.brand = b_user.brand.lower()
            b_user.save()

            # u_user.save()
            # b_user.save()

            # not needed if using custom admin pannel
            # brand_admin_privileges = Group.objects.get(name='Brand_admin')
            # brand_admin_privileges.user_set.add(u_user)

            messages.success(request, BRAND_SUCCESSFULLY_CREATED_MESSAGE)
            return redirect('login')

        else:
            # messages.error(request, "Registration failed.")
            # return redirect('register-brand')
            return render(request, REGISTER_BRAND_TEMPLATE, {'c_form': b_form, 'u_form': u_form})
    else:
        # messages.error(request, "Invalid Request.")
        return render(request, REGISTER_BRAND_TEMPLATE, {'c_form': b_form, 'u_form': u_form})


def register(request):
    c_form = CustomerRegister()
    u_form = RegistrationForm()

    if request.method == 'POST':

        c_form = CustomerRegister(request.POST)
        u_form = RegistrationForm(request.POST)

        if c_form.is_valid() and u_form.is_valid():

            # c_user = c_form.save(commit=False)
            u_user = u_form.save()
            c_user = c_form.save(commit=False)
            c_user.user = u_user
            c_form.save()
            # c_user = c_form.save(commit=False)
            # c_user.user = u_user
            # c_user.email = u_user.email
            # c_user.username = u_user.username
            # u_user.save()
            # c_user.save()

            messages.success(request, ACCOUNT_CREATED_SUCCESSFULLY_MESSAGE)
            return redirect('login')

        else:
            messages.error(request, INVALID_DATA_MESSAGE)
            return render(request, REGISTER_USER_TEMPLATE, {'c_form': c_form, 'u_form': u_form})

    else:
        return render(request, REGISTER_USER_TEMPLATE, {'c_form': c_form, 'u_form': u_form})

# Permissions
# view, add, change, delete product
# view, change, delete brand
from django.shortcuts import render

# Create your views here.
