from django.contrib import admin
from django.urls import path
from ..views import views
from ..views.login_views import UserLoginSerializer
from ..views.password_views import UserPasswordSerializer
from ..views.password_reset import ResetPasswordView
from ..views.otp_views import send_otp_to_phone, OTPVerification


urlpatterns = [
    path('user/otp', send_otp_to_phone,),
    path('admin', admin.site.urls),
    path('user/auth/otp/verify', OTPVerification.as_view(), name='otp_page'),
    path('user/auth/login', UserLoginSerializer.as_view(), name="login"),
    path('auth_user/continuation', UserPasswordSerializer.as_view(), name='validate_password'),
    path('user/session/logout', views.disable_is_active_if_user_logout, name='disabled_is_active_logout'),
    path('user/logout', views.sign_out, name='logout'),
    path('session/user/logout', views.middleware_logout, name='middleware-logout-response'),
    path('password/reset', ResetPasswordView.as_view(), name='password_reset'),

]
