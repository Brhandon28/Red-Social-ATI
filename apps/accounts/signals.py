import logging

from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

logger = logging.getLogger('accounts.audit')


def _get_client_ip(request):
    if request is None:
        return 'unknown'
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = _get_client_ip(request)
    logger.info('LOGIN user=%s ip=%s', user, ip)
    ct = ContentType.objects.get_for_model(user)
    LogEntry.objects.create(
        user_id=user.pk,
        content_type_id=ct.pk,
        object_id=str(user.pk),
        object_repr=str(user),
        action_flag=ADDITION,
        change_message=f'Inicio de sesión desde {ip}',
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if user is None:
        return
    ip = _get_client_ip(request)
    logger.info('LOGOUT user=%s ip=%s', user, ip)
    ct = ContentType.objects.get_for_model(user)
    LogEntry.objects.create(
        user_id=user.pk,
        content_type_id=ct.pk,
        object_id=str(user.pk),
        object_repr=str(user),
        action_flag=ADDITION,
        change_message=f'Cierre de sesión desde {ip}',
    )


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    ip = _get_client_ip(request)
    username = credentials.get('username', 'unknown')
    logger.warning('LOGIN_FAILED user=%s ip=%s', username, ip)
