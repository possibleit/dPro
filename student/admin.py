from django.contrib import admin
from .models import Teacher,Student,OneClass,File
# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None,{
    #         'classes' : ('wide','extrapretty',),
    #         'fields' : ('resume',),
    #     }),
    # )
    list_display = ('name','sex','email','address')

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('file','upload_method',)
admin.site.register(Teacher)
admin.site.register(OneClass)
