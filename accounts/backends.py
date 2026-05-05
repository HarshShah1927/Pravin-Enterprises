from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailOrUsernameBackend(ModelBackend):
    """Authenticate users with either email address or username."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = username or kwargs.get(User.USERNAME_FIELD)
        if not identifier or not password:
            return None

        user = (
            User.objects.filter(email__iexact=identifier).order_by('id').first()
            or User.objects.filter(username__iexact=identifier).order_by('id').first()
        )
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
