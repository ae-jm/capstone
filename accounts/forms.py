from django.contrib.auth.forms import *
from django.views.generic.edit import ModelFormMixin, ProcessFormView, BaseCreateView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.contrib.auth.views import *
from accounts.models import User
# from django.contrib.auth.forms import (
#     UserCreationForm,
#     PasswordChangeForm as AuthPasswordChangeForm
# )
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserForm(forms.ModelForm):
    error_messages = {
        "password_mismatch": ("The two password fields didn’t match."),
    }
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username', ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self._meta.model.USERNAME_FIELD in self.fields:
                self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                    "autofocus"
                ] = True

        def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
            )
            return password2

        def _post_clean(self):
            super()._post_clean()
            # Validate the password after self.instance is updated with form data
            # by super().
            password = self.cleaned_data.get("password2")
            if password:
                try:
                    password_validation.validate_password(password, self.instance)

                except ValidationError as error:
                    self.add_error("password2", error)

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            if commit:
                user.save()
            return user

class LoginView(RedirectURLMixin, FormView):
    """
    Display the login form and handle the login action.
    """

    form_class = AuthenticationForm
    authentication_form = None
    template_name = "registration/login.html"
    redirect_authenticated_user = False
    extra_context = None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update(
            {
                self.redirect_field_name: self.get_redirect_url(),
                "site": current_site,
                "site_name": current_site.name,
                **(self.extra_context or {}),
            }
        )
        return context


class LogoutView(RedirectURLMixin, TemplateView):
    """
    Log out the user and display the 'You are logged out' message.
    """

    # RemovedInDjango50Warning: when the deprecation ends, remove "get" and
    # "head" from http_method_names.
    http_method_names = ["get", "head", "post", "options"]
    template_name = "registration/logged_out.html"
    extra_context = None

    # RemovedInDjango50Warning: when the deprecation ends, move
    # @method_decorator(csrf_protect) from post() to dispatch().
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == "get":
            warnings.warn(
                "Log out via GET requests is deprecated and will be removed in Django "
                "5.0. Use POST requests for logging out.",
                RemovedInDjango50Warning,
            )
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        """Logout may be done via POST."""
        auth_logout(request)
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            # Redirect to target page once the session has been cleared.
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)

    # RemovedInDjango50Warning.
    get = post

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        elif settings.LOGOUT_REDIRECT_URL:
            return resolve_url(settings.LOGOUT_REDIRECT_URL)
        else:
            return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update(
            {
                "site": current_site,
                "site_name": current_site.name,
                "title": ("Logged out"),
                "subtitle": None,
                **(self.extra_context or {}),
            }
        )
        return context



class CreateView(SingleObjectTemplateResponseMixin, BaseCreateView):
    """
    View for creating a new object, with a response rendered by a template.
    """

    template_name_suffix = "_form"

# class UserChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField(
#         label=("Password"),
#         help_text=(
#             'Raw passwords are not stored, so there is no way to see this '
#             'user’s password, but you can change the password using '
#             '<a href="{}">this form</a>.'
#         ),
#     )
#
#     class Meta:
#         model = User
#         fields = '__all__'
#         field_classes = {'username': UsernameField}
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         password = self.fields.get('password')
#         if password:
#             password.help_text = password.help_text.format('../password/')
#         user_permissions = self.fields.get('user_permissions')
#         if user_permissions:
#             user_permissions.queryset = user_permissions.queryset.select_related('content_type')

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=("Password"),
        help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    # def clean_password(self):
    #     # Regardless of what the user provides, return the initial value.
    #     # This is done here, rather than on the field, because the
    #     # field does not have access to the initial value
    #     return self.initial["password"]


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name']


# class PasswordChangeForm(AuthPasswordChangeForm):
#     # clean_new_password2 재정의 시에는 super()함수 호출이 필요하다. (부모에 존재하는 유효성 검사이다.)
#     def clean_new_password1(self):
#         # new_password1에 대한 유효성 검사를 추가로 정의한다.
#         old_password = self.cleaned_data.get('old_password')
#         new_password1 = self.cleaned_data.get('new_password1')
#
#         if old_password and new_password1:
#             if old_password == new_password1:  # 기존 암호와 같을 경우 폼 에러를 일으킨다.
#                 raise forms.ValidationError('새로운 암호는 기존 암호와 다르게 입력해주세요')
#         return new_password1

# class SetPasswordForm(forms.Form):
#     """
#     A form that lets a user change set their password without entering the old
#     password
#     """
#     error_messages = {
#         'password_mismatch': ("The two password fields didn't match."),
#     }
#     new_password1 = forms.CharField(label=("New password"),
#                                     widget=forms.PasswordInput)
#     new_password2 = forms.CharField(label=("New password confirmation"),
#                                     widget=forms.PasswordInput)
#
#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super(SetPasswordForm, self).__init__(*args, **kwargs)
#
#     def clean_new_password2(self):
#         password1 = self.cleaned_data.get('new_password1')
#         password2 = self.cleaned_data.get('new_password2')
#         if password1 and password2:
#             if password1 != password2:
#                 raise forms.ValidationError(
#                     self.error_messages['password_mismatch'],
#                     code='password_mismatch',
#                 )
#         return password2
#
#     def save(self, commit=True):
#         self.user.set_password(self.cleaned_data['new_password1'])
#         if commit:
#             self.user.save()
#         return self.user

# class PasswordChangeForm(SetPasswordForm):
#     """
#     A form that lets a user change their password by entering their old
#     password.
#     """
#     error_messages = dict(SetPasswordForm.error_messages, **{
#         'password_incorrect': ("Your old password was entered incorrectly. "
#                                 "Please enter it again."),
#     })
#     old_password = forms.CharField(label=("Old password"),
#                                    widget=forms.PasswordInput)
#
#     def clean_old_password(self):
#         """
#         Validates that the old_password field is correct.
#         """
#         old_password = self.cleaned_data["old_password"]
#         if not self.user.check_password(old_password):
#             raise forms.ValidationError(
#                 self.error_messages['password_incorrect'],
#                 code='password_incorrect',
#             )
#         return old_password
#
#
# PasswordChangeForm.base_fields = OrderedDict(
#     (k, PasswordChangeForm.base_fields[k])
#     for k in ['old_password', 'new_password1', 'new_password2']
# )