from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AuthenticationConfig(AppConfig):
    name = 'communicare.authentication'
    verbose_name = _('Authentication and Authorization')
