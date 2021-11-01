from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import json, uuid



status =(
    ('processing','processing'),
    ('failed','Failed'),
    ('successful','Successful'),
)

Airtime_choice =(
    (100 , '#100'),
    (500,'#500'),
    (1000,'#1000'),
    (5000,'#5000'),
    (1000,'#1000'),
)
Bank = (
    ('First Bank of Nigeria','First Bank of Nigeria'),
    ('UBA','UBA'),
    ('Access Bank','Access Bank'),
    ('Wema Bank','Wema Bank'),
    ('Diamond Bank','Diamond Bank'),
    ('Heritage Bank','Heritage Bank'),
    ('Skye Bank','Skye Bank'),
    ('Stanbic IBTC','Stanbic IBTC'),
    ('Sterling Bank','Sterling Bank'),
    ('Union Bank','Union Bank'),
    ('Zenith Bank','Zenith Bank'),
    ('Unity Bank','Unity Bank'),
    ('FCMBank','FCMBank'),
    ('GTBank','GTBank'),
    ('FIdelity Bank','FIdelity Bank'),
    ('ECO Bank','ECO Bank'),

)

class CustomUserCreationForm(UserCreationForm):
    username  = forms.CharField()
    password1 = forms.CharField(widget = forms.PasswordInput, label='Password',
    help_text='min_lenght-8 mix characters [i.e musa1234] ')
    password2 = forms.CharField(widget = forms.PasswordInput,help_text='Enter same password as before',label='Confirm Password')
    Phone = forms.CharField(max_length = 11, min_length = 11)
    referer_username = forms.CharField(required=False,help_text='Leave blank if no referral',label='Referral username [optional]')


    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("FullName",'username','email','Phone','Address','referer_username','password1','password2')


class Pinform(forms.ModelForm):
      pin = forms.IntegerField( max_value=9999,min_value=0000,help_text='max 4 lenght digit')

      class Meta:
            model = PinCode
            fields =  ('pin',)


class CustomUserChangeForm(UserChangeForm):

     AccountNumber = forms.CharField(max_length = 15)
     
     class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('BankName',"AccountName",'AccountNumber')


class airtimeform(forms.ModelForm):
    pin = forms.CharField(max_length = 18, min_length = 10)


    class Meta:
        model = Airtime
        fields = ('network','pin','amount')



class Airtime_fundingform(forms.ModelForm):
     amount =forms.IntegerField(min_value = 0 )
     mobile_number = forms.CharField(max_length = 11, min_length = 11)
     use_to_fund_wallet  = forms.BooleanField(required=False,initial=False,label='Check if you want to use it to fund wallet else transfer to bank below.')


     class Meta:
        model = Airtime_funding
        fields = ('network','mobile_number','amount',"use_to_fund_wallet")


class withdrawform(forms.ModelForm):
     bankName = forms.ChoiceField(choices=Bank, initial ='initial="Select Bank Name')
     amount =forms.IntegerField(min_value = 0 )
     class Meta:
        model = Withdraw
        fields =  ('accountName','accountNumber','bankName','amount')




class Transferform(forms.ModelForm):
     amount =forms.IntegerField(min_value = 0 )
     class Meta:
        model =Transfer
        fields =  ('receiver_username','amount')


class Notify_user_form(forms.ModelForm):
     message = forms.CharField(max_length = 3000, widget = forms.Textarea(attrs={'rows':3, 'cols':1}))
    # send_sms = forms.BooleanField(required=False,initial=False,label='Deliver notification has sms to users.')

     class Meta:
        model =Notify_user
        fields =  ('username','message')


class AirtimeTopupform(forms.ModelForm):

     mobile_number = forms.CharField(max_length = 11, min_length = 11)
     amount =forms.IntegerField(min_value = 100 )
     Ported_number = forms.BooleanField(required=False,initial=False,label='Bypass number validator ')

     
     
     
    

     class Meta:
        model = AirtimeTopup
        fields =  ('network','airtime_type','mobile_number','amount',"Ported_number")


