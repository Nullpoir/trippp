from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from trippp import settings
class UserManager(BaseUserManager):
    use_in_migration=True

    def _create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("E-mail must be given.")
        email=self.normalize_email(email)

        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(self._db)

        return user

    def create_user(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    email=models.EmailField(_('メールアドレス'), unique=True,max_length=100)
    nickname=models.CharField(_('表示名(30文字以内)'), max_length=30)

    is_staff = models.BooleanField(
        _('accout_status'),
        default=False,
        help_text=_(
            'False:regular user,True:admin'),
    )
    is_active=models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_name(self):
        return self.nickname
    def notify_user(self, subject, message, from_email=settings.EMAIL_HOST_USER, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

#    @property
#    def nickname(self):
#        return self.email
