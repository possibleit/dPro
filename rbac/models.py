from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    roles = models.ManyToManyField("Role")

    def __str__(self):
        return self.name

class Permission(models.Model):
    title = models.CharField(max_length=32,unique=True)
    url = models.CharField(max_length=128,unique=True)
    PermissionGroup = models.ForeignKey("PermissionGroup",blank = True,on_delete=models.CASCADE)
    def __str__(self):
        return '{PermissionGroup}---{Permission}'\
            .format(PermissionGroup=self.PermissionGroup,Permission=self.title)

class Role(models.Model):
    title = models.CharField(max_length=30,unique=True)
    permissions = models.ManyToManyField("Permission")
    def __str__(self):
        return self.title


class PermissionGroup(models.Model):
    #权限自引用
    title = models.CharField(max_length=32)
    parent = models.ForeignKey("PermissionGroup",null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
        title_list = [self.title]
        p = self.parent
        while p:
            title_list.insert(0,p.title)
            p = p.parent
        return '-'.join(title_list)
