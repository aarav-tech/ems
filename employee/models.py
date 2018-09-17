from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=20, null=False, blank=False)
    salary = models.IntegerField(null=True, blank=True)
    picture = models.ImageField(upload_to='pictures/%Y/%m/%d/', max_length=255, null=True, blank=True)

    class Meta:
        ordering = ('-salary',)

    def __str__(self):
        return "{0} - {1}".format(self.user.username, self.designation)



class EmployeeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(profile__designation="Employee")

class Employee(User):
    class Meta:
        ordering = ("username",)
        proxy = True

    objects = EmployeeManager()
    
    def full_name(self):
        return self.first_name + " - " + self.last_name


@receiver(post_save, sender=User)
def user_is_created(sender, instance, created, **kwargs):
    print(created)
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


from django.contrib.auth.models import User

@property
def full_name(self):
    return "{} {}".format(self.first_name, self.last_name)

User.add_to_class('full_name', full_name)