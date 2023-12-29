# Signal for creating groups after migrations
def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group
    from accounts.permissions import get_permissions
    permissions = get_permissions()

    FREE_GROUP, free_created = Group.objects.get_or_create(name='Free Users')
    BASIC_GROUP, basic_created = Group.objects.get_or_create(name='Basic Users')
    PRO_GROUP, pro_created = Group.objects.get_or_create(name='Pro Users')
    PREMIUM_GROUP, premium_created = Group.objects.get_or_create(name='Premium Users')

    FREE_GROUP.permissions.set([permissions['fr']])
    BASIC_GROUP.permissions.set([
        permissions['fr'],
        permissions['bc']
    ])
    PRO_GROUP.permissions.set([
        permissions['fr'],
        permissions['bc'],
        permissions['pr']
    ])
    PREMIUM_GROUP.permissions.set([
        permissions['fr'],
        permissions['bc'],
        permissions['pr'],
        permissions['pm']
    ])

def get_groups():
    from django.contrib.auth.models import Group
    FREE_GROUP = Group.objects.get(name='Free Users')
    BASIC_GROUP = Group.objects.get(name='Basic Users')
    PRO_GROUP = Group.objects.get(name='Premium Users')
    PREMIUM_GROUP = Group.objects.get(name='Pro Users')

    return {
        'fr': FREE_GROUP,
        'bc': BASIC_GROUP,
        'pr': PRO_GROUP,
        'pm': PREMIUM_GROUP
    }


def migrate_user(user):
    from accounts.models import Profile
    current_plan = Profile.objects.get(user=user).plan
    user_group = user.groups.get()
    # print(f"Current plan: {current_plan}, current group: {user_group}")
    
    groups = get_groups()

    for plan, group in groups.items():
        if current_plan == plan and user_group == group:
            pass
        elif current_plan == plan and user_group != group:
            user.groups.remove(user_group)
            user.groups.add(group)
            # print(f"'{user.username}' moved from {user_group} to {group}")
        else:
            pass
        