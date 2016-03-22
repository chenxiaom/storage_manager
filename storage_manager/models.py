from django.db import models

class DEPTS(models.Model):
    name = models.CharField(max_length=80, unique=True)
    comment = models.CharField(max_length=160, blank=True, null=True)

    def __unicode__(self):
        return self.name

class UserGroups(models.Model):
    name = models.CharField(max_length=80, unique=True)
    dept = models.ForeignKey(DEPTS)
    comment = models.CharField(max_length=160, blank=True, null=True)

    def __unicode__(self):
        return self.name

class Users(models.Model):
    USER_ROLE_CHOICES = (
        ('SU', 'SuperUser'),
        ('DA', 'DeptAdmin'),
        ('CU', 'CommonUser'),
    )
    username = models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=75)
    role = models.CharField(max_length=2, choices=USER_ROLE_CHOICES, default='CU')
    dept = models.ForeignKey(DEPTS)
    group = models.ManyToManyField(UserGroups)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)
    date_joined = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.username

