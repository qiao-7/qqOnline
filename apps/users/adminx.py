import xadmin
from users.models import UserProfile,EmailVerifyRecord,Banner
from xadmin import views
# Register your models here.

class BaseSetting(object):
    '''
    切换页面主题
    '''
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    '''
    设置网站标题和页脚
    '''
    site_title = '在线教育平台'
    site_footer = 'Powered By 1906C - 2020'
    menu_style = "accordion"   #设置菜单折叠


class UserProfileAdmin(object):
    list_display = ['username','gender','mobile','address']
    search_fields = ['username','gender','mobile','address']
    list_filter = ['username','gender','mobile','address']
    model_icon = 'fa fa-user'  #改变图标
    style_fields =  {"address": "ueditor"} #富文本
    ordering = ['date_joined'] #排序
    readonly_fields = ['nick_name'] #只读字段，不能编辑
    exclude = ['date_joined']  #不显示字段
    list_editable = ['mobile'] #直接修改
    refresh_times = [3, 5]  #自动刷新（秒）


class EmailVerifyRecordAdmin(object):
    #显示的列
    list_display = ['code','email','send_type','send_time']
    #搜索字段
    search_fields = ['code','email','send_type']
    #过滤
    list_filter = ['code','email','send_type','send_time']
    model_icon = 'fa fa-envelope'


class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']
    model_icon = 'fa fa-picture-o'


xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)