from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    userid = models.PositiveIntegerField(default=0,null=True)
    username = models.CharField(max_length=80, null=True)
    phone = models.CharField(max_length=80, null=True)
    email = models.CharField(max_length=80, null=True)
    profile_pic = models.ImageField(default="profile.png", null=True, blank=True)
    sate_create = models.DateTimeField(auto_now_add=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Feature_selection(models.Model):
    user_id = models.TextField(default=0, null=True)
    task_name = models.CharField(max_length=89)
#     variableName_file', 'sent_email')
    isExternal = models.CharField(max_length=40, default="true")
    splitRatio = models.FloatField(null=True, blank=True, default =0.5,validators=[MaxValueValidator(1), MinValueValidator(0)])
    rankingAlgorithm = models.CharField(max_length=40, default='fisher')
    vipComponent = models.IntegerField( null=True,blank = True,default = 0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    rocType = models.CharField(max_length=40,  default="false")
    tupaType = models.CharField(max_length=40,  default="classtupa")
    isMotabo = models.CharField(max_length=40,  default="true")
    scaleType = models.CharField(max_length=40,  default="autoscale")
    iterations = models.IntegerField(default = 1,validators=[MaxValueValidator(100), MinValueValidator(1)])
    survivalRate = models.FloatField(null=True, blank=True, default =0.85, validators=[MaxValueValidator(1), MinValueValidator(0)])
    motaboFile = models.FileField(upload_to='featureSelection/motabo', null=True, blank=True, default=0)
    sample_file = models.FileField(upload_to='featureSelection/sample', null=True, default=0,blank=True)
    class_file = models.FileField(upload_to='featureSelection/class', default=0, blank=True, null=True)
    sampleName_file =  models.FileField(upload_to='featureSelection/sampleName', default=0, blank=True, null=True)
    variableName_file =  models.FileField(upload_to='featureSelection/variableName', default=0, blank=True, null=True)
    project_output = models.FileField(upload_to='featureSelection/out', blank=True, null=True)
    sent_email = models.BooleanField(default=False)
    graph1 = models.ImageField(upload_to='featureSelection/graph1',default=0)

    def __str__(self):
        return self.task_name
