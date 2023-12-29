from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from accounts import groups
from accounts.models import Profile

# Create your views here.
class Home(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/home.html')

class Register(View):
    referer = ''

    def get(self, request, *args, **kwargs):        
        return render(request, 'accounts/register.html')
    
    def post(self, request, *args, **kwargs):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(email=email).exists():
            print('Email already exists')
            return redirect('accounts:register')
        
        if User.objects.filter(username=username).exists():
            print('Username already in use.')
            return redirect('accounts:register')
        
        if password != password2:
            print('Passwords don\'t match.')
            return redirect('accounts:register')
        
        new_user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password
        )

        # confirm if profile is created automatically, else create it manually
        try:
            profile = Profile.objects.get(user=new_user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=new_user)
        new_user.groups.add(groups.get_groups()['fr']) # automatically add all new users to the free group
        
        return redirect('accounts:login')

class Login(View):
    # this is a placeholder for the referring page; its value will be set in the `get()` function
    referer = ''

    def get(self, request, *args, **kwargs):
        try:
            prev_url = request.GET['next']
            if prev_url not in self.__class__.referer:
                self.__class__.referer = prev_url
        except KeyError:
            self.__class__.referer = 'accounts:home'

        # print('Login referer', self.__class__.referer)
            
        if request.user.is_authenticated:
            return redirect(self.__class__.referer)

        return render(request, 'accounts/login.html')
    
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(self.__class__.referer)
        else:
            print('Invalid credentials')
            return redirect('accounts:login')
        
@method_decorator(login_required, name='dispatch')
class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:home')
    
@method_decorator(login_required, name='dispatch')
class LoginOnly(View):
    def get(self, request, *args, **kwargs):
        context = {
            'name': 'Enoch',
            'username': 'admin'
        }
        return render(request, 'accounts/login_only.html', context=context)

@method_decorator(login_required, name='dispatch')
class UpgradePlan(View):
    def get(self, request, *args, **kwargs):
        current_profile = get_object_or_404(Profile, user=request.user)
        context = {
            'profile': current_profile
        }
        return render(request, 'accounts/upgrade_plan.html', context=context)

    def post(self, request, *args, **kwargs):
        new_plan = request.POST['new_plan']
        current_profile = get_object_or_404(Profile, user=request.user)

        if current_profile.plan == new_plan:
            print("Same plans")
            return redirect('accounts:upgrade_plan')

        # update user's plan on Profile model
        current_profile.plan = new_plan
        current_profile.save(update_fields=['plan'])

        # remove user from current group and add to another group
        groups.migrate_user(request.user)

        return redirect('accounts:upgrade_plan')

class Error404(View):
    def get(self, request, *args, **kwargs):
        return render(self, 'accounts/error404.html')
    
home_view = Home.as_view()
register_view = Register.as_view()
login_view = Login.as_view()
logout_view = Logout.as_view()
login_only = LoginOnly.as_view()
upgrade_plan = UpgradePlan.as_view()
error404 = Error404.as_view()