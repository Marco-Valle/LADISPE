from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.conf import settings
import logging
import ldap

logger = logging.getLogger(__name__)
User = get_user_model()
ldap.set_option(ldap.OPT_REFERRALS, 0)

class CustomLDAPBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwars):

        if username is None:
            return None
        
        try:
            ldap_conn = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
        except ldap.SERVER_DOWN:
            logger.warning("LDAP server unreachable.")
            return None
        try:
            ldap_conn.simple_bind_s(username, password)
        except ldap.INVALID_CREDENTIALS:
            return None
        
        ldap_user = ldap_conn.search_s(settings.AUTH_LDAP_USER_SEARCH, ldap.SCOPE_SUBTREE, f'mail={username}')[0][1]
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
    