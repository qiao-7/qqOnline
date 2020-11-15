from datetime import datetime
from django.db import models


# Create your models here.
class CityDict(models.Model):
    name = models.CharField(max_length=20,verbose_name="城市")
    desc = models.CharField(max_length=200,verbose_name="描述")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    ORG_CHOICES = (
        ('pxjg','培训机构'),
        ('gx','高校'),
        ('gr','个人')
    )

    name = models.CharField(max_length=50,verbose_name="机构名称",)
    desc = models.TextField(verbose_name="机构描述")
    category = models.CharField(verbose_name='机构类型',choices=ORG_CHOICES,max_length=20,default='pxjg')
    click_nums = models.IntegerField(verbose_name="点击数",default=0)
    fav_nums = models.IntegerField(verbose_name="收藏数",default=0)
    students = models.IntegerField("学习人数", default=0)
    course_nums = models.IntegerField("课程数", default=0)
    image = models.ImageField(verbose_name="logo",upload_to='org/%Y%m',max_length=100)
    address = models.CharField(max_length=150,verbose_name='机构地址')
    city = models.ForeignKey(CityDict,verbose_name='所在城市',on_delete=models.CASCADE)
    tag = models.CharField('机构标签', max_length=10, default='全国知名')
    add_time = models.DateTimeField(default=datetime.now)


    class Meta:
        verbose_name = '机构课程'
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        # 获取机构教师数
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,verbose_name='所属机构',on_delete=models.CASCADE)
    name = models.CharField(max_length=50,verbose_name="教师名")
    work_years = models.IntegerField(verbose_name='工作年限',default=0)
    work_company = models.CharField(max_length=50,verbose_name='就职公司')
    work_position = models.CharField(max_length=50,verbose_name='公司职位')
    points = models.CharField(max_length=50,verbose_name='教学特点')
    click_nums = models.IntegerField(verbose_name='点击数',default=0)
    fav_nums = models.IntegerField(verbose_name='收藏数',default=0)
    image = models.ImageField(max_length=100,default='',upload_to='teacher/%Y%m',verbose_name='头像')
    teacher_age = models.IntegerField(verbose_name='年龄', default=25)
    add_time = models.DateTimeField(default=datetime.now)


    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def get_course_nums(self):
        return self.course_set.all().count()

    def __str__(self):
        return  "[{0}]的教师：{1}".format(self.org,self.name)





