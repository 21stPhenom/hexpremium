from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType
from accounts.models import Profile

# profile_contenttype = ContentType.objects.get_for_model(Profile)

FREE_PERMISSION = Permission.objects.get(codename='can_view_free')
BASIC_PERMISSION = Permission.objects.get(codename='can_view_basic')
PRO_PERMISSION = Permission.objects.get(codename='can_view_pro')
PREMIUM_PERMISSION = Permission.objects.get(codename='can_view_premium')

def check_permissions(user=None, tag=None):
    assert user != None and tag != None, 'user and tag must be supplied'
    user_permissions = user.groups.get().permissions.all()
    permissions_dict = {
        'fr': FREE_PERMISSION,
        'bc': BASIC_PERMISSION,
        'pr': PRO_PERMISSION,
        'pm': PREMIUM_PERMISSION,
    }

    if tag in permissions_dict.keys() and permissions_dict[tag] in user_permissions:
        return True
    else:
        return False