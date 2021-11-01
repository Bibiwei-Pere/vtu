from django.db import models
from django.db.models import F
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
import requests
import datetime
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from django.db.models import Sum
from django.db import transaction
from django.utils import dateparse
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
import json


# Create your models here.
import random



def sendmail(subject, message, user_email, username):
    ctx = {
        'message': message,
        "subject": subject,
        "username": username
    }
    message = get_template('email.html').render(ctx)
    msg = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()


User = settings.AUTH_USER_MODEL

Bank = (
    ('First Bank of Nigeria', 'First Bank of Nigeria'),
    ('UBA', 'UBA'),
    ('Access(Diamond) Bank', 'Access (Diamond) Bank'),
    ('Wema Bank', 'Wema Bank'),

    ('Heritage Bank', 'Heritage Bank'),
    ('Polarise Bank', 'Polarise Bank'),
    ('Stanbic IBTC', 'Stanbic IBTC'),
    ('Sterling Bank', 'Sterling Bank'),
    ('Union Bank', 'Union Bank'),
    ('Zenith Bank', 'Zenith Bank'),
    ('Unity Bank', 'Unity Bank'),
    ('FCMBank', 'FCMBank'),
    ('GTBank', 'GTBank'),
    ('FIdelity Bank', 'FIdelity Bank'),
    ('ECO Bank', 'ECO Bank'),

)
status = (
    ('processing', 'processing'),
    ('failed', 'Failed'),
    ('successful', 'Successful'),
)

Netstatus = (
    ('Fair', 'Fair'),
    ('Bad', 'Bad'),
    ('Strong', 'Strong'),

)

service = (
    ('Data', 'Data'),
    ('Airtime', 'Airtime'),
    ('Cablesub', 'Cablesub'),
    ('Bill', 'Bill'),
    ('Withdraw', 'Withdraw'),
    ('Recharge Printing', 'Recharge Printing'),
    ('Bulk SMS', 'Bulk SMS'),
    ('AIRTIME TO CASH ', 'AIRTIME TO CASH '),
    ('RESULT CHECKER SERVICES', 'RESULT CHECKER SERVICES'),

)

plan_type = (
    ('CORPORATE GIFTING', 'CORPORATE GIFTING'),
    ('GIFTING', 'GIFTING'),
    ('SME', 'SME')
)


Mtn_Tran_Plan = (
    ('600', '1Gb  = #600'),
    ('1200', '2Gb  = #1200'),
    ('2900', '5Gb  = #2900'),

)

Network_2 = (
    ('MTN', 'MTN'),
    ('AIRTEL', 'AIRTEL'),

)


mtype = (
    ('Prepaid', 'Prepaid'),
    ('Postpaid', 'Postpaid'),

)

Network_3 = (
    ('MTN', 'MTN'),

)

api_medium = (
    ('SIMHOST', 'SIMHOST'),
    ('SMEPLUG', 'SMEPLUG'),
    ('SMS', 'SMS'),
    ('UWS', 'UWS'),
    ('MSPLUG', 'MSPLUG'),
    ('VTUAUTO', 'VTUAUTO'),
    ('VTPASS', 'VTPASS'),
    ('SMEIFY', 'SMEIFY'),
     ('MSORG_DEVELOPED_WEBSITE', 'MSORG_DEVELOPED_WEBSITE'),
)

cop_api_medium ={
    ('SMEPLUG', 'SMEPLUG'),
    ('CG_KONNECT', 'CG_KONNECT'),
    ('SMS', 'SMS'),
    ('UWS', 'UWS'),
    ('USSD', 'USSD'),
    ('MSORG_DEVELOPED_WEBSITE', 'MSORG_DEVELOPED_WEBSITE'),
}


api_medium2 = (
    ('SIMHOST', 'SIMHOST'),
    ('SMS', 'SMS'),
    ('MSPLUG', 'MSPLUG'),
    ('VTUAUTO', 'VTUAUTO'),
    ('SMEIFY', 'SMEIFY'),
     ('MSORG_DEVELOPED_WEBSITE', 'MSORG_DEVELOPED_WEBSITE'),

)




Netchoice = (
    ('MTN', 'MTN'),
    ('GLO', 'GLO'),
    ('AIRTEL', 'AIRTEL'),
    ('9MOBILE', '9MOBILE'),
    ('SMILE', 'SMILE'),
    ('SPECTRANET', 'SPECTRANET'),
    ('SWIFT', 'SWIFT'),

)

result = (
    ('WAEC', 'WAEC'),
    ('NECO', 'NECO'),

)


Air_choice = (
    ('100', '#100'),
    ('200', '#200'),
    ('400', '#400'),
    ('500', '#500'),
    ('1000', '#1000'),

)

service = (
    ('Data', 'Data'),
    ('Airtime', 'Airtime'),
    ('Cablesub', 'Cablesub'),
    ('Bill', 'Bill'),
    ('Bankpayment', 'Bankpayment'),
    ('Monnify ATM', 'Monnify ATM'),
    ('Monnfy bank', 'Monnify bank'),
    ('paystack', 'paystack'),
    ('Result_checker', 'Result_checker'),
    ('Recharge_printing', 'Recharge_printing'),
    ('Bulk sms', 'Bulk sms'),
    ('Airtime_Funding', 'Airtime_Funding'),


)

airtype = (
    ('VTU', 'VTU'),
    ('Share and Sell', 'Share and Sell'),

)

Volchoice = (
    ('MB', 'MB'),
    ('GB', 'GB'),
    ('TB', 'TB'),

)

ratechoice = (
    ('Selling_rate', 'Selling_rate'),
    ('Buying_rate', 'Buying_rate'),


)


Multichoice = (
    ('GOTV', 'GOTV'),
    ('DSTV', 'DSTV'),
    ('STARTIME', 'STARTIME'),
    ('TSTV', 'TSTV'),

)

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


user_t = (
    ("Smart Earner", "Smart Earner"),
    ("Affilliate", "Affilliate"),
    ("TopUser", "TopUser"),
    ("API", "API")

)

status2 = (
    ('Pending', 'Pending'),
    ('Processing', 'processing'),
    ('Delivered', 'Delivered'),
)


