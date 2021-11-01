"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path,include
from vtuapp.views import *
from vtuapp.admin import *
from . import settings
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls
from django.views.generic.base import TemplateView

from django_otp.admin import OTPAdminSite
from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin
from django.contrib.sites.models import Site
from django.contrib.admin.models import LogEntry

class OTPAdmin(OTPAdminSite):
    pass


admin_site = OTPAdmin(name='OTPAdmin')

admin_site.register(TOTPDevice, TOTPDeviceAdmin)
admin_site.site_title = "datavilla"
admin_site.site_header = "Welcome To datavilla Admin Panel"

admin_site.register(SmeifyAuth,SmeifyAuth_admin)
admin_site.register(TopuserWebsite,TopuserWebsiteAdmin)
admin_site.register(Load_Recharge_pin,Load_Recharge_pinAdmin)
admin_site.register(Upgrade_user,upgradeuserAdmin)
admin_site.register(Result_Checker_Pin, Result_Checker_Pin_admin)
admin_site.register(Result_Checker_Pin_order, Result_Checker_Pin_order_admin)
#admin_site.register(Post, PostAdmin)
admin_site.register( paymentgateway, paymentgateway_admin)
admin_site.register(Transactions,TransactionsAdmin)
admin_site.register(Bulk_Message,Bulk_sms_admin)
admin_site.register(CustomUser,CustomUserAdmin)
admin_site.register(Info_Alert)
#admin_site.register(Btc_rate,Btc_rate_admin)
#admin_site.register(Airtime,AirtimeAdmin)
admin_site.register(Data,DataAdmin)
admin_site.register(ServicesCharge)
#admin_site.register(Airtimeswap, AirtimeswapAdmin)
admin_site.register(AirtimeTopup,AirtimeTopupAdmin)
admin_site.register(Transfer,TransferAdmin)
admin_site.register(Plan,PlanAdmin)
admin_site.register(BankAccount)
admin_site.register(Network,NetworkAdmin)
admin_site.register(Withdraw, WithdrawAdmin)
admin_site.register(Couponcode, CouponCodeAdmin)
admin_site.register(CouponPayment,CouponPaymentAdmin)
admin_site.register(Admin_number,Admin_number_Admin)
admin_site.register(Airtime_funding,Airtime_fundingAdmin)
admin_site.register(Disable_Service)
#admin_site.register(Airtime_to_Data_tranfer,Airtime_to_Data_tranfer_Admin)
#admin_site.register(Airtime_to_Data_pin,Airtime_To_Data_Pin_Admin)
#admin_site.register(Automation_control,Automation_control_Admin)
admin_site.register(Recharge_pin_order,Recharge_pin_orderadmin)
admin_site.register(Bankpayment,Bank_payment_admin)
admin_site.register(Cablesub,Cablesub_Admin)
admin_site.register(CablePlan,CablePlan_Admin)
admin_site.register(Cable,Cable_Admin)
admin_site.register(Percentage,Percentage_Admin)
admin_site.register(Charge_user, Charge_userAdmin)
admin_site.register(Fund_User, Fund_userAdmin)
admin_site.register(Wallet_summary,WalletAdmin)
admin_site.register(Recharge,RechargeAdmin)
admin_site.register(SME_text)
admin_site.register(Disco_provider_name)
admin_site.register(TopupPercentage,Topup_Percentage_Admin)
admin_site.register(Billpayment,Billpayment_Admin)
admin_site.register(KYC,KYCAdmin)
admin_site.register(WebsiteConfiguration)
admin_site.register(Black_List_Phone_Number)
admin_site.register(Wallet_Funding,Wallet_Funding_Admin)
admin_site.register(Site)
admin_site.register(LogEntry)




urlpatterns = [
    path('',WelcomeView.as_view(),name='home'),
    path('',include('vtuapp.urls')),
    path('',include('django.contrib.auth.urls')),
    path('activate/(P<uidb64>[0-9A-Za-z_\-]+)/(P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',activate, name='activate'),

    path('admin/', TemplateView.as_view(template_name='admin.html')),
    path('super-admin/', TemplateView.as_view(template_name='admin2.html')),
    path('500/server-error/page/', TemplateView.as_view(template_name='500.html')),
    path('403/bad-request-error/page/', TemplateView.as_view(template_name='403.html')),
    path('404/page-not-found-error/page/', admin.site.urls),
    #path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    ###### API URL ####
    ###### By MSORG DEVELOPERS ####
    path('api/validateiuc/', ValidateIUCAPIView.as_view()),
    path('api/validatemeter/', ValidateMeterAPIView.as_view()),
    path('api/data/<int:id>', DataAPIView.as_view()),
    path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('api/data/', DataAPIListView.as_view()),
    path('api/topup/<int:id>', AirtimeTopupAPIView.as_view()),
    path('api/cablesub/', CableSubAPIListView.as_view()),
    path('api/cablesub/<int:id>',CableSubAPIView.as_view()),
    path('api/epin/<int:id>', Result_Checker_Pin_orderAPIView.as_view()),
    path('api/epin/',Result_Checker_Pin_orderAPIListView.as_view()),
    path('api/rechargepin/',Recharge_pin_orderAPIListView.as_view()),
    path('api/pin/',PINSETUPAPIView.as_view()),
    path('api/u_webhook/',U_Webhook),
    path('api/changepin/',PINCHANGEAPIView.as_view()),
    path('api/checkpin/',PINCCHECKAPIView.as_view()),
    path('api/resetpin/',PINRESETAPIView.as_view()),
    path('api/billpayment/', BillPaymentAPIListView.as_view()),
    path('api/billpayment/<int:id>',BillPaymentAPIView.as_view()),
    path('api/topup/', AirtimeTopupAPIListView.as_view()),
    path('api/couponpayment/', CouponPaymentAPIView.as_view()),
    path('api/Airtime_funding/', Airtime_fundingAPIView.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('api/users/', UserListView.as_view()),
    path('api/history/', Api_History.as_view()),
    path('api/user/',  UserAPIView.as_view()),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('session_security/', include('session_security.urls')),
    path('api/kyc/',KYCAPIView.as_view()),
    path('api/transfer/', TransferAPIView.as_view()),
    path('api/bonus_transfer/', bonus_transferAPIView.as_view()),
    # new urls
    path('api/withdraw/', WithdrawAPIView.as_view()),
    path('api/Wallet_summary/', Wallet_summaryListView.as_view()),
    path('api/referal/', ReferalListView.as_view()),
    path('api/alert/', AlertAPIView.as_view()),
    path('api/network/', NetworkAPIView.as_view()),
    path('api/cable/', CablenameAPIView.as_view()),
    path('api/disco/', DiscoAPIView.as_view()),
    path('api/registration/', CustomUserCreate.as_view()),
    path('api/passwordchange/', PasswordChangeAPIView.as_view()),
    path('api/referal/', ReferalListView.as_view()),
    path('api/bank_notification/',BankpaymentAPIView.as_view()),

    path('api/available_recharge',available_recharge.as_view()),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)