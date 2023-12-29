# Signal handler for creating permissions after migrating
def create_permissions(sender, **kwargs):
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType

    from accounts.models import Profile

    profile_contenttype = ContentType.objects.get_for_model(Profile)

    FREE_PERMISSION, free_created = Permission.objects.get_or_create(
        name="Can view free content",
        content_type=profile_contenttype,
        codename='can_view_free'
    )
    BASIC_PERMISSION, basic_created = Permission.objects.get_or_create(
        name='Can view basic content',
        content_type=profile_contenttype,
        codename='can_view_basic'
    )
    PRO_PERMISSION, pro_created = Permission.objects.get_or_create(
        name='Can view basic content',
        codename='can_view_pro',
        content_type=profile_contenttype
    )
    PREMIUM_PERMISSION, premium_created = Permission.objects.get_or_create(
        name='Can view premium content',
        codename='can_view_premium',
        content_type=profile_contenttype
    )

def get_permissions():
    from django.contrib.auth.models import Permission
    FREE_PERMISSION = Permission.objects.get(codename='can_view_free')
    BASIC_PERMISSION = Permission.objects.get(codename='can_view_basic')
    PRO_PERMISSION = Permission.objects.get(codename='can_view_pro')
    PREMIUM_PERMISSION = Permission.objects.get(codename='can_view_premium')

    return {
        'fr': FREE_PERMISSION,
        'bc': BASIC_PERMISSION,
        'pr': PRO_PERMISSION,
        'pm': PREMIUM_PERMISSION,
    }

def check_permissions(user=None, tag=None):
    assert user != None and tag != None, 'user and tag must be supplied'
    
    user_permissions = user.groups.get().permissions.all()
    permissions_dict = get_permissions()

    if tag in permissions_dict.keys() and permissions_dict[tag] in user_permissions:
        return True
    else:
        return False