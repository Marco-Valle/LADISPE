from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpRequest
from typing import Optional
from ladiusers.models import LADIUser
import logging
import ldap


logger = logging.getLogger(__name__)
User = get_user_model()
ldap.set_option(ldap.OPT_REFERRALS, 0)


class CustomLDAPBackend(ModelBackend):
    """ Custom authentication backend to allow auth with LDAP """

    def authenticate(self,
                     request: HttpRequest,
                     username: Optional[str] = None,
                     password: Optional[str] = None,
                     **kwars) -> Optional[LADIUser]:
        """ Implementation of the required Django authenticate() method """

        if username is None:
            return None
        
        try:
            ldap_conn = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
            ldap_conn.simple_bind_s(username, password)
            ldap_user = ldap_conn.search_s(settings.AUTH_LDAP_USER_SEARCH, ldap.SCOPE_SUBTREE, f'mail={username}')[0][1]
        except ldap.INVALID_CREDENTIALS:
            return None
        except ldap.SERVER_DOWN:
            logger.warning("LDAP server unreachable.")
            return None

        try:
            user = User.objects.get(email=username)
            user.set_password(password)
        except User.DoesNotExist:
            try:
                name = ldap_user['givenName'][0].decode("utf-8").title()
                surname = ldap_user['sn'][0].decode("utf-8").title()
                email = ldap_user['mail'][0].decode("utf-8").lower()
            except TypeError:
                name = ''
                surname = ''
                email = username.lower()
            is_staff = email.find('@studenti.polito.it') == -1
            user = User.objects.create_user(email=email,
                                            password=password,
                                            name=name,
                                            surname=surname,
                                            superuser=False,
                                            staff=is_staff)
        user.save()
        return user
    