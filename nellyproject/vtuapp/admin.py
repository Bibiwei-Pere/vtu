from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import *
import json




class CustomUserAdmin(UserAdmin):



    list_display =['username',"FullName",'email','user_type','Phone','Account_Balance','referer_username','referals','Referer_Bonus','id','last_login','date_joined','verify']
    search_fields = ('username','email','Phone','referer_username','id','user_type')

    def referals(self, obj):
        a = CustomUser.objects.get(id = obj.id)
        return Referal_list.objects.filter(user=a).count()

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('user_type','reservedaccountNumber','verify')}),
             ("Profile", {'fields': ('image_tag',"FullName",'Phone',"Account_Balance",'referer_username','Referer_Bonus',"BVN","DOB",'BankName','AccountNumber','AccountName',"Gender","State_of_origin","Local_gov_of_origin")}),
    )

    readonly_fields = ('image_tag','FullName','Address',"Account_Balance",'referer_username','Referer_Bonus','BankName','AccountNumber','AccountName',"BVN","DOB","Gender","State_of_origin","Local_gov_of_origin")


class AirtimeAdmin(admin.ModelAdmin):
    add_form=airtimeform
    list_display =['user','network','pin','amount','id','ident','Status','create_date']
    search_fields = ('id','ident','mobile_number')



class DataAdmin(admin.ModelAdmin):

    add_form=dataform
    list_display =['user','network','mobile_number','plan','id','ident','Status','medium','create_date']
    search_fields = ('user__username','mobile_number','id','ident')

class Airtime_fundingAdmin(admin.ModelAdmin):
    add_form=Airtime_fundingform
    list_display =['user',"use_to_fund_wallet",'network','mobile_number','amount',"BankName",'AccountNumber','AccountName','id','ident','Status','create_date']
    search_fields = ('user__username','id','ident')


class WithdrawAdmin(admin.ModelAdmin):
    add_form=withdrawform
    list_display =['user','accountNumber','accountName','bankName','amount','id','ident','Status','create_date']
    search_fields = ('user__username','id','ident')

class Admin_number_Admin(admin.ModelAdmin):

    list_display =['network','phone_number']

class NetworkAdmin(admin.ModelAdmin):
    list_display =['name','status']

class PlanAdmin(admin.ModelAdmin):
    list_display =['network','plansize','ussd_string','planamount','Affilliateprice','TopUserprice','apiprice']
    ordering = ['network','plan_size']

    def plansize(self, obj):

        return  str(obj.plan_size) + str(obj.plan_Volume)

    def planamount(self, obj):

        return  "₦" + str(obj.plan_amount)

    def Affilliateprice(self, obj):

        return  "₦" + str(obj.Affilliate_price)

    def TopUserprice(self, obj):

        return  "₦" + str(obj.TopUser_price)

    def apiprice(self, obj):

        return  "₦" + str(obj.api_price)


class TransferAdmin(admin.ModelAdmin):
    add_form=Transferform
    list_display =['user','receiver_username','amount','id','ident','Status','create_date']
    search_fields = ('user__username','id','ident')

class AirtimeTopupAdmin(admin.ModelAdmin):
    add_form=AirtimeTopupform
    list_display =['user','network','mobile_number','amount','id','ident','Status','medium','create_date']
    search_fields = ('user__username','id','ident','mobile_number')
    list_filter = ['network','Status']


class AirtimeswapAdmin(admin.ModelAdmin):
    add_form=Airtimeswapform
    list_display =['user','swap_from_network','swap_to_network','mobile_number','amount','Status','id','ident','create_date']
    search_fields = ('id','ident')

class CouponCodeAdmin(admin.ModelAdmin):
    list_display =['Coupon_Code','amount','Used']

class CouponPaymentAdmin(admin.ModelAdmin):
    list_display =['user','Code','amount','id','ident']
    search_fields = ('user__username','id','ident')

class TestimonialAdmin(admin.ModelAdmin):
    list_display =['user','message']

class CommentAdmin(admin.ModelAdmin):
    list_display =['Reply']

class Airtime_To_Data_Pin_Admin(admin.ModelAdmin):

    list_display =['user','network','mobile_number','pin','plan','id','ident','Status','create_date']
    search_fields = ('id','ident')

class Airtime_To_Data_PlanAdmin(admin.ModelAdmin):
    list_display =['network','plan_amount','plan_size']
    search_fields = ('id','ident')


class Automation_control_Admin(admin.ModelAdmin):
    list_display =['network_name','Network_good','id']


