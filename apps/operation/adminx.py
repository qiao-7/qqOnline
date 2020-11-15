import xadmin
from .models import UserAsk,UserCourse,UserMessage,CourseComments,UserFavorite

# Register your models here.

class UserAskAdmin(object):
    '''用户表单我要学习'''
    list_display = ['name','mobile','course_name','add_time']
    search_fields = ['name','mobile','course_name',]
    list_filter = ['name','mobile','course_name','add_time']
    model_icon = 'fa fa-phone'


class UserCourseAdmin(object):
    '''用户课程学习'''
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']
    model_icon = 'fa fa-bars'


class UserMessageAdmin(object):
    '''用户消息后台'''
    list_display = ['user','message','has_read','add_time']
    search_fields = ['user','message','has_read']
    list_filter = ['user','message','has_read','add_time']
    model_icon = 'fa fa-comments'


class CourseCommentAdmin(object):
    '''用户评论后台'''
    list_display = ['user','course','comments','add_time']
    search_fields = ['user','course','comments']
    list_filter = ['user','course','comments','add_time']
    model_icon = 'fa fa-comment-o'


class UserFavoriteAdmin(object):
    '''用户收藏后台'''
    list_display = ['user','fav_id','fav_type','add_time']
    search_fields = ['user','fav_id','fav_type']
    list_filter = ['user','fav_id','fav_type','add_time']
    model_icon = 'fa fa-heart'


#将后台管理器与Model进行关联注册
xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(CourseComments,CourseCommentAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
