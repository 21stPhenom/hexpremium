from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from accounts.models import Profile

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'profile'
    verbose_name_plural = 'profiles'

class UserInline(admin.TabularInline):
    model = User.groups.through

    can_delete = False
    verbose_name = 'user'
    verbose_name_plural = 'users'

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

class GroupAdmin(BaseGroupAdmin):
    inlines = [UserInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

admin.site.register(Profile)