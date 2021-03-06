from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    passwordQuestion = models.CharField(max_length=150)
    passwordQuestionAnswer = models.CharField(max_length=150)
    # phone = models.CharField(max_length=15)
    # gender = models.CharField(max_length=10)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.FileField(blank=True)
    filepath = models.FileField()
    filterpath = models.FileField(blank=True)


class FilterSection(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="filters")
    start_time = models.FloatField()
    end_time = models.FloatField()
    word = models.CharField(max_length=10)
