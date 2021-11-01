from django.db import models

class Login(models.Model):
    username = models.CharField(unique=True, max_length=20, blank=True, null=True)
    password = models.CharField(max_length=40)
    role = models.ForeignKey('Roles', models.DO_NOTHING, db_column='role', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'login'
        
class Roles(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'