def create_id():
    num = random.randint(100, 2000)
    num_2 = random.randint(1, 1000)
    num_3 = random.randint(60, 1000)
    return str(num) + str(num_2)+str(num_3)+str(uuid.uuid4())[:8]

    # +str(num_2)+str(num_3)+str(uuid.uuid4())[:7]


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(
            self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class CustomUser(AbstractUser):
    objects = CustomUserManager()
    email = models.EmailField()
    birth_date = models.DateField(blank=True,null=True)
    FullName = models.CharField(max_length=200,  null=True)
    Address = models.CharField(max_length=500,  null=True)
    BankName = models.CharField(max_length=100, choices=Bank, blank=True)
    AccountNumber = models.CharField(max_length=40, blank=True)
    Phone = models.CharField(max_length=30, blank=True)
    AccountName = models.CharField(max_length=200, blank=True)
    Account_Balance = models.FloatField(
        default=0.00, null=True, validators=[MinValueValidator(0.0)],)
    pin = models.CharField(null=True, blank=True, max_length=5)
    referer_username = models.CharField(max_length=50, blank=True, null=True)
    first_payment = models.BooleanField(default=False)
    Referer_Bonus = models.FloatField(
        default=0.00, null=True, validators=[MinValueValidator(0.0)],)
    user_type = models.CharField(
        max_length=30, choices=user_t, default="Smart Earner", null=True)
    reservedaccountNumber = models.CharField(
        max_length=100, blank=True, null=True)
    reservedbankName = models.CharField(max_length=100, blank=True, null=True)
    reservedaccountReference = models.CharField(max_length=100, blank=True, null=True)
    Bonus = models.FloatField(default=0.00, null=True, validators=[ MinValueValidator(0.0)],)
    verify = models.BooleanField(default=False)
    DOB = models.DateField(null=True,blank=True,)
    Gender = models.CharField(max_length=6, null=True,)
    State_of_origin = models.CharField(max_length=100, null=True,)
    Local_gov_of_origin = models.CharField(max_length=100, null=True,)
    BVN = models.CharField(max_length=50, null=True,)
    passport_photogragh = models.ImageField(upload_to="passport_images", null=True, help_text="Maximum of 50kb in size")
    accounts = models.TextField(blank=True,null=True)


    def f_account(self):
        try:
            return json.loads(self.accounts)
        except:
            return {}


    def __str__(self):
        return self.username

    def image_tag(self):

        from django.utils.html import mark_safe
        return mark_safe('<img src="https://www.Husmodata.com/media/%s" width="150" height="150" />' % (self.passport_photogragh))

    image_tag.short_description = 'Image'

    def walletb(self):
         return  str(round(self.Account_Balance))

    def bonusb(self):
         return  str(round(self.Referer_Bonus))

    def ref_deposit(self, amount):
        self.Referer_Bonus += amount
        self.Referer_Bonus = round(self.Referer_Bonus, 2)
        self.save()


    def ref_withdraw(self, amount):
        if self.self.Referer_Bonus > amount or amount < 0 :
            return False
        self.Referer_Bonus -= amount
        self.Referer_Bonus = round(self.Referer_Bonus, 2)
        self.save()


    @classmethod
    def withdraw(cls, id, amount):
        with transaction.atomic():
            account = (cls.objects.select_for_update().get(id=id))
            print(account)
            balance_before = account.Account_Balance
            if account.Account_Balance < amount or amount < 0:
                return False
            account.Account_Balance -= amount
            account.save()

        try:

            Transactions.objects.create(user=CustomUser.objects.get(id=id),
                transaction_type="DEBIT", balance_before= balance_before,balance_after = balance_before -amount,amount=amount)

        except:
            pass

    @classmethod
    def deposit(cls, id, amount, transfer=False,medium = "NONE" ):
        with transaction.atomic():
            account = (cls.objects.select_for_update().get(id=id))
            # if transfer == False:
            #     if account.referer_username:
            #         if CustomUser.objects.filter(username__iexact=account.referer_username).exists():
            #             if account.first_payment == False:
            #                 referer = CustomUser.objects.get(
            #                     username__iexact=account.referer_username)
            #                 if amount >= 5000:
            #                     referer.ref_deposit(100)
            #                     account.first_payment = True
            #                 else:
            #                     referer.ref_deposit((0.05*amount))
            #                     account.first_payment = True

            balance_before = account.Account_Balance
            if medium != "NONE" :

                    if Charge_user.objects.filter(username = account.username).exists():
                            pending_charge = Charge_user.objects.filter(username =account.username).last()
                            if pending_charge.pending_amount > 0:
                                    if amount > pending_charge.pending_amount:
                                        amt = amount - pending_charge.pending_amount
                                        balance_before = account.Account_Balance
                                        pending_charge.balance_before = balance_before
                                        account.Account_Balance += amt
                                        account.save()

                                        try:
                                            Wallet_summary.objects.create(user=account, product=f"N{pending_charge.pending_amount} pending wallet charge paid", amount=amount, previous_balance = balance_before, after_balance= balance_before + amount)
                                        except:
                                            pass
                                        pending_charge.comment = f"N{pending_charge.pending_amount} pending wallet charge paid"
                                        pending_charge.balance_after = amt
                                        pending_charge.pending_amount = 0
                                        pending_charge.save()





                                    else:
                                        balance_before = account.Account_Balance
                                        pending_charge.balance_before = balance_before
                                        amt = pending_charge.pending_amount - amount
                                        pending_charge.comment = f"N{amount} paid from  pending wallet charge, pending amount remain {amount} "
                                        pending_charge.pending_amount =  amt
                                        pending_charge.balance_after = 0
                                        pending_charge.save()



                            else:
                                  account.Account_Balance += amount
                                  account.save()
                    else:
                          account.Account_Balance += amount
                          account.save()

            try:

                Transactions.objects.create(user=CustomUser.objects.get(id=id),
                    transaction_type="CREDIT",balance_before= balance_before,balance_after = balance_before + amount, amount= amount)

            except:
                pass

            try:
                 Wallet_Funding.objects.create(user=CustomUser.objects.get(id=id),medium=medium,previous_balance= balance_before,after_balance= balance_before + amount, amount= amount)

            except:
                    pass


        return account

    def ref_withdraw(self, amount):
        if self.Referer_Bonus > 0.0:
            self.Referer_Bonus -= amount
            self.Referer_Bonus = round(self.Referer_Bonus, 2)
            self.save()


    class Meta:
        verbose_name_plural = 'USERS MANAGEMENT'

vericate = (
    ('processing', 'processing'),
    ('Approved', 'Approved'),
    ('Not_Appprove', 'Not_Approve'),
)


def validate_file_size(value):
    filesize = value.size

    if filesize > 1024 * 50:
        raise ValidationError(
            "The maximum file size that can be uploaded is 50kb")
    else:
        return value



class TopuserWebsite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    Domain_name = models.CharField(max_length=500)
    amount = models.CharField(max_length=10)
    Offices_Address = models.CharField(max_length=800)
    Website_Customer_Care_Number = models.CharField(max_length=15)
    SSL_Security = models.BooleanField(
        default=False, help_text="Additional ₦5000 for SSL Certificate")
    status = models.CharField(
        max_length=30, choices=status2, default='processing')

    def __str__(self):
        return self.user.username


class user_upgrade_amount(models.Model):
    top_user_amount = models.CharField(max_length=10)
    affilliate_user_amount = models.CharField(max_length=10)

    def __str__(self):
        return "Upgrade price"

    def save(self, *args, **kwargs):
        if user_upgrade_amount.objects.all():
            user_upgrade_amount.objects.all().delete()
        super(user_upgrade_amount, self).save(*args, **kwargs)

class Wallet_Funding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name='wallet_funding')
    medium = models.CharField(max_length=500, blank=True,editable=False, )
    amount = models.CharField(max_length=30, blank=True,editable=False, )
    previous_balance = models.CharField(max_length=30, blank=True,editable=False, )
    after_balance = models.CharField(max_length=30, blank=True, null=True,editable=False, )
    create_date = models.DateTimeField(default=timezone.now,editable=False, )
    ident = models.CharField(default=create_id, editable=False, max_length=30)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'WALLET FUNDING TRACKING'

    def save(self, *args, **kwargs):
        try:
            user = self.user
            chek =  Wallet_Funding.objects.filter(user=user).count()
            if user.referer_username and chek == 0:
                if CustomUser.objects.filter(username__iexact=user.referer_username).exists():
                    referer = CustomUser.objects.get(username__iexact=user.referer_username)
                    ref_previous_bal = referer.Account_Balance
                    amt_to_earn = round(int(self.amount) * 0.05)
                    if amt_to_earn > 200:
                        amt_to_earn = 200

                    amt_to_earn = int(amt_to_earn)
                    referer.ref_deposit(int(amt_to_earn))

                    notify.send(referer, recipient=referer, verb=f'you Earned N{amt_to_earn} Bonus from your referal: {user.username} first funding and has been added to your referal bonus wallet')
                    Wallet_summary.objects.create(user=referer, product=f"Earned N{amt_to_earn} referral bonus from {user} first funding", amount=amt_to_earn, previous_balance=ref_previous_bal, after_balance=(ref_previous_bal + amt_to_earn))
        except:
            pass
        return super(Wallet_Funding, self).save(*args, **kwargs)


class Black_List_Phone_Number(models.Model):
    phone = models.CharField(max_length=30, blank=True,)

    def __str__(self):
        return str(self.phone)

    class Meta:
        verbose_name_plural = 'BLACKLIST PHONE NUMBER'



class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    amount = models.FloatField()
    balance_before = models.FloatField(blank=True, null=True)
    balance_after = models.FloatField(blank=True, null=True)
    transaction_type = models.CharField(max_length=30, blank=True)
    create_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'WALLET TRANSACTIONS'

    def __str__(self):
        return str(self.transaction_type)

    def today_credit_transaction(self):

        today = datetime.date.today()
        return Transactions.objects.filter(create_date__gt=today, transaction_type="CREDIT").aggregate(Sum('amount'))['amount__sum']

    def today_debit_transaction(self):
        today = datetime.date.today()
        return Transactions.objects.filter(create_date__gt=today, transaction_type="DEBIT").aggregate(Sum('amount'))['amount__sum']

    def this_month_credit_transaction(self):
        current_month = datetime.datetime.now().month
        return Transactions.objects.filter(create_date__month=current_month, transaction_type="CREDIT").aggregate(Sum('amount'))['amount__sum']

    def this_month_debit_transaction(self):
        current_month = datetime.datetime.now().month
        return Transactions.objects.filter(create_date__month=current_month, transaction_type="DEBIT").aggregate(Sum('amount'))['amount__sum']

    def total_credit_transaction(self):
        return Transactions.objects.filter(transaction_type="CREDIT").aggregate(Sum('amount'))['amount__sum']

    def total_debit_transaction(self):
        return Transactions.objects.filter(transaction_type="DEBIT").aggregate(Sum('amount'))['amount__sum']


