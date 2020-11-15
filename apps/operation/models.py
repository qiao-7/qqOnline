from datetime import datetime
from django.db import models
from users.models import UserProfile
from course.models import Course
# Create your models here.

class UserAsk(models.Model):
    name = models.CharField(max_length=20,verbose_name='姓名')
    mobile = models.CharField(max_length=11,verbose_name='手机')
    course_name = models.CharField(max_length=50,verbose_name='课程名')
    add_time = models.DateTimeField(verbose_name='添加时间',default=datetime.now)


    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserMessage(models.Model):
    user = models.IntegerField(verbose_name='接受用户',default=0)
    message = models.CharField(max_length=500,verbose_name='用户消息')
    has_read = models.BooleanField(verbose_name='是否已读',default=False)
    add_time = models.DateTimeField(verbose_name='添加时间',default=datetime.now)

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name='用户',on_delete=models.CASCADE)
    course = models.ForeignKey(Course,verbose_name='课程',on_delete=models.CASCADE)
    comments = models.CharField(max_length=200,verbose_name='评论')
    add_time = models.DateTimeField(verbose_name='添加时间',default=datetime.now)

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural= verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name='用户',on_delete=models.CASCADE)
    course = models.ForeignKey(Course,verbose_name='课程',on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='添加时间',default=datetime.now)

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    FAV_TYPE = (
        (1,'课程'),
        (2,'课程机构'),
        (3,'讲师')
    )
    user = models.ForeignKey(UserProfile,verbose_name='用户',on_delete=models.CASCADE)
    fav_id = models.IntegerField(verbose_name='数据Id',default=0)
    fav_type = models.IntegerField(verbose_name='收藏类型',choices=FAV_TYPE,default=1)
    add_time = models.DateTimeField(verbose_name='添加时间',default=datetime.now)


    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
