from django.urls import path,re_path
from .views import UserinfoView,UploadImageView,UpdatePwdView,SendEmailCodeView,UpdateEmailView

app_name = 'users'

urlpatterns = [
    path("info/", UserinfoView.as_view(),name='user_info'),
    path("image/upload", UploadImageView.as_view(), name='image_upload'),
    path("update/pwd/", UpdatePwdView.as_view(), name='update_pwd'),
    path("sendemail_code/", SendEmailCodeView.as_view(), name='sendemail_code'),
    path("update_email/", UpdateEmailView.as_view(),name='update_email'),

]