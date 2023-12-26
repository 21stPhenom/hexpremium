from django.contrib.auth.models import Group
from accounts.models import Profile

FREE_GROUP = Group.objects.get(name='Free Users')
BASIC_GROUP = Group.objects.get(name='Basic Users')
PRO_GROUP = Group.objects.get(name='Pro Users')
PREMIUM_GROUP = Group.objects.get(name='Premium Users')

groups = {
    'fr': FREE_GROUP,
    'bc': BASIC_GROUP,
    'pr': PRO_GROUP,
    'pm': PREMIUM_GROUP
}

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
        