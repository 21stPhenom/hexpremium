from django.contrib.auth.models import Group
from django.db.utils import OperationalError
from accounts.models import Profile

try:
    from accounts.permissions import FREE_PERMISSION, BASIC_PERMISSION, PRO_PERMISSION, PREMIUM_PERMISSION
    FREE_GROUP, free_created = Group.objects.get_or_create(
        name='Free Users',
        permissions=[FREE_PERMISSION]
    )
    BASIC_GROUP, basic_created = Group.objects.get_or_create(
        name='Basic Users',
        permissions=[FREE_PERMISSION, BASIC_PERMISSION]
    )
    PRO_GROUP, pro_created = Group.objects.get_or_create(
        name='Pro Users',
        permissions=[FREE_PERMISSION, BASIC_PERMISSION, PRO_PERMISSION]
    )
    PREMIUM_GROUP, premium_created = Group.objects.get_or_create(
        name='Premium Users',
        permissions=[FREE_PERMISSION, BASIC_PERMISSION, PRO_PERMISSION, PREMIUM_PERMISSION]
    )

    groups = {
        'fr': FREE_GROUP,
        'bc': BASIC_GROUP,
        'pr': PRO_GROUP,
        'pm': PREMIUM_GROUP
    }
except Exception as e:
    print(e)

def migrate_user(user):
    current_plan = Profile.objects.get(user=user).plan
    user_group = user.groups.get()
    # print(f"Current plan: {current_plan}, current group: {user_group}")
    
    for plan, group in groups.items():
        if current_plan == plan and user_group == group:
            pass
        elif current_plan == plan and user_group != group:
            user.groups.remove(user_group)
            user.groups.add(group)
            # print(f"'{user.username}' moved from {user_group} to {group}")
        else:
            pass
        