class Airtimeswapform(forms.ModelForm):

      amount =forms.IntegerField(min_value = 0)
      mobile_number = forms.CharField(max_length = 11, min_length = 11)
      Ported_number = forms.BooleanField(required=False,initial=False,label='Bypass number validator ')



      class Meta:
        model = Airtimeswap
        fields =  ('swap_from_network','swap_to_network','mobile_number','amount','Ported_number')

class paymentgateway_form(forms.ModelForm):

      class Meta:
        model = paymentgateway
        fields =  ('amount',)

class Bulk_Message_form(forms.ModelForm):


    sendername = forms.CharField(max_length=12,label='From [Sendername]: ')
    to = forms.CharField(max_length=4000, widget = forms.Textarea(attrs={'rows':4, 'cols':1}),help_text='Type or Paste up to 10,000 phone numbers here (080... or 23480...) separate with comma ,NO SPACES!',label='To [Recipients]: ')
    message = forms.CharField(max_length =4000, widget = forms.Textarea(attrs={'rows':4, 'cols':1}))
    #DND = forms.BooleanField(required=False,initial=False,label='Select this to ensure delivery to DND numbers at 2 units per  number.')


    class Meta:
          model = Bulk_Message
          fields =  ('sendername','to','message')


class Buybtcform(forms.ModelForm):

      class Meta:
        model = Buybtc
        fields =  ('amount','Btc_address')


class SellBtcform(forms.ModelForm):

      class Meta:
        model = SellBtc
        fields =  ('Btc',)

class Result_Checker_Pin_order_form(forms.ModelForm):
      quantity = forms.IntegerField(min_value = 1,max_value = 5,initial = 1)
     

      class Meta:
        model = Result_Checker_Pin_order
        fields =  ('exam_name',"quantity")



class Recharge_Pin_order_form(forms.ModelForm):
      quantity = forms.IntegerField(min_value = 1,max_value = 24,initial = 1)
      name_on_card = forms.CharField(max_length = 200, min_length = 3,help_text="Your Company name to show on generated pin")



      class Meta:
        model = Recharge_pin_order
        fields =  ('network','network_amount',"name_on_card","quantity")

      def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['network_amount'].queryset = Recharge.objects.none()

            if 'network' in self.data:
                try:
                    network_id = int(self.data.get('network'))
                    self.fields['network_amount'].queryset = Recharge.objects.filter(network_id = network_id).order_by('amount')

                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['network_amount'].queryset = self.instance.network.network_amount.order_by('amount')





class bonus_transfer_form(forms.ModelForm):

      class Meta:
        model = bonus_transfer
        fields =  ('amount',)



class Bulk_Message_form(forms.ModelForm):


    sendername = forms.CharField(max_length=12,label='From [Sendername]: ')
    to = forms.CharField(max_length=4000, widget = forms.Textarea(attrs={'rows':4, 'cols':1}),help_text='Type or Paste up to 10,000 phone numbers here (080... or 23480...) separate with comma ,NO SPACES!',label='To [Recipients]: ')
    message = forms.CharField(max_length =4000, widget = forms.Textarea(attrs={'rows':4, 'cols':1}))
    DND = forms.BooleanField(required=False,initial=False,label='    Select this to ensure delivery to DND numbers at 2 units per  number.')


    class Meta:
          model = Bulk_Message
          fields =  ('sendername','to','message','DND')


class CouponCodeform(forms.ModelForm):

      class Meta:
        model = CouponPayment
        fields =  ('Code',)


class Postcreate(forms.ModelForm):

      class Meta:
        model = Post
        fields =  ('title','image','content','status')

class Bankpaymentform(forms.ModelForm):

      Reference = forms.CharField(max_length = 15,label ='Reference or Narration',required =True, help_text = "Use your name as  Reference or Narration if it is bank Tranfer")
      amount = forms.IntegerField(min_value = 0)
      class Meta:
        model = Bankpayment
        fields =  ('Bank_paid_to','Reference', 'amount',)


class Testimonialform(forms.ModelForm):
      message = forms.CharField(max_length = 3000, widget = forms.Textarea(attrs={'rows':4, 'cols':1}))
      class Meta:
        model = Testimonial
        fields =  ('message',)

class Commentform(forms.ModelForm):
      Reply = forms.CharField(max_length = 3000, widget = forms.Textarea(attrs={'rows':2, 'cols':1}),label='Reply')
      class Meta:
        model = Comment
        fields =  ('Reply',)



