from datetime import datetime
from DjangoUeditor.models import UEditorField
from django.db import models
from organization.models import CourseOrg
from organization.models import Teacher
# Create your models here.

class Course(models.Model):
    DEGREE_CHOICES = (
        ('cj','初级'),
        ('zj','中级'),
        ('qj','高级')
    )

    name = models.CharField(max_length=50,verbose_name='课程表')
    desc = models.CharField(max_length=300,verbose_name='课程描述')
    detail = UEditorField(verbose_name=u'课程详情', width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default='')
    degree = models.CharField(max_length=2,choices=DEGREE_CHOICES,verbose_name='难度')
    learn_times = models.IntegerField(verbose_name='学习时长(分钟数)',default=0)
    students = models.IntegerField(verbose_name='学习人数',default=0)
    fav_nums = models.IntegerField(verbose_name='收藏人数',default=0)
    image = models.ImageField(max_length=100,upload_to='course/%Y%m',verbose_name="封面图")
    click_nums = models.IntegerField(verbose_name="点击数",default=0)
    tag = models.CharField(verbose_name='课程标签', default='', max_length=10)
    add_time = models.DateTimeField(verbose_name="添加时间",default=datetime.now)
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构", null=True, blank=True)
    category = models.CharField("课程类别",max_length=20, default="")
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True, on_delete=models.CASCADE)
    youneed_know = models.CharField('课程须知',max_length=300,default='')
    teacher_tell = models.CharField('老师告诉你',max_length=300,default='')
    is_banner = models.BooleanField('是否轮播', default=False)

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        #获取课程的章节数
        return self.lesson_set.all().count()
    get_zj_nums.short_description = '章节数'  # 在后台显示的名称

    def get_learn_users(self):
        #获取这门课程的学习用户
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        #获取课程的章节
        return self.lesson_set.all()

    def go_to(self):
        from django.utils.safestring import mark_safe
        # mark_safe后就不会转义
        return mark_safe("<a href='https://home.cnblogs.com/u/derek1184405959/'>跳转</a>")

    go_to.short_description = "跳转"



    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name='课程',on_delete=models.CASCADE)
    name = models.CharField(max_length=100,verbose_name="章节名")
    add_time = models.DateTimeField(verbose_name="添加时间",default=datetime.now)


    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程的章节 >> {1}'.format(self.course,self.name)

    def get_lesson_vedio(self):
        #获取章节所有视频
        return self.video_set.all()

class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name='章节',on_delete=models.CASCADE)
    name = models.CharField(max_length=100,verbose_name="视频名")
    url = models.CharField( max_length=200,default='',verbose_name='访问地址')
    learn_times = models.IntegerField("学习时长(分钟数)", default=0)
    add_time = models.DateTimeField(verbose_name="添加时间",default=datetime.now)


    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name='课程',on_delete=models.CASCADE)
    name = models.CharField(max_length=100,verbose_name="名称")
    download = models.FileField(max_length=100,upload_to='course/resource/%Y%m',verbose_name="资源文件")
    add_time = models.DateTimeField(verbose_name="添加时间",default=datetime.now)


    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

class BannerCourse(Course):
    '''显示轮播课程'''
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        #这里必须设置proxy=True，这样就不会再生成一张表，同时还具有Model的功能
        proxy = True