class Airtime_to_data_Network_Admin(admin.ModelAdmin):
    list_display =['name']


class Airtime_to_data_Plan_Admin(admin.ModelAdmin):
    list_display =['network','plan_amount','plan_size']
    search_fields = ('id','ident')

class Airtime_to_Data_tranfer_Admin(admin.ModelAdmin):
    list_display =['user','network','plan','Transfer_number','mobile_number','Status','id','ident','create_date']
    search_fields = ('id','ident')


class Bank_payment_admin(admin.ModelAdmin):
     list_display =['user','amount','ident','Status','create_date']
     search_fields = ('user__username','id','ident')


class Cable_Admin(admin.ModelAdmin):
    list_display =['name']

class CablePlan_Admin(admin.ModelAdmin):
    list_display =['cablename','package']



class Cablesub_Admin(admin.ModelAdmin):
    list_display =['user','cablename','cableplan','smart_card_number','Status','create_date','id']
    search_fields = ('user__username','id','customer_name','smart_card_number','cablename__name')
    list_filter = ['cablename']


class Billpayment_Admin(admin.ModelAdmin):
    list_display =['user','disco_name','amount','meter_number','Status','create_date','id']
    search_fields = ('user__username','id','ident','disco_name__name','meter_number')
    list_filter = ['Status']


class Percentage_Admin(admin.ModelAdmin):
    list_display =['network','percent','id']

class Topup_Percentage_Admin(admin.ModelAdmin):
    list_display =['network','percent','id']

class New_order_admin(admin.ModelAdmin):
     list_display = ['user','name','amount']
     search_fields = ('user__username','id','ident')



class Btc_rate_admin(admin.ModelAdmin):
     list_display = ['rate','amount']

class Bulk_sms_admin(admin.ModelAdmin):
     list_display = ['user','sendername','message','to','total','amount','create_date']
     search_fields = ('user__username','id','ident')


class Result_Checker_Pin_admin(admin.ModelAdmin):
     list_display = ['exam_name','amount']

class Result_Checker_Pin_order_admin(admin.ModelAdmin):
     list_display = ['user','exam_name','create_date']

class BuyBtc_admin(admin.ModelAdmin):
     list_display = ['user','Btc','amount','Btc_address','ident','Status','create_date']

class paymentgateway_admin(admin.ModelAdmin):
     list_display = ['user','reference','amount','gateway','Status','created_on']
     search_fields = ['user__username', 'reference','gateway']


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','image','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'amount','previous_balance',"after_balance",'create_date')

    search_fields = ['user__username','product',]



class upgradeuserAdmin(admin.ModelAdmin):
    list_display = ('user', 'from_package', "to_package",'amount','previous_balance',"after_balance",'create_date')
    search_fields = ['user__username',]

class RechargeAdmin(admin.ModelAdmin):
    list_display = ('network', 'amount', 'amount_to_pay')
    search_fields = ['user__username',]

class KYCAdmin(admin.ModelAdmin):
    list_display = ('user','First_Name', 'Middle_Name', 'Last_Name', 'DOB', 'Gender', 'State_of_origin', 'status')
    search_fields = ['user__username',]

    fieldsets =  (
        ("INFORMATION SUBMITED", {'fields': ('upload_passport','First_Name', 'Middle_Name', 'Last_Name', 'DOB', 'Gender', 'State_of_origin','Local_gov_of_origin',)}),
       ("BVN INFORMATION", {'fields': ("bvn_passport","FirsName",'middleName','lastName','dateOfBirth','gender')}),
        ("VERIFICATION REMARK", {'fields': ("comment","status")}),

    )
    readonly_fields =('Local_gov_of_origin',"FirsName",'dateOfBirth','gender','middleName','lastName','upload_passport',"bvn_passport",'First_Name', 'Middle_Name', 'Last_Name', 'DOB', 'Gender', 'State_of_origin')


    def FirsName(self, obj):
        print(obj.dump)
        print("musa")
        return  str(json.loads(obj.dump)["response"]["data"]["firstName"])

    def lastName(self, obj):
        print(obj.dump)
        print("musa")
        return  str(json.loads(obj.dump)["response"]["data"]["lastName"])
    def middleName(self, obj):
        print(obj.dump)
        print("musa")
        return  str(json.loads(obj.dump)["response"]["data"]["middleName"])

    def dateOfBirth(self, obj):
        print(obj.dump)
        print("musa")
        return  str(json.loads(obj.dump)["response"]["data"]["dateOfBirth"])

    def gender(self, obj):
        print(obj.dump)
        print("musa")
        return  str(json.loads(obj.dump)["response"]["data"]["gender"])


