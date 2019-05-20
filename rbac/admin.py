from django.contrib import admin
from .models import PermissionGroup,Permission,User,Role
# Register your models here.
admin.site.register(PermissionGroup)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(User)