class dataform(forms.ModelForm):
     mobile_number = forms.CharField(max_length = 11, min_length = 11)
     Ported_number = forms.BooleanField(required=False,initial=False,label='Bypass number validator ')
     Amount = forms.CharField(required=False,max_length = 11, min_length = 11)

     class Meta:
        model = Data
        fields =  ('network','data_type','mobile_number','plan',"Amount","Ported_number")

     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan'].queryset = Plan.objects.none()

        if 'network' in self.data:
            try:
                network_id = int(self.data.get('network'))
                self.fields['plan'].queryset = Plan.objects.filter(network_id = network_id).order_by('plan_amount')

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['plan'].queryset = self.instance.network.plan_set.order_by('plan_amount')



class Airtime_to_Data_pin_form(forms.ModelForm):
     mobile_number = forms.CharField(max_length = 11, min_length = 11)
     Ported_number = forms.BooleanField(required=False,initial=False,label='Bypass number validator ')




     class Meta:
        model = Airtime_to_Data_pin
        fields =  ('network','plan','pin','mobile_number','Ported_number')

     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan'].queryset = Airtime_to_data_Plan.objects.none()

        if 'network' in self.data:
            try:
                network_id = int(self.data.get('network'))
                self.fields['plan'].queryset = Airtime_to_data_Plan.objects.filter(network_id = network_id).order_by('plan_amount')

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['plan'].queryset = self.instance.network.plan_set.order_by('plan_amount')


class Airtime_to_Data_tranfer_form(forms.ModelForm):
     mobile_number = forms.CharField(max_length = 11, min_length = 11,label ='Receive Number')
     Ported_number = forms.BooleanField(required=False,initial=False,label='Bypass number validator ')


     class Meta:
        model = Airtime_to_Data_tranfer
        fields =  ('network','Transfer_number','mobile_number','plan','Ported_number')

class paymentgateway_form(forms.ModelForm):

     amount = forms.FloatField(label='Amount' ,min_value = 0.0 ,max_value = 2450.0)
     class Meta:
        model = paymentgateway
        fields =  ('amount',)


class Book_order_Form(forms.ModelForm):


     class Meta:
        model = Book_order
        fields =  ('email',)


class cableform(forms.ModelForm):

     smart_card_number = forms.CharField(max_length = 15, min_length = 5,label = 'Smart Card number / IUC number')

     class Meta:
        model = Cablesub
        fields =  ('cablename','smart_card_number','cableplan', 'customer_name',)

     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cableplan'].queryset = CablePlan.objects.none()

        if 'cablename' in self.data:
            try:
                cablename_id = int(self.data.get('cablename'))
                self.fields['cableplan'].queryset = CablePlan.objects.filter(cablename_id = cablename_id).order_by('plan_amount')

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['cableplan'].queryset = self.instance.cablename.cableplan_set.order_by('plan_amount')




class paymentraveform(forms.Form):
    amount = forms.FloatField(label='Amount' ,min_value = 0.0 ,max_value = 2450.0)
   


class TopuserWebsiteForm(forms.ModelForm):

    class Meta:
        model = TopuserWebsite
        fields = ('Domain_name','Offices_Address','Website_Customer_Care_Number',"SSL_Security")

class Billpaymentform(forms.ModelForm):
    Customer_Phone = forms.CharField(max_length = 11, min_length = 11,help_text="customer phone number")
    class Meta:
        model = Billpayment
        fields =  ('disco_name','meter_number','MeterType', 'customer_name', 'customer_address','amount','Customer_Phone')


class  monnify_payment_form(forms.Form):
    amount = forms.FloatField(label='Amount' ,min_value = 0.0 ,max_value = 5000.0)


gender =(
    ('MALE','MALE'),
    ('FEMALE','FEMALE'),

)

class KYCForm(forms.ModelForm):
     Gender = forms.ChoiceField(choices= gender)
     
     class Meta:
            model = KYC
            fields =  ('First_Name','Middle_Name',"Last_Name","DOB","Gender","State_of_origin","Local_gov_of_origin","BVN","passport_photogragh")