class Recharge_pin_orderadmin(admin.ModelAdmin):
    list_display =    ('user','network','network_amount','name_on_card','quantity','data_pin','id','Status',"previous_balance","after_balance","amount",'create_date' )
    search_fields = ['user__username',]

class Load_Recharge_pinAdmin(admin.ModelAdmin):
    list_display = ('dump_pin','amount','total_pin_loaded','load_code')

class Charge_userAdmin(admin.ModelAdmin):
    list_display = ('username','amount','pending_amount','balance_before','balance_after')
    search_fields = ['user__username',]

class Fund_userAdmin(admin.ModelAdmin):
    list_display = ('username','amount','balance_before','balance_after')
    search_fields = ['username',]

class Wallet_Funding_Admin(admin.ModelAdmin):
    list_display = ('user','medium','amount','previous_balance','after_balance','create_date')
    search_fields = ['user__username',]

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('user','amount','transaction_type','balance_before','balance_after')
    search_fields = ['user__username',]

class TopuserWebsiteAdmin(admin.ModelAdmin):
    list_display = ('user','Domain_name','amount','Offices_Address','Website_Customer_Care_Number',"SSL_Security")


class SmeifyAuth_admin(admin.ModelAdmin):
     list_display = ['expire_date','username','password',"token"]


class Recharge_pin_Admin(admin.ModelAdmin):
     list_display = ['network','amount','pin',"serial", 'load_code', 'available']
     list_filter = ['network','available']


admin.site.register(Recharge_pin, Recharge_pin_Admin)
admin.site.register(SmeifyAuth,SmeifyAuth_admin)
admin.site.register(TopuserWebsite,TopuserWebsiteAdmin)
admin.site.register(Load_Recharge_pin,Load_Recharge_pinAdmin)
admin.site.register(Upgrade_user,upgradeuserAdmin)
admin.site.register(Result_Checker_Pin, Result_Checker_Pin_admin)
admin.site.register(Result_Checker_Pin_order, Result_Checker_Pin_order_admin)
#admin.site.register(Post, PostAdmin)
admin.site.register( paymentgateway, paymentgateway_admin)
admin.site.register(Transactions,TransactionsAdmin)
admin.site.register(Bulk_Message,Bulk_sms_admin)
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Info_Alert)
#admin.site.register(Btc_rate,Btc_rate_admin)
#admin.site.register(Airtime,AirtimeAdmin)
admin.site.register(Data,DataAdmin)
admin.site.register(ServicesCharge)
#admin.site.register(Airtimeswap, AirtimeswapAdmin)
admin.site.register(AirtimeTopup,AirtimeTopupAdmin)
admin.site.register(Transfer,TransferAdmin)
admin.site.register(Plan,PlanAdmin)
admin.site.register(BankAccount)
admin.site.register(Network,NetworkAdmin)
admin.site.register(Withdraw, WithdrawAdmin)
admin.site.register(Couponcode, CouponCodeAdmin)
admin.site.register(CouponPayment,CouponPaymentAdmin)
admin.site.register(Admin_number,Admin_number_Admin)
admin.site.register(Airtime_funding,Airtime_fundingAdmin)
admin.site.register(Disable_Service)
#admin.site.register(Airtime_to_Data_tranfer,Airtime_to_Data_tranfer_Admin)
#admin.site.register(Airtime_to_Data_pin,Airtime_To_Data_Pin_Admin)
#admin.site.register(Automation_control,Automation_control_Admin)
admin.site.register(Recharge_pin_order,Recharge_pin_orderadmin)
admin.site.register(Bankpayment,Bank_payment_admin)
admin.site.register(Cablesub,Cablesub_Admin)
admin.site.register(CablePlan,CablePlan_Admin)
admin.site.register(Cable,Cable_Admin)
admin.site.register(Percentage,Percentage_Admin)
admin.site.register(Charge_user, Charge_userAdmin)
admin.site.register(Fund_User, Fund_userAdmin)
admin.site.register(Wallet_summary,WalletAdmin)
admin.site.register(Recharge,RechargeAdmin)
admin.site.register(SME_text)
admin.site.register(Disco_provider_name)
admin.site.register(TopupPercentage,Topup_Percentage_Admin)
admin.site.register(Billpayment,Billpayment_Admin)
admin.site.register(KYC,KYCAdmin)
admin.site.register(WebsiteConfiguration)
admin.site.register(Black_List_Phone_Number)
admin.site.register(Wallet_Funding,Wallet_Funding_Admin)


