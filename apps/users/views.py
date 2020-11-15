import json
from django.shortcuts import render,redirect,reverse
from django.views.generic.base import View
from django.contrib.auth import authenticate,login,logout
from .forms import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm,UploadImageForm,UserInfoForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email,EmailVerifyRecord
from django.contrib.auth.backends import  ModelBackend
from .models import UserProfile
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from course.models import Course
from django.db.models import Q
from utils.mixin_utils import LoginRequiredMixin
from django.http import HttpResponse
from django.core.paginator import PageNotAnInteger
from pure_pagination import Paginator
#邮箱和用户名都能登录
#基于ModelBackend类，因为它有authentioncates方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            #不希望用户存在两个，GET只能有一个。两个是get失败的一种原因，Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))

            #django的后台中密码加密，所以不能password==password
            #UserProfile继承的AbstracUser中有def check_password(self,raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None




class LoginView(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        #实例化
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            #获取用户提交的用户名和密码
            user_name = request.POST.get('username',None)
            pass_word = request.POST.get('password',None)
            #成功返回USER对象，失败None
            user = authenticate(username=user_name,password=pass_word)
            #如果不是Null说明验证成功
            if user is not None:
                if user.is_active:
                    #只有注册激活才能登录
                    login(request,user)
                    return render(request,'index.html')
                else:
                    return render(request,'login.html',{'msg':'没有激活账号','login_form':login_form})
            #只有当用户名或密码不存在是，才返回错误信息到前端
            else:
                return render(request,'login.html',{'msg':'用户名或密码错误','login_form':login_form})
       #form.is_valid()已经判断不合法了，所以这里不需要再返回错误信息到前端了
        else:
            return render(request,'login.html',{'login_form':login_form})



class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse("index"))

#用户注册
'''
主要实现的功能
1.用户输入邮箱、密码和验证码，点击注册按钮
2. 如果输入的不正确，提示错误信息
3. 如果正确，发送激活邮件，用户通过邮件激活后才能登录
4. 即使注册成功，没有激活的用户也不能登录
'''

class RegisterView(View):
    '''注册'''
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email',None)
            #如果用户已经存在，则提示错误信息
            if UserProfile.objects.filter(email=user_name):
                return render(request,'register.html',{'register_form':register_form,'msg':'用户已存在'})

            pass_word = request.POST.get('password',None)
            #实例化一个user_profile对象
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            #对保存到数据库的密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name,'register')
            return render(request,'login.html')
        else:
            return render(request,'register.html',{'register_form':register_form})


class ActiveUserView(View):
    def get(self,request,active_code):
        #查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                #获取到对应的邮箱
                email = record.email
                #查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active =True
                user.save()
            #验证码不对的时候跳转到激活失败的页面
        else:
            return render(request,'active_fail.html')
        #激活成功跳转到登录页面
        return render(request,'login.html')



class ForgetPwdView(View):
    '''找回密码'''
    def get(self,request):
        forget_form = ForgetPwdForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email',None)
            send_register_email(email,'forget')
            return render(request, 'send_success.html')
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})


class ResetView(View):
    '''重置密码'''

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,'password_reset.html',{"email":email})
        else:
            return render(request,'active_fail.html')
        return render(request,'login.html')

#修改密码的后台逻辑
class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{"email":email,'msg':'密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request,'login.html')

        else:
            email = request.POST.get('email','')
            return render(request,'password_reset.html',{"email":email,"modify_form":modify_form})


class UserinfoView(LoginRequiredMixin,View):
    '''用户个人信息'''
    def get(self,request):
        return render(request,'users/usercenter-info.html')

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin,View):
    '''用户图像修改'''
    def post(self,request):
        #上传的文件都在request.FILES里面获取，所以这里要多传一个这个参数
        image_form = UploadImageForm(request.POST,request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')



class UpdatePwdView(View):
    """
    个人中心修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}',  content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')

class SendEmailCodeView(View):
    '''发送邮箱修改验证码'''
    def get(self,request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}',content_type="application/json")

        send_register_email(email,'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    '''修改邮箱'''
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码无效"}', content_type='application/json')





