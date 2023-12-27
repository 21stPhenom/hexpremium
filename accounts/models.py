from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    plan_options = [
        ('fr', 'free'),
        ('bc', 'basic'),
        ('pr', 'pro'),
        ('pm', 'premium')
    ]
    __plan_ranking = {
        'fr': 1,
        'bc': 2,
        'pr': 3,
        'pm': 4
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(verbose_name='profile plan', max_length=7, choices=plan_options, default='fr')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
    
    class Meta:
        ordering = ['-date_created']

    def is_plan(self, plan_name):
     return self.plan == plan_name

    def __gt__(self, other):
        assert isinstance(other, self.__class__), f'`other` must be an instance of {self.__class__}'
        return self.__plan_ranking[self.plan] > other.__plan_ranking[other.plan]
    
    def get_ranks(self):
        return [rank for rank in self.__plan_ranking.keys() if self.__plan_ranking[rank] <= self.__plan_ranking[self.plan]]