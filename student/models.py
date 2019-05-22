from django.db import models
import uuid,os
# Create your models here.

# Create your models here.
class Student(models.Model):#学生模板
    SEX = (
        ('男' , '男'),
        ('女' , '女'),
    )
    name = models.CharField(max_length=20, unique=False,verbose_name='名字')
    sex = models.CharField(max_length=2,choices=SEX)
    age = models.IntegerField()
    nativeplace = models.CharField(max_length=50, default='',verbose_name='籍贯')
    unitwork = models.CharField(max_length=20, default='',verbose_name='工作单位')
    business = models.CharField(max_length=20, default='',verbose_name='职务')
    address = models.CharField(max_length=50, default='',verbose_name='家庭住址')
    resume = models.TextField(max_length=1024, default='',verbose_name='个人简介（离校后）')
    email = models.CharField(max_length=30, default='',verbose_name='邮箱')

    tel_number = models.IntegerField()
    clazz = models.ForeignKey('OneClass',blank=True,on_delete=models.CASCADE,)
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

class OneClass(models.Model):#班级模板
    name = models.CharField(max_length=50)
    # student = models.ForeignKey(Student,on_delete=models.CASCADE)
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

class Teacher(models.Model):#老师模板
    name = models.CharField(max_length=20)
    sex = models.CharField(max_length=1)
    age = models.IntegerField()
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=30)
    tel_number = models.IntegerField()
    headteacher = models.ForeignKey(OneClass,on_delete=models.CASCADE)
    def __unicode__(self):
        return self.name


# Create your models here.
# Define user directory path

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("files", filename)


class File(models.Model):
    file = models.FileField(upload_to=user_directory_path, null=True)
    upload_method = models.CharField(max_length=20, verbose_name="Upload Method")