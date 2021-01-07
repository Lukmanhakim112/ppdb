from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                _("This account is inactive."),
                code='inactive',
            )