class Wallet_summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             editable=False, blank=False, null=True, related_name='wallet')
    product = models.CharField(max_length=500, blank=True)
    amount = models.CharField(max_length=30, blank=True)
    previous_balance = models.CharField(max_length=30, blank=True)
    after_balance = models.CharField(max_length=30, blank=True, null=True)
    Status = models.CharField(
        max_length=30, choices=status, default='successful')
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        try:
            sendmail("Transaction Notification ",f"{product} \n Amount : {self.amount} \n Previous Balance : {self.previous_balance} \n New Balance: {self.after_balance} \n Date {self.create_date.strftime('%d, %b %Y') }", self.user.email, self.user.username)
        except:
            pass
        super(Wallet_summary, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'USERS WALLET SUMMARY'


class bonus_transfer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    amount = models.CharField(max_length=30, blank=True)
    create_date = models.DateTimeField(default=timezone.now)
    Current_bonus = models.CharField(max_length=30, blank=True)
    ident = models.CharField(default=create_id, editable=False, max_length=30)

    def __str__(self):
        return self.amount

class BankAccount(models.Model):

    bank_name = models.CharField(max_length=500, null=True, blank=True)
    account_name = models.CharField(max_length=500, null=True, blank=True)
    account_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.bank_name
    class Meta:
        verbose_name_plural = 'ADMIN BANK ACCOUNT'


class WebsiteConfiguration(models.Model):

    vtpass_email = models.CharField(max_length=500, null=True, blank=True,
                                    help_text="Enter your Vtpass Email here if you are using VTpass else leave blank")
    vtpass_password = models.CharField(max_length=500, null=True, blank=True,
                                       help_text="Enter your Vtpass password here if you are using VTpass else leave blank")

    hollatag_username = models.CharField(max_length=500, null=True, blank=True,
                                         help_text="Enter your hollatag username here if you are using hollatag else leave blank")
    hollatag_password = models.CharField(max_length=500, null=True, blank=True,
                                         help_text="Enter your hollatag  password here if you are using hollatag else leave blank")
    sme_plug_secret_key = models.CharField(max_length=500, null=True, blank=True,
                                           help_text="Enter your SMEPLUG SCRET API KEY here if you are using SMEplug else leave blank")
    Paystack_secret_key = models.CharField(max_length=500, null=True, blank=True,
                                           help_text="Enter your Paystack SCRET API KEY here if you are using Paystack, else leave blank")
    monnify_API_KEY = models.CharField(max_length=500, null=True, blank=True,
                                       help_text="Enter your monnify  API_KEY here if you are using monnify  else leave blank")
    monnify_SECRET_KEY = models.CharField(max_length=500, null=True, blank=True,
                                          help_text="Enter your monnify Secret Key here if you are using monnify else leave blank")
    monnify_contract_code = models.CharField(
        max_length=500, null=True, blank=True, help_text="Enter your monnify contarct code here if you are using monnify else leave blank")
    simhost_API_key = models.CharField(max_length=500, null=True, blank=True,
                                       help_text="Enter your simhost APIKEY here if you are using simhost else leave blank")
    msplug_API_key = models.CharField(max_length=500, null=True, blank=True,
                                      help_text="Enter your msplug APIKEY here if you are using msplug else leave blank")
    vtu_auto_email = models.CharField(max_length=500, null=True, blank=True,
                                    help_text="Enter your vtuauto Email here if you are using vtuauto else leave blank")
    vtu_auto_password = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your vtuauto Password here if you are using vtuauto else leave blank")
    support_phone_number = models.CharField(max_length=13, null=True, blank=True, help_text="Customer support phone number ,Whatsapp number  (start with 234)")
    whatsapp_group_link = models.URLField(null=True, blank=True, help_text="Support group link if any")
    gmail = models.EmailField( null=True, blank=True, help_text="Email to get notification on")
    mobilenig_username = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your mobilenig username here if you are using mobilenig else leave blank")
    mobilenig_api_key = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your mobilenig APIKEY here if you are using mobilenig else leave blank")
    idchecker_api_key = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your mobilenig APIKEY here if you are using mobilenig else leave blank")
    uws_token = models.TextField( null=True, blank=True,)
    msorg_web_url = models.TextField( null=True, blank=True,)
    msorg_web_api_key = models.CharField(max_length=500, null=True, blank=True, help_text="Enter your mobilenig APIKEY here if you are using mobilenig else leave blank")



    def save(self, *args, **kwargs):
        if WebsiteConfiguration.objects.all():
            WebsiteConfiguration.objects.all().delete()

        super(WebsiteConfiguration, self).save(*args, **kwargs)

    def __str__(self):
        return "Website Configuration"

    class Meta:
        verbose_name_plural = 'WEBSITE CONFIGURATIONS'


class Referal_list(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    username = models.CharField(max_length=30)
    referal_user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="referal")

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        mb = CustomUser.objects.get(username__iexact=self.username)
        self.referal_user = mb

        super(Referal_list, self).save(*args, **kwargs)


class Network(models.Model):
    name = models.CharField(max_length=30, choices=Netchoice, unique=True)
    status = models.CharField(max_length=30, choices=Netstatus)
    recharge_pin = models.BooleanField(default = False,blank=True,null=True)
    data_vending_medium = models.CharField(max_length=30, choices=api_medium)
    gifting_data_vending_medium = models.CharField(max_length=30, choices=cop_api_medium,null=True)
    corporate_data_vending_medium = models.CharField(max_length=30, choices=cop_api_medium,null=True)
    vtu_vending_medium = models.CharField(max_length=30, choices=api_medium,null=True)
    msorg_web_net_id = models.CharField(max_length=5, null=True)
    share_and_sell_vending_medium = models.CharField(
        max_length=30, choices=api_medium2,null=True)
    convertion_parcentage = models.IntegerField(blank=True, null=True)
    sme_disable = models.BooleanField(default = False,blank=True,null=True)
    corporate_gifting_disable = models.BooleanField(default = False,blank=True,null=True)
    gifting_disable = models.BooleanField(default = False,blank=True,null=True)
    airtime_disable = models.BooleanField(default=False, blank=True, null=True)
    data_disable = models.BooleanField(default=False, blank=True, null=True)
    recharge_pin_disable = models.BooleanField(
        default=False, blank=True, null=True)
    share_and_sell_disable = models.BooleanField(
        default=False, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'NETWORKS'


class Network_1(models.Model):
    name = models.CharField(max_length=30, choices=Network_2, unique=True)
    status = models.CharField(max_length=30, choices=Netstatus)

    def __str__(self):
        return str(self.name)


class New_order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    name = models.CharField(max_length=30)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class Charge_user(models.Model):
    username = models.CharField(max_length=100, null=True)
    amount = models.IntegerField()

    balance_before = models.FloatField(
        null=True, blank=True, help_text="leave blank sytem automatic set this")
    balance_after = models.FloatField(
        null=True, blank=True, help_text="leave blank sytem automatic set this")
    comment = models.TextField()
    pending_amount = models.IntegerField(default=0,help_text="leave blank sytem automatic set this,if the amount you want to with not upto user wallet, pending amount wait till when user fund next")

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        try:
            mb = CustomUser.objects.get(username=self.username)
        except:
            raise ValidationError(f'Invalid user, enter correct username')
        if not self.id:
                        if self.amount > mb.Account_Balance:
                            self.pending_amount = self.amount  - mb.Account_Balance
                            self.balance_before = mb.Account_Balance
                            mb.withdraw(mb.id, mb.Account_Balance)

                            self.balance_after = 0

                            try:
                                Wallet_summary.objects.create(
                                    user=mb, product=f"Admin Charge your account for {self.comment} ", amount=self.amount, previous_balance=self.balance_before, after_balance=self.balance_after)
                            except:
                                pass

                        else:
                            self.balance_before = mb.Account_Balance
                            withdraw = mb.withdraw(mb.id, self.amount)
                            if withdraw == False:
                                raise ValidationError(
                                    f'Insufficient fund ,{self.username} wallet balance is {mb.Account_Balance}')
                            self.balance_after = mb.Account_Balance - self.amount

                            try:
                                Wallet_summary.objects.create(
                                    user=mb, product=f"Admin Charge your account for {self.comment} ", amount=self.amount, previous_balance=self.balance_before, after_balance=self.balance_after)
                            except:
                                pass

        super(Charge_user, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'WITHDRAW FROM USER WALLET'


class Fund_User(models.Model):
    username = models.CharField(max_length=100, null=True)
    amount = models.IntegerField()
    balance_before = models.FloatField(
        null=True, blank=True, help_text="leave blank sytem automatic set this")
    balance_after = models.FloatField(
        null=True, blank=True, help_text="leave blank sytem automatic set this")

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):

        try:
            mb = CustomUser.objects.get(username=self.username)
        except:
            raise ValidationError(f'Invalid user, enter correct username')

        self.balance_before = mb.Account_Balance
        mb.deposit(mb.id, self.amount,False,"ADMIN WALLET FUNDING")
        self.balance_after = mb.Account_Balance + self.amount

        try:
            Wallet_summary.objects.create(
                user=mb, product=f"Admin  Funding your wallet with sum of {self.amount}", amount=self.amount, previous_balance=self.balance_before, after_balance=(self.balance_after))
        except:
            pass

        super(Fund_User, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'FUND USER WALLET'

class Plan(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    plan_size = models.FloatField()
    plan_Volume = models.CharField(max_length=30, choices=Volchoice)
    plan_amount = models.PositiveIntegerField()
    ussd_string =  models.CharField(max_length = 500, null=True,blank=True, help_text="put small letter n in place of number and p in place of pin i.e*141*6*2*3*3*1*n*p#")
    sms_command =  models.CharField(max_length = 500, null=True,blank=True, help_text="put small letter n in place of number and p in place of pin i.e SMEB n 1000 p")
    affillate_price = models.PositiveIntegerField(default=0)
    Affilliate_price = models.PositiveIntegerField(default=100000)
    TopUser_price = models.PositiveIntegerField(default=100000)
    api_price = models.PositiveIntegerField(default=100000)
    plan_name_id = models.CharField(max_length=500, null=True, blank=True)
    smeplug_id = models.CharField(max_length=500, null=True, blank=True)
    cgkonnect_id = models.CharField(max_length=500, null=True, blank=True)
    vtpass_vairiation_code = models.CharField(
        max_length=500, null=True, blank=True)
    smeify_plan_name_id = models.CharField(max_length = 30,blank=True,null=True)
    uws_plan_name_id = models.CharField(max_length = 500,blank=True,null=True)
    msplug_plan_name_id = models.CharField(max_length = 30,blank=True,null=True)

    plan_type = models.CharField(
        max_length=30, choices=plan_type, blank=True, help_text="Data plan  type only .")
    month_validate = models.CharField(max_length=30)

    def __str__(self):
        return str(self.plan_size) + str(self.plan_Volume) + '----' + 'N' + str(self.plan_amount)

    def plan_name(self):
        return str(self.plan_size) + str(self.plan_Volume)

    def plan_net(self):
        return str(self.network)

    def plan_amt(self):
        return str(self.plan_amount)

    def plan_amt2(self):
        return  str(self.Affilliate_price)

    def plan_amt3(self):
        return  str(self.TopUser_price)

    def plan_id(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'DATA PLANS'


class Disable_Service(models.Model):
    service = models.CharField(max_length=50, choices=service, unique=True,)
    disable = models.BooleanField(
        default=False, help_text="Check this box to disable this service, uncheck to unable it back")

    def save(self, *args, **kwargs):
        if Disable_Service.objects.filter(service=service):
            Disable_Service.objects.filter(service=service).delete()

        super(Disable_Service, self).save(*args, **kwargs)

    def __str__(self):
        return self.service

    class Meta:
        verbose_name_plural = 'DISABLE SERVICES'



class SmeifyAuth(models.Model):
      username = models.CharField(max_length =100,null=True,blank=True)
      password = models.CharField(max_length =100,null=True,blank=True)
      token = models.TextField(null=True,blank=True)
      expire_date  = models.DateTimeField(null=True,blank=True)
      re_auth = models.BooleanField(default=True,blank=True,null=True)


      def get_token(self):
            print(timezone.now())
            print(self.expire_date)
            print("musa")
            print(timezone.now() > self.expire_date)
            print(timezone.now() < self.expire_date)
            if timezone.now() >= self.expire_date:

                    try:
                        url = "https://auto.smeify.com/api/v1/refresh"
                        headers = { 'Content-Type': 'application/json','Authorization': f'Bearer {self.token}'}
                        resp = requests.request("GET", url,headers=headers)
                        print(resp.text)
                        rdata = json.loads(resp.text)
                        self.token = rdata["token"]
                        self.expire_date = dateparse.parse_datetime(f"{rdata['expires']}")
                        self.save()

                        return rdata["token"]
                    except:
                         return self.token
            else:

                 return self.token

      def save(self,*args,**kwargs):

              if  self.username and self.password and self.re_auth == True:
                    try:
                            url = f"https://auto.smeify.com/api/v1/auth/login?identity={self.username}&&password={self.password}"
                            response = requests.request("POST", url)
                            rdata = json.loads(response.text)
                            self.token = rdata["token"]
                            self.expire_date = dateparse.parse_datetime(f"{rdata['expires']}")

                            self.username = ""
                            self.password = ""
                            self.re_auth = False
                            self.save()

                    except:
                            pass

              super(SmeifyAuth,self).save(*args,**kwargs)


class Info_Alert(models.Model):
    message = models.TextField()
    image = models.ImageField(upload_to="alert_images", blank=True, null=True)

    class Meta:
        verbose_name_plural = 'CREATE ALERT NOTIFICATION'

    def save(self, *args, **kwargs):
        try:
            Info_Alert.objects.first().delete()
            # self.id += 1
            self.save()
        except:
            pass
        super(Info_Alert, self).save(*args, **kwargs)

    def __str__(self):
        return self.message


class Upgrade_user(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    from_package = models.CharField(max_length=50, blank=True)
    to_package = models.CharField(max_length=50, blank=True)
    amount = models.CharField(max_length=30, blank=True)
    previous_balance = models.CharField(max_length=30, blank=True)
    after_balance = models.CharField(max_length=30, blank=True, null=True)
    Status = models.CharField(
        max_length=30, choices=status, default='successful')
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name_plural = 'UPGRADE USER'


class Percentage(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    percent = models.IntegerField()

    def __str__(self):
        return str(self.network) + "-----" + str(self.percent)

    class Meta:
        verbose_name_plural = 'AIRTIME TO CASH PERCENTAGE'


class TopupPercentage(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    percent = models.IntegerField()
    Affilliate_percent = models.IntegerField(default=100)
    topuser_percent = models.IntegerField(default=100)
    api_percent = models.IntegerField(default=100)
    share_n_sell_percent = models.IntegerField(default=100)
    share_n_sell_api_percent = models.IntegerField(default=100)
    share_n_sell_affilliate_percent = models.IntegerField(default=100)
    share_n_sell_topuser_percent = models.IntegerField(default=100)

    class Meta:
        verbose_name_plural = 'AIRTIME TOPUP PERCENTAGE'

    def __str__(self):
        return str(self.network) + "-----" + str(self.percent)


class ServicesCharge(models.Model):
    service = models.CharField(choices=service, max_length=100, unique=True)
    charge = models.FloatField(
        default=0.0, help_text="Note: Extra charge , you can either set charge or Discount dont set both at once")
    Affilliate_charge = models.FloatField(
        default=0.0, help_text="Note: Extra charge , you can either set charge or Discount dont set both at once")
    topuser_charge = models.FloatField(
        default=0.0, help_text="Note: Extra charge , you can either set charge or Discount dont set both at once")
    api_charge = models.FloatField(
        default=0.0, help_text="Note: Extra charge , you can either set charge or Discount dont set both at once")
    discount = models.FloatField(
        default=0.0, help_text="set charge to 0 to set discount")
    Affilliate_discount = models.FloatField(
        default=0.0, help_text="set charge to 0 to set discount for affillitae users")
    topuser_discount = models.FloatField(
        default=0.0, help_text="set charge to 0 to set discount for topuser")
    api_discount = models.FloatField(
        default=0.0, help_text="set charge to 0 to set discountfor api user")

    def __str__(self):
        return str(self.service)

    def save(self, *args, **kwargs):

        if self.charge > 0.0 and self.discount > 0.0:
            self.discount = 0.0

        super(ServicesCharge, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'SERVICE CHARGE'


class Airtime_to_data_Plan(models.Model):
    network = models.ForeignKey(Network_1, on_delete=models.CASCADE)
    plan_size = models.FloatField()
    plan_Volume = models.CharField(max_length=30, choices=Volchoice)
    plan_amount = models.PositiveIntegerField()
    month_validate = models.CharField(max_length=30)

    def __str__(self):
        return str(self.plan_size)+str(self.plan_Volume) + '----' + '#' + str(self.plan_amount)+'#'


class Admin_number(models.Model):
    network = models.CharField(max_length=30, choices=Netchoice, unique=True)
    phone_number = models.CharField(max_length=30, blank=True, unique=True)

    def __str__(self):
        return str(self.network) + str(self. phone_number)

    class Meta:
        verbose_name_plural = 'AIRTIME TO CASH NUMBER'


class Airtime_funding(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    network = models.ForeignKey(Network, on_delete=models.SET_NULL, null=True)
    mobile_number = models.CharField(max_length=30, blank=True)
    amount = models.FloatField()
    Receivece_amount = models.FloatField(null=True)
    Status = models.CharField(max_length=30, choices=status, default='processing',
                              help_text="Select Succesful and save to fund user")
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    fund = models.BooleanField(default=False, blank=True, null=True)
    BankName = models.CharField(max_length=100, blank=True)
    AccountNumber = models.CharField(max_length=10, blank=True)
    AccountName = models.CharField(max_length=200, blank=True)
    use_to_fund_wallet = models.BooleanField(
        default=False, help_text="Note : if this is not check the user want to withdraw it to his bank kindly transfer to the account above after comfirm the airtime and change status to successful")

    def get_absolute_url(self):
        return reverse('airtime_detail', args=[str(self.id)])

    def __str__(self):
        return self.mobile_number

    def save(self, *args, **kwargs):

        if self.Status == 'successful' and self.fund == False and self.use_to_fund_wallet == True:
            previous_bal = self.user.Account_Balance
            self.user.deposit(self.user.id,float(self.Receivece_amount),False,"AIRTIME WALLET FUNDING")
            self.fund = True
            Wallet_summary.objects.create(user=self.user, product="Airtime  share Funding", amount=self.Receivece_amount,
                                          previous_balance=previous_bal, after_balance=(previous_bal + float(self.Receivece_amount)))

        super(Airtime_funding, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'AIRTIME TO CASH TRANSACTIONS'


class Airtime(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    network = models.ForeignKey(Network, on_delete=models.SET_NULL, null=True)
    pin = models.CharField(max_length=30, blank=True)
    amount = models.CharField(
        max_length=30, choices=Air_choice, default='#100')
    Receivece_amount = models.FloatField(null=True)
    Status = models.CharField(
        max_length=30, choices=status, default='processing')
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    fund = models.BooleanField(default=False, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('airtime_success', args=[str(self.id)])

    def __str__(self):
        return self.Status

    def save(self, *args, **kwargs):

        if self.Status == 'successful' and self.fund == False:
            previous_bal = self.user.Account_Balance
            self.user.deposit(self.user.id, self.user.id,
                              float(self.Receivece_amount),False,"AIRTIME WALLET FUNDING")
            self.fund = True
            Wallet_summary.objects.create(user=self.user, product="Airtime  pin Funding", amount=self.Receivece_amount,
                                          previous_balance=previous_bal, after_balance=(previous_bal - float(self.Receivece_amount)))

        super(Airtime, self).save(*args, **kwargs)


class Result_Checker_Pin(models.Model):

    exam_name = models.CharField(max_length=15, choices=result, unique=True)
    provider_amount = models.FloatField(
        help_text="amount your API provider are selling it", default=1700)
    disable_this_exam = models.BooleanField(
        default=False, blank=True, null=True)
    provider_api = models.CharField(max_length=30, default="MOBILENIG",choices=(("MOBILENIG","MOBILENIG"),("VTPASS","VTPASS"),("EASYACCESS","EASYACCESS.COM.NG")))
    amount = models.FloatField(default="1800")
    Affilliate_price = models.FloatField(default=1750)
    TopUser_price = models.FloatField(default=1750)
    api_price = models.FloatField(default=1750)

    def __str__(self):
        return self.exam_name

    class Meta:
        verbose_name_plural = 'RESULT CHECKER CONTROL'


class Result_Checker_Pin_order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    exam_name = models.CharField(max_length=15, choices=result)
    create_date = models.DateTimeField(default=timezone.now)
    quantity = models.PositiveIntegerField(default=1,)
    data = models.TextField(null=True)
    amount = models.FloatField(default=0)
    previous_balance = models.CharField(max_length=30, blank=True)
    after_balance = models.CharField(max_length=30, blank=True, null=True)
    Status = models.CharField(
        max_length=30, choices=status, default='successful')

    def __str__(self):
        return self.exam_name

    def data_pin(self):
        if self.data:
            return json.loads(self.data)

    def get_absolute_url(self):
        return reverse('checker_pin', args=[str(self.id)])

    class Meta:
        verbose_name_plural = 'RESULT CHECKER TRANSACTIONS'




class Recharge_pin(models.Model):

    network = models.ForeignKey(
        Network, on_delete=models.CASCADE, related_name="pin_net")
    available = models.BooleanField(default=True)
    amount = models.FloatField(default=100)
    pin = models.CharField(max_length=20, unique=False, null=True)
    serial = models.CharField(max_length=100, unique=False, null=True)
    load_code = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.network.name) + "  " + str(self.pin) + "  " + str(self.serial)


class Load_Recharge_pin(models.Model):
    network = models.ForeignKey(
        Network, on_delete=models.CASCADE, related_name="Loadpin_net")
    dump_pin = models.TextField()
    amount = models.FloatField(default=0)
    load_code = models.CharField(max_length=100, null=True)
    total_pin_loaded = models.CharField(
        max_length=100, null=True, blank=True, help_text="Leave blank, system automatic return it")

    def save(self, *args, **kwargs):
        data = self.dump_pin.split("\n")
        self.total_pin_loaded = len(data)
        if Recharge_pin.objects.all():
            last_id = int(Recharge_pin.objects.all().last().serial)
        else:
            last_id = 0

        for x in data:
            last_id += 1
            Recharge_pin.objects.create(
                pin=x, network=self.network, amount=self.amount, serial=last_id, load_code=self.load_code)
        super(Load_Recharge_pin, self).save(*args, **kwargs)

    def __str__(self):
        return " set  " + str(self.id)

    class Meta:
        verbose_name_plural = 'LOAD RECHARGE PIN'


class Recharge(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    amount = models.FloatField(default=0)
    amount_to_pay = models.FloatField(default=0)
    Affilliate_price = models.FloatField(default=100)
    TopUser_price = models.FloatField(default=100)
    api_price = models.FloatField(default=100)

    class Meta:
        verbose_name_plural = 'RECHARGE CARD PRINTING PRICE'

    def __str__(self):
        return str(self.amount_to_pay)

    def netname(self):
        return str(self.network.name)


class Recharge_pin_order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE, null=True)
    network_amount = models.ForeignKey(
        Recharge, on_delete=models.CASCADE, null=True)
    data = models.TextField(blank=False, null=True)
    name_on_card = models.CharField(max_length=200, blank=False, null=True)
    amount = models.FloatField(default=0)
    previous_balance = models.CharField(max_length=30, blank=True)
    after_balance = models.CharField(max_length=30, blank=True, null=True)
    quantity = models.PositiveIntegerField(null=True)
    create_date = models.DateTimeField(default=timezone.now)
    Status = models.CharField(
        max_length=30, choices=status, default='successful')

    class Meta:
        verbose_name_plural = 'RECHARGE CARD PRINTING TRANSACTIONS'

    def __str__(self):
        return str(self.create_date) + "> Batch " + str(self.id) + str(self.amount) + str(self.quantity)

    def Batch(self):
        return str(self.create_date) + "> Batch " + str(self.id) + str(self.amount) + str(self.quantity)

    def net_work(self):
        return str(self.network.name)

    def data_pin(self):
        if self.data:
            return json.loads(self.data)

    def loadcode(self):
        if self.network.name == "MTN":
            return str("Dial *555*pin# to load")
        elif self.network.name == "GLO":
            return str("Dial *123*pin# to load")
        elif self.network.name == "AIRTEL":
            return str("Dial *126*pin# to load")
        elif self.network.name == "9MOBILE":
            return str("Dial *222*pin# to load")

    def get_absolute_url(self):
        return reverse('recharge_pin', args=[str(self.id)])




class Couponcode(models.Model):

    Coupon_Code = models.CharField(max_length=15, unique=True)
    amount = models.CharField(max_length=15)
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    Used = models.BooleanField()

    def __str__(self):
        return self.Coupon_Code

    class Meta:
        verbose_name_plural = 'COUPON CODES'


class CouponPayment(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    Code = models.CharField(max_length=15)
    amount = models.IntegerField(editable=False, null=True)
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    Status = models.CharField(
        max_length=30, choices=status, default='successful')

    def get_absolute_url(self):
        return reverse('Coupon_success', args=[str(self.id)])

    def __str__(self):
        return self.Code

    class Meta:
        verbose_name_plural = 'COUPON PAYMENTS'


class Withdraw(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    accountNumber = models.CharField(max_length=30, blank=True)
    accountName = models.CharField(max_length=30, blank=True)
    bankName = models.CharField(max_length=100, choices=Bank, blank=True)
    amount = models.CharField(max_length=30, blank=True)
    previous_balance = models.CharField(max_length=30, blank=True)
    after_balance = models.CharField(max_length=30, blank=True, null=True)
    Status = models.CharField(max_length=30, choices=status, default='processing',
                              help_text="Select failed and save to refund user")
    create_date = models.DateTimeField(default=timezone.now)
    Current_balance = models.CharField(max_length=30, blank=True)
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    refund = models.BooleanField(default=False, blank=True, null=True)


    def save(self, *args, **kwargs):

        if self.Status == 'failed' and self.refund == False:
            previous_bal = self.user.Account_Balance
            self.user.deposit(self.user.id, float(self.amount),False,"Wallet Withdraw Refund")
            self.refund = True
            Wallet_summary.objects.create(user=self.user, product="Wallet Withdraw Refund", amount=self.amount,
                                          previous_balance=previous_bal, after_balance=(previous_bal + float(self.amount)))
        super(Withdraw, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('Withdraw_success', args=[str(self.id)])

    def __str__(self):
        return self.accountName

    class Meta:
        verbose_name_plural = 'WITHDRAW TRANSACTIONS'


class Data(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    network = models.ForeignKey(Network, on_delete=models.SET_NULL, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    data_type = models.CharField(max_length = 30, choices=plan_type,blank=True,null=True,help_text="Select Plan Type SME or GIFTING or CORPORATE GIFTING")
    mobile_number = models.CharField(max_length=30, blank=True)
    Status = models.CharField(max_length=30, choices=status, default='processing',
                              help_text="Select failed and save to refund user")
    medium = models.CharField(max_length=30, default='website')
    create_date = models.DateTimeField(default=timezone.now)
    balance_before = models.CharField(max_length=30, blank=True)
    balance_after = models.CharField(max_length=30, blank=True, null=True)
    plan_amount = models.CharField(max_length=30, blank=True)
    Ported_number = models.BooleanField(default=False, blank=True, null=True)
    ident = models.CharField(default=create_id, editable=False, max_length=300)
    refund = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'DATA TOP-UP TRANSACTIONS'

    def __str__(self):
        return str(self.plan)

    def data_amount(self):
        return str(self.plan_amount)

    def save(self, *args, **kwargs):

        # previous_bal = self.user.Account_Balance

        # if self.Status != 'successful' and self.refund == False:
        if self.Status == 'failed' and self.refund == False:
            previous_bal = float(self.user.Account_Balance) - float(self.plan_amount)
            after_bal = self.user.Account_Balance

            self.user.deposit(self.user.id, float(self.plan_amount),False ,"FAILED DATA TOPUP REFUND")
            self.refund = True

            Wallet_summary.objects.create(user=self.user, product="FAILED DATA TOPUP REFUND for {} {}{}   N{}  with {} ".format(self.network.name, self.plan.plan_size, self.plan.plan_Volume,  self.plan_amount, self.mobile_number), amount=self.plan_amount, previous_balance=previous_bal, after_balance=after_bal)

            # Wallet_summary.objects.create(user=self.user, product="{} {}{}   N{}  DATA topup Refund for {} ".format(self.network.name, self.plan.plan_size, self.plan.plan_Volume,  self.plan_amount, self.mobile_number), amount=self.plan_amount, previous_balance=previous_bal, after_balance=(previous_bal + float(self.plan_amount)))

        super(Data, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('Data_success', args=[str(self.id)])


class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False,
                             blank=False, null=True, related_name='Airtime_tranfere')
    receiver_username = models.CharField(max_length=30, blank=True)
    amount = models.CharField(max_length=30, blank=True)
    previous_balance = models.CharField(max_length=30, blank=True)
    after_balance = models.CharField(max_length=30, blank=True, null=True)
    Status = models.CharField(
        max_length=30, choices=status, default='successful')
    create_date = models.DateTimeField(default=timezone.now)
    Current_balance = models.CharField(max_length=30, blank=True)
    ident = models.CharField(default=create_id, editable=False, max_length=30)

    def __str__(self):
        return self.receiver_username

    def get_absolute_url(self):
        return reverse('Transfer_detail', args=[str(self.id)])

    class Meta:
        verbose_name_plural = 'WALLET-WALLET TRANSFER TRANSACTIONS'


class AirtimeTopup(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    network = models.ForeignKey(Network, on_delete=models.SET_NULL, null=True)
    mobile_number = models.CharField(max_length=30, blank=True)
    airtime_type = models.CharField(
        max_length=30, choices=airtype, default='VTU', help_text="VTU or share and Sell")
    amount = models.CharField(max_length=30, blank=True)
    paid_amount = models.CharField(max_length=30, blank=True)
    Status = models.CharField(max_length=30, choices=status, default='processing',
                              help_text="Select failed and save to refund user")
    create_date = models.DateTimeField(default=timezone.now)
    balance_before = models.CharField(max_length=30, blank=True)
    balance_after = models.CharField(max_length=30, blank=True)
    Ported_number = models.BooleanField(default=False, blank=True, null=True)
    medium = models.CharField(max_length=30, default='website')
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    refund = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.mobile_number

    def get_absolute_url(self):
        return reverse('AirtimeTopup_success', args=[str(self.id)])

    def plan_net(self):
        return str(self.network)

    def plan_amt(self):
        return "N"+str(self.amount)

    def save(self, *args, **kwargs):

        if self.Status == 'failed' and self.refund == False:
            previous_bal = self.user.Account_Balance
            self.user.deposit(self.user.id, float(self.paid_amount),False ,"AIRTIME TOPUP Refund")
            self.refund = True
            Wallet_summary.objects.create(user=self.user, product="{} {} Airtime topup Refund for {} ".format(
                self.network.name, self.amount, self.mobile_number), amount=self.paid_amount, previous_balance=previous_bal, after_balance=(previous_bal + float(self.paid_amount)))

        super(AirtimeTopup, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'AIRTIME TOPUP TRANSACTIONS'



class SME_text(models.Model):
    number = models.CharField(max_length=100)
    text_to_search = models.CharField(max_length=100, null=True, blank=True)
    new_data_vending_medium_for_random = models.CharField(max_length =100, choices = (('NORMAL_SLOT', 'NORMAL_SLOT'),('OLDSIM', 'OLDSIM'),('NEWSIM', 'NEWSIM')),null=True,blank=True)
    data_vending_medium_for_1_gb = models.CharField(max_length =100, choices = (('OLDSIM', 'OLDSIM'),('NEWSIM', 'NEWSIM')),null=True,blank=True)
    pin = models.CharField(
        max_length=10, help_text="DATA PIN if any", null=True, blank=True)
    pin2 = models.CharField(max_length =10,null=True, blank=True)
    pin3 = models.CharField(max_length =10,null=True, blank=True)

    vtu_pin = models.CharField(max_length=10, null=True, blank=True)
    share_and_sell_pin = models.CharField(max_length=10, null=True, blank=True)
    sim_host_server_id = models.CharField(
        max_length=500, help_text="If you are using simhost", null=True, blank=True)
    vtu_auto_device_id  = models.CharField(
        max_length=500, help_text="If you are using VTU AUTO", null=True, blank=True)
    vtu_sim_slot  = models.IntegerField( help_text="If you are using VTU AUTO i.e enter 1 for sim1", null=True, blank=True)
    msplug_device_id  = models.CharField(
        max_length=500, help_text="If you are using MSPLUG ", null=True, blank=True)
    msplug_sim_slot  = models.CharField(max_length=5, choices=(('sim1','sim1'), ('sim2', 'sim2')),help_text="If you are using MSPLUG i.e enter sim1 for sim1, sim2 for sim2", null=True, blank=True)

    network = models.OneToOneField(
        Network, on_delete=models.SET_NULL, null=True, unique=True)
    mtn_sme_route  = models.CharField(
        max_length=500, help_text="Select either SMS  to 131 or USSD  ", choices=(("SMS","SMS"),("USSD","USSD")),null=True, blank=True)

    def __str__(self):
        return self.network.name

    def save(self, *args, **kwargs):
        if SME_text.objects.filter(network=self.network):
            SME_text.objects.filter(network=self.network).delete()

        super(SME_text, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'SIM MANAGEMENT'


class Airtimeswap(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    swap_from_network = models.ForeignKey(
        Network, on_delete=models.SET_NULL, null=True, related_name='network_swap_from')
    swap_to_network = models.ForeignKey(
        Network, on_delete=models.SET_NULL, null=True, related_name='network_swap_to')
    amount = models.CharField(max_length=30, blank=True)
    mobile_number = models.CharField(max_length=30, blank=True)
    Status = models.CharField(
        max_length=30, choices=status, default='processing')
    create_date = models.DateTimeField(default=timezone.now)
    Receivece_amount = models.FloatField(null=True)
    Ported_number = models.BooleanField(default=False, blank=True, null=True)
    ident = models.CharField(default=create_id, editable=False, max_length=30)

    def __str__(self):
        return str(self.amount)

    def get_absolute_url(self):
        return reverse('Airtimeswap_success', args=[str(self.id)])


class PinCode(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    pin = models.IntegerField(unique=True)

    def get_absolute_url(self):
        return reverse('Transfer_detail', args=[str(self.id)])


class Btc_rate(models.Model):

    rate = models.CharField(max_length=50, choices=ratechoice)
    btc_wallet_address = models.CharField(max_length=200, default='abcdef')
    amount = models.FloatField()

    def __str__(self):
        return str(self.rate)


class Buybtc(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    Btc = models.FloatField(blank=False, null=True)
    amount = models.FloatField(blank=False, null=True)
    Btc_address = models.CharField(max_length=200)
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    Status = models.CharField(
        max_length=30, choices=status, default='processing')

    def __str__(self):
        return str(self.Btc)

    def get_absolute_url(self):
        return reverse('buy_btc_success', args=[str(self.id)])


class SellBtc(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    Btc = models.FloatField(blank=False, null=True)
    amount = models.FloatField(blank=False, null=True)
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    Status = models.CharField(
        max_length=30, choices=status, default='processing')

    def __str__(self):
        return str(self.Btc)

    def get_absolute_url(self):
        return reverse('sell_btc_success', args=[str(self.id)])


class Bulk_Message(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    unit = models.IntegerField(null=True)
    invalid = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    page = models.FloatField(null=True)
    amount = models.FloatField(null=True)
    sendername = models.CharField(max_length=12, blank=True)
    message = models.TextField(blank=True)
    to = models.TextField(blank=True)
    create_date = models.DateTimeField(default=timezone.now)
    DND = models.BooleanField(default=False, blank=True, null=True)
    ident = models.CharField(default=create_id, editable=False, max_length=30)

    def get_absolute_url(self):
        return reverse('Bulk_success', args=[str(self.id)])

    class Meta:
        verbose_name_plural = 'BULK SMS'


class Testimonial(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    message = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message


class Comment(models.Model):

    testimonial = models.ForeignKey(
        Testimonial, blank=True, on_delete=models.CASCADE)
    Reply = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Reply


class Notify_user(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    username = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    send_email = models.BooleanField(null=True, blank=True, default=False)
    ident = models.CharField(default=create_id, editable=False, max_length=30)

    def __str__(self):
        return self.username


class Airtime_to_Data_pin(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    network = models.ForeignKey(Network_1, on_delete=models.CASCADE)
    plan = models.ForeignKey(Airtime_to_data_Plan,
                             on_delete=models.SET_NULL, null=True)
    mobile_number = models.CharField(max_length=30, blank=True)
    Status = models.CharField(
        max_length=30, choices=status, default='processing')
    create_date = models.DateTimeField(default=timezone.now)
    pin = models.CharField(max_length=30, blank=True)
    Ported_number = models.BooleanField(default=False, blank=True, null=True)
    ident = models.CharField(default=create_id, editable=False, max_length=30)

    def __str__(self):
        return str(self.plan)

    def save(self, *args, **kwargs):
        if self.Status == 'failed':
            mb = CustomUser.objects.get(id=self.user.id)
            mb.deposit(mb.id, float(self.plan.plan_amount))
        super(Airtime_to_Data_pin, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('Airtime_to_Data_pin_success', args=[str(self.id)])


class Airtime_to_Data_tranfer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    plan = models.CharField(choices=Mtn_Tran_Plan, max_length=30, null=True)
    network = models.CharField(choices=Network_3, max_length=30, null=True)
    Transfer_number = models.CharField(max_length=30, blank=True)
    mobile_number = models.CharField(max_length=30, blank=True)
    Status = models.CharField(
        max_length=30, choices=status, default='processing')
    create_date = models.DateTimeField(default=timezone.now)
    Ported_number = models.BooleanField(default=False, blank=True, null=True)
    ident = models.CharField(default=create_id, editable=False, max_length=30)

    def __str__(self):
        return str(self.plan)

    def save(self, *args, **kwargs):
        if self.Status == 'failed':
            mb = CustomUser.objects.get(id=self.user.id)
            mb.deposit(mb.id, float(self.plan.plan_amount))
        super(Airtime_to_Data_tranfer, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('Airtime_to_Data_tranfer_success', args=[str(self.id)])


class Automation_control(models.Model):
    Network_good = models.BooleanField(default=False)
    network_name = models.OneToOneField(
        Network, on_delete=models.SET_NULL, null=True, unique=True, blank=True)

    def __str__(self):
        return str(self.network_name)


class Airtime_automation_control(models.Model):
    Network_good = models.BooleanField(default=False)
    network_name = models.OneToOneField(
        Network, on_delete=models.SET_NULL, null=True, unique=True, blank=True)

    def __str__(self):
        return str(self.network_name)


class Bankpayment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)

    Bank_paid_to = models.CharField(max_length=15, blank=True, null=True)
    Reference = models.CharField(max_length=15, blank=True, null=True)
    amount = models.CharField(max_length=30, blank=True, null=True)
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    Status = models.CharField(
        max_length=30, choices=status, default='processing')
    fund = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('Banksuccess', args=[str(self.id)])

    def save(self, *args, **kwargs):
        amount = self.amount
        if self.Status == 'successful' and self.fund == False:
            previous_bal = self.user.Account_Balance

            self.user.deposit(self.user.id, float(amount),False ,"Manual Bank Funding")
            self.fund = True
            Wallet_summary.objects.create(user=self.user, product="Manual Bank Funding", amount=amount,
                                          previous_balance=previous_bal, after_balance=(previous_bal + float(amount)))

        super(Bankpayment, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'MANUAL BANK FUNDING'


class paymentgateway(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    reference = models.CharField(null=True, blank=True, max_length=50)
    amount = models.FloatField(blank=True, null=True)
    Status = models.CharField(
        max_length=30, choices=status, default='processing')
    gateway = models.CharField(max_length=30, default="Paystack")
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = 'PAYMENT GATEWAY TRANSACTIONS'


class Cable(models.Model):
    name = models.CharField(max_length=30, choices=Multichoice, unique=True)
    status = models.CharField(max_length=30, choices=Netstatus)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'CABLE COMPANY'


class CablePlan(models.Model):
    cablename = models.ForeignKey(Cable, on_delete=models.CASCADE)
    plan_amount = models.PositiveIntegerField()
    product_code = models.CharField(max_length=200, blank=True, null=True)
    package = models.CharField(
        max_length=200, help_text="package(ie GOTV Plus)")
    hasAddon = models.BooleanField(default=False)
    Addon_name = models.CharField(
        max_length=200, help_text="package(ie Asian Add-on)", blank=True, null=True)
    addoncode = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.package) + str(self.Addon_name) + '----' + '#' + str(self.plan_amount)

    def plan_name(self):
        return str(self.package)

    def cableplanname(self):
        return str(self.cablename)

    def plan_amt(self):
        return str(self.plan_amount)

    def plan_id(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'CABLE SUBSCRIPTION PLAN'


class Cablesub(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    cablename = models.ForeignKey(Cable, on_delete=models.SET_NULL, null=True)
    cableplan = models.ForeignKey(
        CablePlan, on_delete=models.SET_NULL, null=True)
    smart_card_number = models.CharField(max_length=30, blank=True)
    balance_before = models.CharField(max_length=30, blank=True)
    balance_after = models.CharField(max_length=30, blank=True)
    plan_amount = models.CharField(max_length=30, blank=True)
    Status = models.CharField(max_length=30, choices=status, default='processing',
                              help_text="Select failed and save to refund user")
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    refund = models.BooleanField(default=False, blank=True, null=True)
    customer_name = models.CharField(max_length=70, blank=True, null=True)

    def __str__(self):
        return str(self.cableplan)

    def get_absolute_url(self):
        return reverse('cablesub_success', args=[str(self.id)])

    def save(self, *args, **kwargs):

        if self.Status == 'failed' and self.refund == False:
            previous_bal = self.user.Account_Balance
            self.user.deposit(self.user.id, float(self.plan_amount),False ,"Cablesub Refund")
            self.refund = True
            Wallet_summary.objects.create(user=self.user, product="{} N{} Cablesub Refund for {} ".format(self.cableplan.package, self.plan_amount,
                                                                                                          self.smart_card_number), amount=self.plan_amount, previous_balance=previous_bal, after_balance=(previous_bal + float(self.plan_amount)))

        super(Cablesub, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'CABLE SUBSCRIPTION TRANSACTIONS'


class Disco_provider_name(models.Model):
    name = models.CharField(max_length=150, unique=True)
    p_id = models.CharField(max_length=150, unique=True,
                            null=True, blank=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'DISCO PROVIDER NAMES'


config = WebsiteConfiguration.objects.first()
# config = ""

class KYC(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             editable=False, blank=False, null=True, related_name='Customer')
    First_Name = models.CharField(
        max_length=50, null=True, help_text="Your name here")
    Middle_Name = models.CharField(max_length=50, null=True,)
    Last_Name = models.CharField(max_length=50, null=True, help_text="Your Surname")
    DOB = models.DateField(null=True)
    Gender = models.CharField(max_length=6, null=True,)
    State_of_origin = models.CharField(max_length=100, null=True,)
    Local_gov_of_origin = models.CharField(max_length=100, null=True,)
    BVN = models.CharField(max_length=50, null=True,)
    passport_photogragh = models.ImageField(upload_to="passport_images", null=True, help_text="Maximum of 50kb in size", validators=[validate_file_size])

    status = models.CharField(max_length=20, null=True, choices=vericate, default="processing")
    dump = models.TextField()
    comment = models.TextField()
    primary_details_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'KYC'

    def save(self, *args, **kwargs):
        if self.status == "Approved":
            self.user.verify = True
            self.user.FullName = self.First_Name + " " +  self.Middle_Name + " " + self.Last_Name
            self.user.DOB = self.DOB
            self.user.BVN = self.BVN
            self.user.passport_photogragh = self.passport_photogragh
            self.user.State_of_origin = self.State_of_origin
            self.user.Local_gov_of_origin = self.Local_gov_of_origin
            self.user.Gender = self.Gender
            self.user.save()

            try:
                    body = {"bvn": self.BVN}
                    data = json.dumps(body)
                    ad = requests.post("https://api.monnify.com/api/v1/auth/login", auth=HTTPBasicAuth(
                    f'{config.monnify_API_KEY}', f'{config.monnify_SECRET_KEY}'))
                    mydata = json.loads(ad.text)
                    headers = {'Content-Type': 'application/json',"Authorization": "Bearer {}" .format(mydata['responseBody']["accessToken"])}
                    ab = requests.post(f"https://api.monnify.com/api/v1/bank-transfer/reserved-accounts/update-customer-bvn/{self.user.reservedaccountReference}", headers=headers, data=data)


            except:
                pass

            try:
                sendmail("KYC Approved Notification ",f"Dear {self.user.username} , your KYC varification has been Approved. your account daily transactions is now unlimited", self.user.email, self.user.username)
            except:
                pass

        if not self.id :
                try:
                    sendmail("User KYC Verification Notification ",f" {self.user.username} Just submitted his details for KYC verification", config.email, "Admin")
                except:
                    pass

        super(KYC, self).save(*args, **kwargs)

    def __str__(self):
        return '<img src="https://www.Husmodata.com/media/{}" height="150"/>'.format(self.passport_photogragh.url)

    def upload_passport(self):
        from django.utils.html import mark_safe
        return mark_safe('<img src="https://www.Husmodata.com/media/%s" width="150" height="150" />' % (self.passport_photogragh))

    upload_passport.short_description = 'Uploaded Passport'

    def bvn_passport(self):
        from django.utils.html import mark_safe
        data = json.loads(self.dump)
        img = data["response"]["base64Image"]
        img = "data:image/jpeg;base64,"+img
        print(img)
        return mark_safe('<img src="%s" width="150" height="150" />' % (img))

    bvn_passport.short_description = 'BVN Passport'

    def __str__(self):
        return str(self.user)



class Billpayment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    disco_name = models.ForeignKey(
        Disco_provider_name, on_delete=models.SET_NULL, null=True)
    amount = models.CharField(max_length=30)
    paid_amount = models.CharField(max_length=30, blank=True)
    balance_before = models.CharField(max_length=30, blank=True)
    balance_after = models.CharField(max_length=30, blank=True)
    meter_number = models.CharField(max_length=30, blank=True)
    token = models.CharField(max_length=200, blank=True, null=True)
    Customer_Phone = models.CharField(max_length=15, null=True)
    MeterType = models.CharField(max_length=30, choices=mtype, null=True)
    Status = models.CharField(max_length=30, choices=status, default='processing',
                              help_text="Select failed and save to refund user")
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)
    refund = models.BooleanField(default=False, blank=True, null=True)
    customer_name = models.CharField(max_length=250, blank=True, null=True)
    customer_address = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.disco_name)

    def get_absolute_url(self):
        return reverse('bill_success', args=[str(self.id)])

    def save(self, *args, **kwargs):

        if self.Status == 'failed' and self.refund == False:
            previous_bal = self.user.Account_Balance
            self.user.deposit(self.user.id, float(self.amount),False ,"Bill Payment Refund")
            self.refund = True
            Wallet_summary.objects.create(user=self.user, product="{} {}Bill Payment Refund for {} ".format(
                self.disco_name.name, self.amount, self.meter_number), amount=self.amount, previous_balance=previous_bal, after_balance=(previous_bal + float(self.amount)))

        elif self.token:

                def sendmessage(sender,message,to,route):
                             payload={
                                'sender':sender,
                                'to': to,
                                'message': message,
                                'type': '0',
                                'routing':route,
                                'token':'cYTj0CCFuGM4PSrvABkoANCBNlNF2SoipZFSNlz5hmKnejg6fubGLFu7Ph2URDj22dWGYjlRqDILQz7kHxARBlAwdC4CpTKHGC5D',
                                'schedule':'',
                                    }

                             baseurl = 'https://sms.hollatags.com/api/send/?user=oluwole1&pass=Pstsegunsss@c1&to={0}&from={1}&msg={2}'.format(to,sender,message)
                             response = requests.get(baseurl,verify=False)

                sendmessage('BILLTOKEN', "From datavilla your Bill Token is {0} ".format(
                    self.token), self.Customer_Phone, "02")

        super(Billpayment, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'BILL PAYMENT TRANSACTIONS'


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="blogimage", null=True, blank=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return '<img src="{}" height="150"/>'.format(self.image.url)
        Post.allow_tags = True

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])


class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True,
                            db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book_list_by_category', args=[self.slug])


class Book(models.Model):
    category = models.ForeignKey(
        Category, related_name='books', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    author = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='books/%Y/%m/%d', blank=True)

    class Meta:
        ordering = ('name', )
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('book_detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Book, self).save(*args, **kwargs)


class Book_order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
