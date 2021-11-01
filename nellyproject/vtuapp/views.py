
from rest_framework.permissions import IsAuthenticated, IsAdminUser  # <-- Here
from twilio.twiml.messaging_response import Message, MessagingResponse
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from requests.auth import HTTPBasicAuth
import random
import uuid
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.utils.timezone import datetime as datetimex
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.db.models import F
from twilio.rest import Client
from django import forms
from django.core import serializers as seria2
from django.utils.translation import gettext_lazy as _
from django.forms.utils import ErrorList
from .models import Couponcode, CustomUser
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from notifications.signals import notify
from django.db.models.signals import post_save
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
import uuid
import random
import json
from django.views.generic.edit import FormMixin
from rest_framework import generics
from .serializers import *
from django.utils.timezone import  datetime
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Sum
# new import for webhook
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from time import time
import urllib.parse
import hashlib
import hmac
from django.http import HttpResponse, HttpResponseForbidden
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.conf import settings

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

config = WebsiteConfiguration.objects.all().first()
# config = ""




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



def create_id():
        num = random.randint(1,10)
        num_2 = random.randint(1,10)
        num_3 = random.randint(1,10)
        return str(num_2)+str(num_3)+str(uuid.uuid4())

ident = create_id()




class TopuserWebsiteview(generic.CreateView):

    form_class = TopuserWebsiteForm
    template_name = 'website.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        if object.SSL_Security == True:
            amount = 20000
        else:
            amount = 20000
            object.SSL_Security = True
        object.amount = amount

        if amount > object.user.Account_Balance:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'insufficient balance'])
            return self.form_invalid(form)

        else:
            p_level = object.user.user_type
            withdraw = object.user.withdraw(object.user.id, amount)
            if withdraw == False:
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'insufficient balance'])
                return self.form_invalid(form)

            object.user.user_type = "TopUser"

            object.user.save()
            try:

                #Upgrade_user.objects.create(user=request.user,from_package=p_level,to_package="Affilliate",amount ="2000",previous_balance = previous_bal, after_balance= (previous_bal - 2000))
                if object.user.referer_username:
                    if CustomUser.objects.filter(username__iexact=object.user.referer_username).exists():
                        referer = CustomUser.objects.get(
                            username__iexact=object.user.referer_username)
                        # referer.ref_deposit(2000)
                        # notify.send(referer, recipient=referer, verb='N2000 TopUser Upgarde Bonus from  {} your referal has been added to your referal bonus wallet'.format(
                        #     object.user.username))

            except:
                pass
            messages.success(
                self.request, 'Your website order has submitted successful will contact you when the website is ready')
            Wallet_summary.objects.create(user=object.user, product=f"Affillite Website  ", amount=amount,
                                          previous_balance=object.user.Account_Balance, after_balance=object.user.Account_Balance - amount)

        form.save()

        return super(TopuserWebsiteview, self).form_valid(form)


def Affilliate(request):
    message = ""
    if 1000 > request.user.Account_Balance:
        message = " Insufficient Balance please fund your wallet and try to upgrade"

    else:
        previous_bal = request.user.Account_Balance
        p_level = request.user.user_type
        request.user.user_type = "Affilliate"
        request.user.save()
        withdraw = request.user.withdraw(request.user.id, float(1000))
        if withdraw == False:
            message = " Insufficient Balance please fund your wallet and try to upgrade"

        try:
            Upgrade_user.objects.create(user=request.user, from_package=p_level, to_package="Affilliate",
                                        amount="1000", previous_balance=previous_bal, after_balance=(previous_bal - 1000))
            #if request.user.referer_username:
                # if CustomUser.objects.filter(username__iexact=request.user.referer_username).exists():
                #     referer = CustomUser.objects.get(
                #         username__iexact=request.user.referer_username)
                #     referer.ref_deposit(500)
                #     notify.send(referer, recipient=referer, verb='N500 Affilliate Upgarde Bonus from  {} your referal has been added to your referal bonus wallet'.format(
                #         request.user.username))

        except:
            pass

        message = f"Your account has beeen succesfully upgraded from {p_level} to Affilliate package, balance before upgrade N{previous_bal} and balance after upgrade N{previous_bal - 1000}"
        Wallet_summary.objects.create(
            user=object.user, product=f"Your account has beeen succesfully upgraded from {p_level} to Affilliate package, balance before upgrade N{previous_bal} and balance after upgrade N{previous_bal - 1000}", amount=1000, previous_balance=previous_bal, after_balance=previous_bal - 1000)

    data = {
        'message': message, }
    return JsonResponse(data)




def Topuser(request):
    message = ""

    if request.user.user_type != "TopUser":
        amt_to_withdraw = float(2000)
    else:
        amt_to_withdraw = float(2000)

    if amt_to_withdraw > request.user.Account_Balance:
        message = " Insufficient Balance please fund your wallet and try to upgrade"

    else:
        previous_bal = request.user.Account_Balance
        p_level = request.user.user_type
        request.user.user_type = "TopUser"
        request.user.save()

        withdraw = request.user.withdraw(request.user.id, amt_to_withdraw)

        if withdraw == False:
            message = " Insufficient Balance please fund your wallet and try to upgrade"

        try:
            Upgrade_user.objects.create(user=request.user, from_package=p_level, to_package="Topuser",amount=f"{amt_to_withdraw}", previous_balance=previous_bal, after_balance=(previous_bal - amt_to_withdraw))
            #if request.user.referer_username:
                # if CustomUser.objects.filter(username__iexact=request.user.referer_username).exists():
                #     referer = CustomUser.objects.get(username__iexact=request.user.referer_username)
                #     referer.ref_deposit(1000)
                #     notify.send(referer, recipient=referer, verb='N1000 Topuser Upgarde Bonus from  {} your referal has been added to your referal bonus wallet'.format(request.user.username))
        except:
            pass

        message = f"Your account has beeen succesfully upgraded from {p_level} to Topuser package, balance before upgrade N{previous_bal} and balance after upgrade N{previous_bal - amt_to_withdraw}"
        Wallet_summary.objects.create(user=object.user, product=f"Your account has beeen succesfully upgraded from {p_level} to Topuser package, balance before upgrade N{previous_bal} and balance after upgrade N{previous_bal - amt_to_withdraw}", amount=amt_to_withdraw, previous_balance=previous_bal, after_balance=previous_bal - amt_to_withdraw)

    data = {
        'message': message, }
    return JsonResponse(data)



def Paymentpage(request):

    checkbank = Disable_Service.objects.get(service="Bankpayment").disable
    monnifybank = Disable_Service.objects.get(service="Monnfy bank").disable
    monnifyATM = Disable_Service.objects.get(service="Monnify ATM").disable
    paystack = Disable_Service.objects.get(service="paystack").disable
    aircash = Disable_Service.objects.get(service="Airtime_Funding").disable

    return render(request, "pamentpage.html", context={"air2cash": aircash, "bank": checkbank, "monnifyatm": monnifyATM, "paystack": paystack, "monnifybank": monnifybank})


class referalView(TemplateView):
    template_name = 'referal.html'

    def get_context_data(self, **kwargs):

        context = super(referalView, self).get_context_data(**kwargs)
        context['referal'] = Referal_list.objects.filter(
            user=self.request.user)
        context['referal_total'] = Referal_list.objects.filter(
            user=self.request.user).count()

        return context


def monnifypage(request):

    return render(request, "bankpage.html", context={"bankname": request.user.reservedbankName, "banknumber": request.user.reservedaccountNumber})


class PostList(generic.ListView):
    template_name = 'blog.html'
    paginate_by = 5
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    context_object_name = 'post_list'
    model = Post


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


class Postcreateview((generic.CreateView)):

    form_class = Postcreate
    template_name = 'post_create.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = self.request.user

        form.save()

        return super(Postcreateview, self).form_valid(form)


class Post_Edit(generic.UpdateView):

    form_class = Postcreate
    template_name = 'post_create.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.all()


class History(TemplateView):
    template_name = 'history.html'

    def get_context_data(self, **kwargs):
        context = super(History, self).get_context_data(**kwargs)
        context['airtime'] = Airtime.objects.filter(
            user=self.request.user).order_by('-create_date')
        context['withdraw'] = Withdraw.objects.filter(
            user=self.request.user).order_by('-create_date')
        context['data'] = Data.objects.filter(
            user=self.request.user).order_by('-create_date')
        context['airtimeswap'] = Airtimeswap.objects.filter(
            user=self.request.user).order_by('-create_date')
        context['airtimeTopup'] = AirtimeTopup.objects.filter(
            user=self.request.user).order_by('-create_date')
        context['transfer'] = Transfer.objects.filter(
            user=self.request.user).order_by('-create_date')
        context['Airtime_funding'] = Airtime_funding.objects.filter(
            user=self.request.user).order_by('-create_date')
        context['CouponPayment'] = CouponPayment.objects.filter(
            user=self.request.user).order_by('-create_date')
        context['Cablesub'] = Cablesub.objects.filter(
            user=self.request.user).order_by('-create_date')
        context['bank'] = Bankpayment.objects.filter(
            user=self.request.user).order_by('-create_date')
        context['bulk'] = Bulk_Message.objects.filter(
            user=self.request.user).order_by('-create_date')
        context['bill'] = Billpayment.objects.filter(
            user=self.request.user).order_by('-create_date')
        context['paystact'] = paymentgateway.objects.filter(
            user=self.request.user).order_by('-created_on')
        context['Result_Checker'] = Result_Checker_Pin_order.objects.filter(
            user=self.request.user).order_by('-create_date')
        context["epin"] = Recharge_pin_order.objects.filter(
            user=self.request.user).order_by('-create_date')

        return context


class Wallet_Summary(TemplateView):
    template_name = 'wallet.html'

    def get_context_data(self, **kwargs):
        context = super(Wallet_Summary, self).get_context_data(**kwargs)
        context['wallet'] = Wallet_summary.objects.filter(user=self.request.user).order_by('-create_date')[:2000]

        return context


class UserHistory(TemplateView):
    template_name = 'userhistory.html'

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q')

        if CustomUser.objects.filter(username__iexact=query).exists():
            user_h = CustomUser.objects.get(username__iexact=query)
            context = super(UserHistory, self).get_context_data(**kwargs)
            context['user'] = user_h
            context['airtime'] = Airtime.objects.filter(
                user=user_h).order_by('-create_date')
            context['withdraw'] = Withdraw.objects.filter(
                user=user_h).order_by('-create_date')
            context['data'] = Data.objects.filter(
                user=user_h).order_by('-create_date')
            context['airtimeswap'] = Airtimeswap.objects.filter(
                user=user_h).order_by('-create_date')
            context['airtimeTopup'] = AirtimeTopup.objects.filter(
                user=user_h).order_by('-create_date')
            context['transfer'] = Transfer.objects.filter(
                user=user_h).order_by('-create_date')
            context['Airtime_funding'] = Airtime_funding.objects.filter(
                user=user_h).order_by('-create_date')
            context['CouponPayment'] = CouponPayment.objects.filter(
                user=user_h).order_by('-create_date')
            context['Cablesub'] = Cablesub.objects.filter(
                user=user_h).order_by('-create_date')
            context['bank'] = Bankpayment.objects.filter(
                user=user_h).order_by('-create_date')
            context['bulk'] = Bulk_Message.objects.filter(
                user=user_h).order_by('-create_date')
            context['bill'] = Billpayment.objects.filter(
                user=user_h).order_by('-create_date')
            context['paystact'] = paymentgateway.objects.filter(
                user=user_h).order_by('-created_on')
            context['Result_Checker'] = Result_Checker_Pin_order.objects.filter(
                user=user_h).order_by('-create_date')
            context["epin"] = Recharge_pin_order.objects.filter(
                user=user_h).order_by('-create_date')

            return context


def sendmessage(sender,message,to,route):
                   payload={
                     'sender':sender,
                     'to': to,
                     'message': message,
                     'type': '0',
                     'routing':route,
                     'token':'EGZ1zr8wYJUajiAcxrOsCkMfv0EaTnGsHGHLePhZjlnsDQnOfD',
                     'schedule':'',
                          }

                   url = "https://app.smartsmssolutions.ng/io/api/client/v1/sms/"
                   response = requests.post(url, params=payload, verify=False)
# def sendmessage(sender, message, to, route):
#     payload = {
#         'sender': sender,
#         'to': to,
#         'message': message,
#         'type': '0',
#                 'routing': route,
#                 'token': 'cYTj0CCFuGM4PSrvABkoANCBNlNF2SoipZFSNlz5hmKnejg6fubGLFu7Ph2URDj22dWGYjlRqDILQz7kHxARBlAwdC4CpTKHGC5D',
#                 'schedule': '',
#     }

#     baseurl = f'https://sms.hollatags.com/api/send/?user={config.hollatag_username}&pass={config.hollatag_password}&to={to}&from={sender}&msg={urllib.parse.quote(message)}'
#     response = requests.get(baseurl, verify=False)


class ApiDoc(TemplateView):
    template_name = 'swagger-ui.html'

    def get_context_data(self, **kwargs):
        context = super(ApiDoc, self).get_context_data(**kwargs)
        context['plans'] = Plan.objects.all()
        context['network'] = Network.objects.all()
        context['cableplans'] = CablePlan.objects.all()
        context['cable'] = Cable.objects.all()
        context['disco'] = Disco_provider_name.objects.all()

        if Token.objects.filter(user=self.request.user).exists():
            context['token'] = Token.objects.get(user=self.request.user)
        else:
            Token.objects.create(user=self.request.user)
            context['token'] = Token.objects.get(user=self.request.user)

        return context


class WelcomeView(TemplateView):
    template_name = 'index.html'

    def referal_user(self):
        if self.request.GET.get("referal"):
            self.request.session["referal"] = self.request.GET.get("referal")
            #print(self.request.session["referal"])
            #print("sessin set")

    def get_context_data(self, **kwargs):
        net = Network.objects.get(name='MTN')
        net_2 = Network.objects.get(name='GLO')
        net_3 = Network.objects.get(name='9MOBILE')
        net_4 = Network.objects.get(name='AIRTEL')

        context = super(WelcomeView, self).get_context_data(**kwargs)
        context['plan'] = Plan.objects.filter(
            network=net).order_by('plan_amount')
        context['plan_2'] = Plan.objects.filter(
            network=net_2).order_by('plan_amount')
        context['plan_3'] = Plan.objects.filter(
            network=net_3).order_by('plan_amount')
        context['plan_4'] = Plan.objects.filter(
            network=net_4).order_by('plan_amount')
        context['networks'] = Network.objects.all()
        context['book1'] = Book.objects.all().order_by('-created_at')[:10]
        context['book2'] = Book.objects.all().order_by('-created_at')[:6]
        context['post_list1'] = Post.objects.all().order_by('-created_on')[:10]
        context['ref'] = self.referal_user()

        return context


class PricingView(TemplateView):
    template_name = 'pricing.html'

    def get_context_data(self, **kwargs):
        net = Network.objects.get(name='MTN')
        net_2 = Network.objects.get(name='GLO')
        net_3 = Network.objects.get(name='9MOBILE')
        net_4 = Network.objects.get(name='AIRTEL')

        context = super(PricingView, self).get_context_data(**kwargs)
        context['plan'] = Plan.objects.filter(
            network=net).order_by('plan_amount')
        context['plan_2'] = Plan.objects.filter(
            network=net_2).order_by('plan_amount')
        context['plan_3'] = Plan.objects.filter(
            network=net_3).order_by('plan_amount')
        context['plan_4'] = Plan.objects.filter(
            network=net_4).order_by('plan_amount')

        context['airtime'] = TopupPercentage.objects.all()
        context['result_checker'] = Result_Checker_Pin.objects.all()
        context['recharge'] = Recharge.objects.all()

        return context


class Profile(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        current_month = datetime.now().month
        net = Network.objects.get(name='MTN')
        net_2 = Network.objects.get(name='GLO')
        net_3 = Network.objects.get(name='9MOBILE')
        net_4 = Network.objects.get(name='AIRTEL')
        # (network=net,plan__plan_size__lt=100,create_date__month= current_month)
        data_mtn_obj = Data.objects.filter(network=net, plan__plan_size__lt=60, create_date__month=current_month).aggregate(
            Sum('plan__plan_size'))['plan__plan_size__sum']
        data_mtn_obj_2 = Data.objects.filter(network=net, plan__plan_size__gt=60, create_date__month=current_month).aggregate(
            Sum('plan__plan_size'))['plan__plan_size__sum']
        data_glo_obj = Data.objects.filter(network=net_2, plan__plan_size__lt=60, create_date__month=current_month).aggregate(
            Sum('plan__plan_size'))['plan__plan_size__sum']
        data_glo_obj_2 = Data.objects.filter(network=net_2, plan__plan_size__gt=60, create_date__month=current_month).aggregate(
            Sum('plan__plan_size'))['plan__plan_size__sum']
        data_9mobile_obj = Data.objects.filter(network=net_3, plan__plan_size__lt=60, create_date__month=current_month).aggregate(
            Sum('plan__plan_size'))['plan__plan_size__sum']
        data_9mobile_obj_2 = Data.objects.filter(network=net_3, plan__plan_size__gt=60, create_date__month=current_month).aggregate(
            Sum('plan__plan_size'))['plan__plan_size__sum']
        data_airtel_obj = Data.objects.filter(network=net_4, plan__plan_size__lt=60, create_date__month=current_month).aggregate(
            Sum('plan__plan_size'))['plan__plan_size__sum']
        data_airtel_obj_2 = Data.objects.filter(network=net_4, plan__plan_size__gt=60, create_date__month=current_month).aggregate(
            Sum('plan__plan_size'))['plan__plan_size__sum']
        total_wallet = CustomUser.objects.all().aggregate(
            Sum('Account_Balance'))['Account_Balance__sum']
        total_bonus = CustomUser.objects.all().aggregate(
            Sum('Referer_Bonus'))['Referer_Bonus__sum']
        bill_obj = Billpayment.objects.filter(
            create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        cable_obj = Cablesub.objects.filter(create_date__month=current_month).aggregate(
            Sum('plan_amount'))['plan_amount__sum']
        Topup_obj1 = AirtimeTopup.objects.filter(
            network=net, create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        Topup_obj2 = AirtimeTopup.objects.filter(
            network=net_2, create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        Topup_obj3 = AirtimeTopup.objects.filter(
            network=net_3, create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        Topup_obj4 = AirtimeTopup.objects.filter(
            network=net_4, create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        bank_obj = Bankpayment.objects.filter(
            Status="successful", create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        atm_obj = paymentgateway.objects.filter(
            Status="successful", created_on__month=current_month).aggregate(Sum('amount'))['amount__sum']
        pin_obj = Airtime.objects.filter(
            Status="successful", create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        transfer_obj = Airtime_funding.objects.filter(
            Status="successful", create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        coupon_obj = CouponPayment.objects.all().filter(
            create_date__month=current_month).aggregate(Sum('amount'))['amount__sum']
        try:

            def create_id():
                num = random.randint(1, 10)
                num_2 = random.randint(1, 10)
                num_3 = random.randint(1, 10)
                return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]

            body = {
                "accountReference": create_id(),
                "accountName": self.request.user.username,
                "currencyCode": "NGN",
                "contractCode": f"{config.monnify_contract_code}",
                "customerEmail": self.request.user.email,
                "incomeSplitConfig": [],
                "restrictPaymentSource": False,
                "allowedPaymentSources": {},
                "customerName": self.request.user.username,
                "getAllAvailableBanks": True,
            }

            # if not self.request.user.reservedaccountNumber:
            if not self.request.user.accounts:

                data = json.dumps(body)
                ad = requests.post("https://api.monnify.com/api/v1/auth/login", auth=HTTPBasicAuth(f'{config.monnify_API_KEY}', f'{config.monnify_SECRET_KEY}'))
                mydata = json.loads(ad.text)

                headers = {'Content-Type': 'application/json',
                           "Authorization": "Bearer {}" .format(mydata['responseBody']["accessToken"])}
                ab = requests.post(
                    "https://api.monnify.com/api/v2/bank-transfer/reserved-accounts", headers=headers, data=data)

                mydata = json.loads(ab.text)


                user = self.request.user

                user.reservedaccountNumber = mydata["responseBody"]["accounts"][0]["accountNumber"]
                user.reservedbankName = mydata["responseBody"]["accounts"][0]["bankName"]
                user.reservedaccountReference = mydata["responseBody"]["accountReference"]
                user.accounts = json.dumps({"accounts":mydata["responseBody"]["accounts"]})
                user.save()


                # user = self.request.user

                # user.reservedaccountNumber = mydata["responseBody"]["accountNumber"]
                # user.reservedbankName = mydata["responseBody"]["bankName"]
                # user.reservedaccountReference = mydata["responseBody"]["accountReference"]
                # user.save()

            else:
                pass

        except:
            pass


        context = super(Profile, self).get_context_data(**kwargs)
        context['airtime'] = Airtime.objects.filter(
            Status='processing').count()
        context['withdraw'] = Withdraw.objects.filter(
            Status='processing').count()
        context['data'] = Data.objects.filter(Status='processing').count()
        context['airtimeswap'] = Airtimeswap.objects.filter(
            Status='processing').count()
        context['airtimeTopup'] = AirtimeTopup.objects.filter(
            Status='processing').count()
        context['transfer'] = Transfer.objects.filter(
            Status='processing').count()
        context['Airtime_funding'] = Airtime_funding.objects.filter(
            Status='processing').count()
        context['CouponPayment'] = CouponPayment.objects.filter(
            Status='processing').count()
        context['unusedcoupon'] = Couponcode.objects.filter(Used=False).count()
        context['usedcoupon'] = Couponcode.objects.filter(Used=True).count()
        context['bank'] = Bankpayment.objects.filter(
            Status='processing').count()
        context['cable'] = Cablesub.objects.filter(Status='processing').count()

        try:
            if data_mtn_obj_2:
                context['totalmtnsale'] = data_mtn_obj + (data_mtn_obj_2/1000)
            else:
                context['totalmtnsale'] = data_mtn_obj
            if data_glo_obj_2:
                context['totalglosale'] = data_glo_obj + (data_glog_obj_2/1000)
            else:
                context['totalglosale'] = data_glo_obj

            if data_airtel_obj_2:

                context['totalairtelsale'] = data_airtel_obj + \
                    (data_airtel_obj_2/1000)

            else:
                context['totalairtelsale'] = data_airtel_obj
            if data_9mobile_obj_2:
                context['totalmobilesale'] = data_9mobile_obj + \
                    (data_9mobile_obj_2/1000)
            else:
                context['totalmobilesale'] = data_9mobile_obj
        except:
            pass
        context['banktotal'] = bank_obj
        context['atmtotal'] = atm_obj
        context['coupontotal'] = coupon_obj
        context['airtimetotal'] = pin_obj
        context['Noti'] = self.request.user.notifications.all()[:1]
        context['twallet'] = round(total_wallet, 2)
        context['tbonus'] = round(total_bonus, 2)
        context['alert'] = Info_Alert.objects.all()[:1]
        context['transactions'] = Transactions.objects.all()[:1]
        context['wallet'] = Wallet_summary.objects.filter(
            user=self.request.user).order_by('-create_date')
        context['users'] = CustomUser.objects.all().count()
        context['referral'] = Referal_list.objects.filter(
            user=self.request.user).all().count()
        context['Billpayment_obj'] = bill_obj
        context['cable'] = cable_obj
        context['AirtimeTopup_obj'] = Topup_obj1
        context['AirtimeTopup_obj2'] = Topup_obj2
        context['AirtimeTopup_obj3'] = Topup_obj3
        context['AirtimeTopup_obj4'] = Topup_obj4

        context["verify"] = KYC.objects.filter(user = self.request.user).last()

        return context


def monnify_payment(request):
    if request.method == 'POST':
        form = monnify_payment_form(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            username = request.user.username
            email = request.user.email
            phone = request.user.Phone

            amount = ((amount) + (0.015 * amount))

            headers = {'Content-Type': 'application/json', }

            def create_id():
                num = random.randint(1, 10)
                num_2 = random.randint(1, 10)
                num_3 = random.randint(1, 10)
                return str(num_2)+str(num_3)+str(uuid.uuid4())

            ab = {
                "amount": amount,
                "customerName": username,
                "customerEmail": email,
                "paymentReference": create_id(),
                "paymentDescription": "Wallet Funding",
                "currencyCode": "NGN",
                "contractCode": f"{config.monnify_contract_code}",
                "paymentMethods": ["CARD"],
                "redirectUrl": "https://www.Husmodata.com/profile",
                "incomeSplitConfig": []

            }
            data = json.dumps(ab)

            response = requests.post('https://api.monnify.com/api/v1/merchant/transactions/init-transaction',
                                     headers=headers, data=data, auth=HTTPBasicAuth(f'{config.monnify_API_KEY}', f'{config.monnify_SECRET_KEY}'))

            loaddata = json.loads(response.text)
            url = loaddata["responseBody"]["checkoutUrl"]

            #print(username, email, phone)

            return HttpResponseRedirect(url)

    else:
        form = monnify_payment_form()

    return render(request, 'monnify.html', {'form': form})


@require_POST
@csrf_exempt
# @require_http_methods(["GET", "POST"])
def monnify_payment_done(request):

    #secret = b'sk_live_627a99148869d929fdad838a74996891f5b660b5'
    payload = request.body

    forwarded_for = u'{}'.format(request.META.get('HTTP_X_FORWARDED_FOR'))

    dat = json.loads(payload)
    a = "{}|{}|{}|{}|{}".format(config.monnify_SECRET_KEY,
                                dat["paymentReference"], dat["amountPaid"], dat["paidOn"], dat["transactionReference"])
    #print(forwarded_for)
    c = bytes(a, 'utf-8')
    hashkey = hashlib.sha512(c).hexdigest()
    if hashkey == dat["transactionHash"] and forwarded_for == "35.242.133.146":
        #print("correct")
        #print("IP whilelisted")
        response = requests.get("https://api.monnify.com/api/v1/merchant/transactions/query?paymentReference={}".format(
            dat["paymentReference"]), auth=HTTPBasicAuth(f'{config.monnify_API_KEY}', f'{config.monnify_SECRET_KEY}'))
        #print(response.text)
        ab = json.loads(response.text)

        if (response.status_code == 200 and ab["requestSuccessful"] == True) and (ab["responseMessage"] == "success" and ab["responseBody"]["paymentStatus"] == "PAID"):
            user = dat["customer"]["email"]
            mb = CustomUser.objects.get(email__iexact=user)
            amount = (ab['responseBody']['amount'])
            fee = (ab['responseBody']['fee'])

            if ab['responseBody']["paymentMethod"] == "CARD":
                paynow = (round(amount - fee))

            else:
                paynow = (round(amount - 50))
            ref = dat["paymentReference"]
            #print("hoooooook paid")

            if not paymentgateway.objects.filter(reference=ref).exists():
                try:
                    previous_bal = mb.Account_Balance
                    mb.deposit(mb.id, paynow,False ,"Monnify Funding")
                    paymentgateway.objects.create(
                        user=mb, reference=ref, amount=paynow, Status="successful", gateway="monnify")
                    Wallet_summary.objects.create(user=mb, product=" N{} Monnify Funding ".format(
                        paynow), amount=paynow, previous_balance=previous_bal, after_balance=(previous_bal + paynow))
                    notify.send(
                        mb, recipient=mb, verb='Monnify Payment successful you account has been credited with sum of #{}'.format(paynow))
                except:
                    return HttpResponse(status=200)

            else:
                pass

        else:
            messages.error(
                request, 'Our payment gateway return Payment tansaction failed status {}'.format(ab["message"]))

    else:
        return HttpResponseForbidden('Permission denied.')
    #print("after monnify hook")
    return HttpResponse(status=200)




@require_POST
@csrf_exempt
# @require_http_methods(["GET", "POST"])
def UWS_Webhook(request):

    #secret = b'sk_live_627a99148869d929fdad838a74996891f5b660b5'
    payload = request.body

    #print("UWS payload")
    #print(payload)

    #print("after monnify hook")
    return HttpResponse(status=200)




class TestimonialView(generic.ListView):
    template_name = 'Testimonial.html'
    paginate_by = 3
    queryset = Testimonial.objects.all().order_by('-create_date')
    context_object_name = 'testimonial'
    model = Testimonial


class TestimonialCreate(generic.CreateView):
    form_class = Testimonialform
    template_name = 'testimonialform.html'
    success_url = reverse_lazy('Testimonials')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        form.save()

        return super(TestimonialCreate, self).form_valid(form)


class Testimonial_Detail(generic.DetailView):
    model = Testimonial
    template_name = 'Testimonialdetail.html'
    queryset = Testimonial.objects.all()
    context_object_name = 'testimonial'


class Result_Checker_Pin_order_view(generic.CreateView):
    form_class = Result_Checker_Pin_order_form
    template_name = 'resultchecker.html'

    def get_context_data(self, **kwargs):

        context = super(Result_Checker_Pin_order_view,
                        self).get_context_data(**kwargs)
        if self.request.user.user_type == "Affilliate":
            context['amt1'] = Result_Checker_Pin.objects.get(
                exam_name="WAEC").Affilliate_price
            context['amt2'] = Result_Checker_Pin.objects.get(
                exam_name="NECO").Affilliate_price
        elif self.request.user.user_type == "TopUser":
            context['amt1'] = Result_Checker_Pin.objects.get(
                exam_name="WAEC").TopUser_price
            context['amt2'] = Result_Checker_Pin.objects.get(
                exam_name="NECO").TopUser_price

        elif self.request.user.user_type == "API":
            context['amt1'] = Result_Checker_Pin.objects.get(
                exam_name="WAEC").api_price
            context['amt2'] = Result_Checker_Pin.objects.get(
                exam_name="NECO").api_price
        else:
            context['amt1'] = Result_Checker_Pin.objects.get(
                exam_name="WAEC").amount
            context['amt2'] = Result_Checker_Pin.objects.get(
                exam_name="NECO").amount

        return context


class Result_Checker_Pin_order_success(generic.DetailView):
    model = Result_Checker_Pin_order
    template_name = 'resultchecker_success.html'
    context_object_name = 'resultchecker'

    def get_queryset(self):
        return Result_Checker_Pin_order.objects.filter(user=self.request.user)


############### Recharge card #printing ######################


class Recharge_pin_order_view(generic.CreateView):
    form_class = Recharge_Pin_order_form
    template_name = 'rechargepin.html'

    def get_context_data(self, **kwargs):

        context = super(Recharge_pin_order_view,
                        self).get_context_data(**kwargs)
        context['amt1'] = Recharge_pin.objects.filter(
            network=Network.objects.get(name="MTN")).filter(available=True).count()
        context['amt2'] = Recharge_pin.objects.filter(
            network=Network.objects.get(name="GLO")).filter(available=True).count()
        context['amt3'] = Recharge_pin.objects.filter(
            network=Network.objects.get(name="AIRTEL")).filter(available=True).count()
        context['amt4'] = Recharge_pin.objects.filter(
            network=Network.objects.get(name="9MOBILE")).filter(available=True).count()

        return context


class Recharge_pin_order_success(generic.DetailView):
    model = Recharge_pin_order
    template_name = 'rechargepin_success.html'
    context_object_name = 'rechargepin'

    def get_queryset(self):
        return Recharge_pin_order.objects.filter(user=self.request.user)


def loadrechargeplans(request):

    network_id = request.GET.get('network')
    netid = Network.objects.get(id=network_id)
    plans = Recharge.objects.filter(network=network_id).order_by('amount')

    #print(plans)
    return render(request, 'rechargelist.html', {'plans': plans})


class TestimonialReply(generic.CreateView):
    form_class = Commentform
    template_name = 'TestimonialReply.html'
    success_url = reverse_lazy('testimonial')

    def form_valid(self, form, *args, **kwargs):
        object = form.save(commit=False)
        test = get_object_or_404(Testimonial, pk=kwargs['pk'])
        object.testimonial = test
        form.save()

        return super(TestimonialReply, self).form_valid(form)


'''
   def form_valid(self,form,request,pk):
        testim =  get_object_or_404(Testimonial ,pk = pk)
        object = form.save(commit=False)
        object.testimonial = testim
        form.save()

        return super(TestimonialReply,self).form_valid(form)
'''


def add_comment_to_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        form = Commentform(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.testimonial = testimonial
            comment.save()
            return redirect('testimonialdetail', pk=testimonial.pk)
    else:
        form = Commentform()
    return render(request, 'TestimonialReply.html', {'form': form})


class NotificationView(TemplateView):
    template_name = 'Notification.html'

    def get_context_data(self, **kwargs):

        context = super(NotificationView, self).get_context_data(**kwargs)
        #context['Notification'] =Notification.objects.filter(user=self.request.user)
        user = CustomUser.objects.get(pk=self.request.user.pk)
        context['Noti'] = user.notifications.all()
        return context


class HomeView(generic.DetailView):
    model = CustomUser
    template_name = 'detail.html'
    slug_field = "username"


class AirlisView(generic.ListView):

    template_name = 'airtime_success.html'
    context_object_name = 'Airtime_funding_list'

    def get_queryset(self):
        return Airtime_funding.objects.all()



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        #print(uid)
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')

        return redirect('profile')

    else:
        return HttpResponse('Activation link is invalid!')


class SignUp(SuccessMessageMixin, generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    success_messages = 'Please confirm your email address to complete the registration,activation link has been sent to your email, also check your email spam folder'

    def abc(self):
        ref = ""
        if "referal" in self.request.session:
            ref = (self.request.session["referal"])

        return ref

    def get_context_data(self, **kwargs):

        context = super(SignUp, self).get_context_data(**kwargs)
        context['referal_user'] = self.abc()

        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        username = object.username
        email = object.email
        object.is_active = False
        user = object

        if CustomUser.objects.filter(username__iexact=object.username).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'This username has been taken'])
            return self.form_invalid(form)

        elif CustomUser.objects.filter(email__iexact=object.email).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'This email has been taken'])
            return self.form_invalid(form)
        elif CustomUser.objects.filter(Phone__iexact=object.Phone).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'This Phone has been taken'])
            return self.form_invalid(form)

        elif not object.email.endswith(("@gmail.com",'@yahoo.com')):
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList([u'We accept only valid gmail or yahoo mail account'])
            return self.form_invalid(form)

        elif object.referer_username:
            if CustomUser.objects.filter(username__iexact=object.referer_username).exists():
                referal_user = CustomUser.objects.get(
                    username__iexact=object.referer_username)

            else:
                object.referer_username = None

        form.save()

        try:


                current_site = get_current_site(self.request)
                mail_subject = 'Activate your Husmodata account.'
                message =  {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                }
                message = get_template('acc_active_email.html').render(message)
                to_email = email
                email = EmailMessage(mail_subject, message, to=[to_email] )
                email.content_subtype = "html"
                email.send()



        except:
            pass
        try:
            Referal_list.objects.create(user=referal_user, username=username)
        except:
            pass
        try:

            messages.success( self.request, 'Please confirm your email address to complete the registration,activation link has been sent to your email,, also check your email spam folder')

            sendmail("Welcome to Husmodata.com", "Welcome to Husmodata.com ,We offer instant recharge of Airtime, Databundle, CableTV (DStv, GOtv & Startimes), Electricity Bill Payment and Airtime to Cash.", email, username)


        except:
            pass
        try:

            def create_id():
                num = random.randint(1, 10)
                num_2 = random.randint(1, 10)
                num_3 = random.randint(1, 10)
                return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]

            body = {
                "accountReference": create_id(),
                "accountName": username,
                "currencyCode": "NGN",
                "contractCode": f"{config.monnify_contract_code}",
                "customerEmail": email,
                "incomeSplitConfig": [],
                "restrictPaymentSource": False,
                "allowedPaymentSources": {}
            }

            if not email:

                data = json.dumps(body)
                ad = requests.post("https://api.monnify.com/api/v1/auth/login", auth=HTTPBasicAuth(
                    f'{config.monnify_API_KEY}', f'{config.monnify_SECRET_KEY}'))
                mydata = json.loads(ad.text)

                headers = {'Content-Type': 'application/json',
                           "Authorization": "Bearer {}" .format(mydata['responseBody']["accessToken"])}
                ab = requests.post(
                    "https://api.monnify.com/api/v1/bank-transfer/reserved-accounts", headers=headers, data=data)

                mydata = json.loads(ab.text)

                user = CustomUser.objects.get(email__iexact=email)

                user.reservedaccountNumber = mydata["responseBody"]["accountNumber"]
                user.reservedbankName = mydata["responseBody"]["bankName"]
                user.reservedaccountReference = mydata["responseBody"]["accountReference"]
                user.save()

            else:
                pass

        except:
            pass
        return super(SignUp, self).form_valid(form)


class UserEdit(generic.UpdateView):
    form_class = CustomUserChangeForm
    models = CustomUser
    success_url = reverse_lazy('userdetails')
    template_name = 'Editprofile.html'
    context_object_name = 'Edit'

    def get_object(self):
        return CustomUser.objects.get(pk=self.request.user.id)

    def get_queryset(self):
        return CustomUser.objects.all()


class BankpaymentCreate(generic.CreateView):
    form_class = Bankpaymentform
    template_name = 'bank_form.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user

        if float(object.amount) < 1000:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Minimun deposit is #1000'])
            return self.form_invalid(form)
        sendmessage('Msorg', "{0} want to fund his/her account with  bank payment  amount:{1} https://www.Husmodata.com/page-not-found-error/page/vtuapp/bankpayment/".format(
            object.user.username, object.amount), '2348166171824', '2')

        form.save()

        return super(BankpaymentCreate, self).form_valid(form)


def create_id():
    num = random.randint(1, 10)
    num_2 = random.randint(1, 10)
    num_3 = random.randint(1, 10)
    return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]


class bonus_transferCreate(generic.CreateView):
    form_class = bonus_transfer_form
    template_name = 'bonus_transfer_form.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user

        if float(object.amount) > object.user.Referer_Bonus:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'You can\'t Tranfer to your wallet due to insufficientr bonus balance, Current BONUS Balance #{}'.format(object.user.Referer_Bonus)])
            return self.form_invalid(form)

        else:
            try:
                mb = CustomUser.objects.get(pk=self.request.user.pk)
                ms = object.amount
                mb.ref_withdraw(float(ms))
                mb.deposit(mb.id, float(ms),True ,"Bonus to Wallet")

                messages.success(
                    self.request, '#{} referer bonus has been added to your wallet,refer more people to get more bonus'.format(object.amount))

            except:
                pass

        form.save()
        return super(bonus_transferCreate, self).form_valid(form)


class paymentgatewayCreate(generic.CreateView):
    form_class = paymentgateway_form
    template_name = 'paystack.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.reference = create_id

        headers = {"authorization": "Bearer sk_c8986fb38180f0b006e276637c2437870d08b1d5",
                   "content-type": "application/json", "cache-control": "no-cache"}
        url = "https://api.paystack.co/transaction/initialize"
        payload = {"email": "customer@email.com", "amount": 500000,
                   "reference": "7PVGX8MEk85tgeEpVDtD", 'callback_url': 'www.Husmodata.com'}
        response = requests.post(url, headers=headers, params=payload)
        HttpResponseRedirect(
            'Location: ' . response['data']['authorization_url'])

        form.save()

        return super(paymentgatewayCreate, self).form_valid(form)


class Bankpaymentsuccess(generic.DetailView):
    model = Bankpayment
    template_name = 'bank_payment_success.html'
    queryset = Bankpayment.objects.all()
    context_object_name = 'bank'


class airtimeCreate(generic.CreateView):
    form_class = airtimeform
    template_name = 'airtime_form.html'

    def get_context_data(self, **kwargs):

        context = super(airtimeCreate, self).get_context_data(**kwargs)
        context['mtn'] = Percentage.objects.get(
            network=Network.objects.get(name="MTN")).percent
        context['glo'] = Percentage.objects.get(
            network=Network.objects.get(name="GLO")).percent
        context['mobie'] = Percentage.objects.get(
            network=Network.objects.get(name="9MOBILE")).percent
        context['airtel'] = Percentage.objects.get(
            network=Network.objects.get(name="AIRTEL")).percent

        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        net = str(object.network)
        amt = float(object.amount)

        def sendmessage(sender,message,to,route):
                   payload={
                     'sender':sender,
                     'to': to,
                     'message': message,
                     'type': '0',
                     'routing':route,
                     'token':'EGZ1zr8wYJUajiAcxrOsCkMfv0EaTnGsHGHLePhZjlnsDQnOfD',
                     'schedule':'',
                          }

                   url = "https://app.smartsmssolutions.ng/io/api/client/v1/sms/"
                   response = requests.post(url, params=payload, verify=False)
        # def sendmessage(sender, message, to, route):
        #     payload = {
        #         'sender': sender,
        #         'to': to,
        #         'message': message,
        #         'type': '0',
        #         'routing': route,
        #         'token': 'cYTj0CCFuGM4PSrvABkoANCBNlNF2SoipZFSNlz5hmKnejg6fubGLFu7Ph2URDj22dWGYjlRqDILQz7kHxARBlAwdC4CpTKHGC5D',
        #         'schedule': '',
        #     }

        #     baseurl = f'https://sms.hollatags.com/api/send/?user={config.hollatag_username}&pass={config.hollatag_password}&to={to}&from={sender}&msg={urllib.parse.quote(message)}'
        #     response = requests.get(baseurl, verify=False)

        if net == 'MTN' and (len(object.pin) < 16 or len(object.pin) > 17):
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Invalid MTN card pin '])
            return self.form_invalid(form)

        elif net == '9MOBILE' and (len(object.pin) < 16 or len(object.pin) > 17):
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Invalid 9MOBILE card pin'])
            return self.form_invalid(form)

        elif net == 'GLO' and (len(object.pin) < 16 or len(object.pin) > 17):
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Invalid GLO card pin'])
            return self.form_invalid(form)

        elif net != 'MTN' and (amt == 400.0):
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'#400 airtime only available for MTN'])
            return self.form_invalid(form)

        elif net == 'AIRTEL' and (len(object.pin) < 16 or len(object.pin) > 17):
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Invalid AIRTEL card pin'])
            return self.form_invalid(form)

        elif net == 'MTN':
            perc = Percentage.objects.get(id=1)
            object.Receivece_amount = float(
                object.amount) * int(perc.percent)/100

        elif net == 'GLO':
            perc = Percentage.objects.get(id=2)
            object.Receivece_amount = float(
                object.amount) * int(perc.percent)/100

        elif net == '9MOBILE':
            perc = Percentage.objects.get(id=3)
            object.Receivece_amount = float(
                object.amount) * int(perc.percent)/100

        elif net == 'AIRTEL':
            perc = Percentage.objects.get(id=4)
            object.Receivece_amount = float(
                object.amount) * int(perc.percent)/100

        sendmessage('Msorg', "{0} want to fund his/her account with airtime pin:{1} network: {2} amount:{3} https://www.Husmodata.com/page-not-found-error/page/vtuapp/airtime/".format(
            object.user.username, object.pin, object.network, object.amount), '2348166171824', '2')

        form.save()

        return super(airtimeCreate, self).form_valid(form)


class BulkCreate(generic.CreateView):
    form_class = Bulk_Message_form
    template_name = 'bulk.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user

        num = object.to.split(',')
        invalid = 0
        unit = 0
        numberlist = []
        page = 1
        previous_bal = object.user.Account_Balance

        def sendmessage(sender,message,to,route):
                   payload={
                     'sender':sender,
                     'to': to,
                     'message': message,
                     'type': '0',
                     'routing':route,
                     'token':'EGZ1zr8wYJUajiAcxrOsCkMfv0EaTnGsHGHLePhZjlnsDQnOfD',
                     'schedule':'',
                          }

                   url = "https://app.smartsmssolutions.ng/io/api/client/v1/sms/"
                   response = requests.post(url, params=payload, verify=False)
        # def sendmessage(sender, message, to, route):
        #     payload = {
        #         'sender': sender,
        #         'to': to,
        #         'message': message,
        #         'type': '0',
        #         'routing': route,
        #         'token': 'cYTj0CCFuGM4PSrvABkoANCBNlNF2SoipZFSNlz5hmKnejg6fubGLFu7Ph2URDj22dWGYjlRqDILQz7kHxARBlAwdC4CpTKHGC5D',
        #         'schedule': '',
        #     }

        #     baseurl = f'https://sms.hollatags.com/api/send/?user={config.hollatag_username}&pass={config.hollatag_password}&to={to}&from={sender}&msg={urllib.parse.quote(message)}'
        #     response = requests.get(baseurl, verify=False)

        for real in num:

            if len(real) == 11:
                if real.startswith('0'):
                    sender = list(real)
                    sender[0] = "234"
                    sender = ''.join(sender)

                    numberlist.append(sender)

                    unit += 1
                else:
                    invalid += 1

            elif len(real) == 13:
                if real.startswith('234'):
                    numberlist.append(real)

                    unit += 1

                else:
                    invalid += 1
            else:
                invalid += 1

        numberset = ','.join(numberlist)
        object.total = len(numberlist)
        if len(object.message) % 160 > 1:
            page = page + len(object.message) // 160

        if object.DND == True:
            if numberset == "" or numberset == None:
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'No valid Number found'])
                return self.form_invalid(form)

            elif Disable_Service.objects.get(service="Bulk sms").disable == True:
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'This Service is not currently available please check back'])
                return self.form_invalid(form)

            else:

                if float(object.total * 3.0 * page) > object.user.Account_Balance:
                    form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                        [u'You can\'t send bulk sms  due to insufficientr balance, Current Balance #{}'.format(object.user.Account_Balance)])
                    return self.form_invalid(form)

                else:
                    response = sendmessage(
                        object.sendername, object.message, numberset, "03")
                    object.unit = unit
                    object.invalid = invalid
                    object.page = page
                    object.total = len(numberlist)
                    object.amount = object.total * 3.0 * int(object.page)
                    mb = CustomUser.objects.get(pk=object.user.pk)
                    withdraw = mb.withdraw(mb.id, float(object.amount))
                    if withdraw == False:
                        form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                            [u'You can\'t send bulk sms  due to insufficientr balance, Current Balance #{}'.format(object.user.Account_Balance)])
                        return self.form_invalid(form)
                    object.Status = 'successful'
                    Wallet_summary.objects.create(user=user, product="bulk sms service charge  N{} ".format(
                        object.amount), amount=object.amount, previous_balance=previous_bal, after_balance=(previous_bal - float(object.amount)))

        else:
            if numberset == "" or numberset == None:
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'No valid Number found'])
                return self.form_invalid(form)

            elif Disable_Service.objects.get(service="Bulk sms").disable == True:
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'This Service is not currently available please check back'])
                return self.form_invalid(form)
            else:

                if float(object.total * 3.0 * page) > object.user.Account_Balance:
                    form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                        [u'You can\'t send bulk sms  due to insufficientr balance, Current Balance #{}'.format(object.user.Account_Balance)])
                    return self.form_invalid(form)

                else:
                    response = sendmessage(
                        object.sendername, object.message, numberset, "02")
                    object.unit = unit
                    object.invalid = invalid
                    object.page = page
                    object.total = len(numberlist)
                    object.amount = object.total * 3.0 * int(object.page)
                    mb = CustomUser.objects.get(pk=object.user.pk)
                    withdraw = mb.withdraw(mb.id, float(object.amount))
                    if withdraw == False:
                        form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                            [u'You can\'t send bulk sms  due to insufficientr balance, Current Balance #{}'.format(object.user.Account_Balance)])
                        return self.form_invalid(form)
                    object.Status = 'successful'
                    Wallet_summary.objects.create(user=object.user, product="bulk sms N{} ".format(
                        object.amount), amount=object.amount, previous_balance=previous_bal, after_balance=(previous_bal - float(object.amount)))

        form.save()

        return super(BulkCreate, self).form_valid(form)


class Bulk_success(generic.DetailView):
    model = Bulk_Message
    template_name = 'bulk_success.html'
    queryset = Bulk_Message.objects.all()
    context_object_name = 'bulk_success'


class airtime_success(generic.DetailView):
    model = Airtime
    template_name = 'Airtime_suc.html'
    queryset = Airtime.objects.all()
    context_object_name = 'Airtime_success'

    def get_context_data(self, **kwargs):

        context = super(airtime_success, self).get_context_data(**kwargs)
        context['net'] = Network.objects.get(name='MTN')
        context['net_2'] = Network.objects.get(name='GLO')
        context['net_3'] = Network.objects.get(name='9MOBILE')
        context['net_4'] = Network.objects.get(name='AIRTEL')
        return context


class Airtime_fundingCreate(generic.CreateView):
    form_class = Airtime_fundingform
    template_name = 'Airtime_funding_form.html'

    def get_context_data(self, **kwargs):

        context = super(Airtime_fundingCreate, self).get_context_data(**kwargs)
        context['mtn'] = Percentage.objects.get(
            network=Network.objects.get(name='MTN')).percent
        context['glo'] = Percentage.objects.get(
            network=Network.objects.get(name='GLO')).percent
        context['mobie'] = Percentage.objects.get(
            network=Network.objects.get(name='9MOBILE')).percent
        context['airtel'] = Percentage.objects.get(
            network=Network.objects.get(name='AIRTEL')).percent
        context['num_1'] = Admin_number.objects.get(network='MTN')
        context['num_2'] = Admin_number.objects.get(network='GLO')
        context['num_3'] = Admin_number.objects.get(network='9MOBILE')
        context['num_4'] = Admin_number.objects.get(network='AIRTEL')

        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user

        Mtn = ['0703', '0903', '0906', '0706', '0803',
               '0806', '0810', '0813', '0816', '0814']
        ETISALATE = ['0809', '0817', '0818', '0909', '0908']
        GLO = ['0705', '0805', '0811', '0807', '0815', '0905']
        AIRTEL = ['0708', '0802', '0808', '0812',
                  '0907', '0701', '0901', '0902']
        net = str(object.network)
        mobilenumber = str(object.mobile_number)
        num = mobilenumber.replace(" ", "")

        form.save()

        return super(Airtime_fundingCreate, self).form_valid(form)


class Airtime_funding_success(generic.DetailView):
    model = Airtime_funding
    template_name = 'Airtime_funding_success.html'
    queryset = Airtime_funding.objects.all()
    context_object_name = 'Airtime_funding_list'

    def get_context_data(self, **kwargs):

        context = super(Airtime_funding_success,
                        self).get_context_data(**kwargs)
        context['net'] = Network.objects.get(name='MTN')
        context['net_2'] = Network.objects.get(name='GLO')
        context['net_3'] = Network.objects.get(name='9MOBILE')
        context['net_4'] = Network.objects.get(name='AIRTEL')
        context['num_1'] = Admin_number.objects.get(network='MTN')
        context['num_2'] = Admin_number.objects.get(network='GLO')
        context['num_3'] = Admin_number.objects.get(network='9MOBILE')
        context['num_4'] = Admin_number.objects.get(network='AIRTEL')
        return context


class CouponCodePayment(generic.CreateView):
    form_class = CouponCodeform
    template_name = 'Coupon.html'
    Coupo = Couponcode.objects.all()

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        previous_bal = object.user.Account_Balance

        # for codes in self.Coupo:
        # exists()
        if not Couponcode.objects.filter(Coupon_Code=object.Code).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Invalid Coupon code note that its case sensetive'])
            return self.form_invalid(form)
        elif Couponcode.objects.filter(Coupon_Code=object.Code, Used=True).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'This Coupon code has been used'])
            return self.form_invalid(form)
        elif Couponcode.objects.filter(Coupon_Code=object.Code).exists():
            mb = CustomUser.objects.get(pk=object.user.pk)
            ms = Couponcode.objects.get(Coupon_Code=object.Code).amount
            object.amount = Couponcode.objects.get(
                Coupon_Code=object.Code).amount
            amount = float(object.amount)
            mb.deposit(mb.id, amount,False ,"Coupon Funding")
            sta = Couponcode.objects.get(Coupon_Code=object.Code)
            sta.Used = True
            Wallet_summary.objects.create(user=object.user, product=" N{} Coupon Funding  ".format(
                amount), amount=amount, previous_balance=previous_bal, after_balance=(previous_bal + amount))

            sta.save()
            messages.success(
                self.request, 'your account has been credited with sum of #{} .'.format(object.amount))

        form.save()
        return super(CouponCodePayment, self).form_valid(form)


class Coupon_success(generic.DetailView):
    model = CouponPayment
    template_name = 'Payment.html'
    context_object_name = 'Coupon'

    def get_queryset(self):
        return CouponPayment.objects.filter(user=self.request.user)


class PinView(generic.CreateView):
    form_class = Pinform
    template_name = 'pin.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        form.save()
        return super(PinView, self).form_valid(form)


class withdrawCreate(generic.CreateView):
    form_class = withdrawform
    template_name = 'withdraw_form.html'

    def sendmessage(sender,message,to,route):
                   payload={
                     'sender':sender,
                     'to': to,
                     'message': message,
                     'type': '0',
                     'routing':route,
                     'token':'EGZ1zr8wYJUajiAcxrOsCkMfv0EaTnGsHGHLePhZjlnsDQnOfD',
                     'schedule':'',
                          }

                   url = "https://app.smartsmssolutions.ng/io/api/client/v1/sms/"
                   response = requests.post(url, params=payload, verify=False)
    # def sendmessage(sender, message, to, route):
    #     payload = {
    #         'sender': sender,
    #         'to': to,
    #         'message': message,
    #         'type': '0',
    #         'routing': route,
    #         'token': 'cYTj0CCFuGM4PSrvABkoANCBNlNF2SoipZFSNlz5hmKnejg6fubGLFu7Ph2URDj22dWGYjlRqDILQz7kHxARBlAwdC4CpTKHGC5D',
    #         'schedule': '',
    #     }

    #     baseurl = f'https://sms.hollatags.com/api/send/?user={config.hollatag_username}&pass={config.hollatag_password}&to={to}&from={sender}&msg={urllib.parse.quote(message)}'
    #     response = requests.get(baseurl, verify=False)

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.amount = float(object.amount) + 100
        previous_bal = object.user.Account_Balance

        if float(object.amount) > object.user.Account_Balance:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Insufficient balance ,Try to fund your account :Account Balance #{}'.format(object.user.Account_Balance)])
            return self.form_invalid(form)

        elif float(object.amount) > object.user.Account_Balance:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Insufficient balance ,Try to fund your account :You can only withdraw #{}'.format(object.user.Account_Balance - 100)])
            return self.form_invalid(form)

        elif object.user.is_superuser == False and Withdraw.objects.filter(create_date__date=datetimex.date.today()).count > 1:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Exceed Maximum withdraw limit for today.'])

        elif float(object.amount) < 1000:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Minimun withdraw is #1000 per transaction'])
            return self.form_invalid(form)

        elif float(object.amount) > 20000:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u' Maximum withdraw is #20000 per transaction'])
            return self.form_invalid(form)
        else:
            try:
                mb = CustomUser.objects.get(pk=object.user.pk)
                ms = object.amount
                check = mb.withdraw(mb.id, float(ms))
                if check == False:
                    form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                        [u'Insufficient balance ,Try to fund your account :You can only withdraw #{}'.format(object.user.Account_Balance - 100)])
                    return self.form_invalid(form)

                Wallet_summary.objects.create(user=object.user, product="Wallet Withdraw ", amount=object.amount,
                                              previous_balance=previous_bal, after_balance=(previous_bal - object.amount))

                sendmessage('Msorg', "{0} want to withdraw   amount:{1}   https://www.Husmodata.com/page-not-found-error/page/vtuapp/withdraw/".format(
                    object.user.username, object.amount), '2348166171824', '2')
            except:
                pass

        form.save()

        return super(withdrawCreate, self).form_valid(form)


class Withdraw_success(generic.DetailView):
    model = Withdraw
    template_name = 'Withdraw-detail.html'
    context_object_name = 'Withdraw_list'

    def get_queryset(self):
        return Withdraw.objects.filter(user=self.request.user)


class dataCreate(generic.CreateView):
    form_class = dataform
    template_name = 'data_form.html'

    def get_context_data(self,**kwargs):

        context = super(dataCreate,self).get_context_data(**kwargs)
        context['network'] = Network.objects.get(name ='MTN')
        context['networks'] = Network.objects.all()
        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
            [u'use updated browser and retry'])
        return self.form_invalid(form)

        return super(dataCreate, self).form_valid(form)


def loadplans(request):

    network_id = request.GET.get('network')
    netid = Network.objects.get(id=network_id)
    plans = Plan.objects.filter(network_id=network_id).order_by('plan_amount')

    #print(plans)
    return render(request, 'planslist.html', {'plans': plans})


class Data_success(generic.DetailView):
    model = Data
    template_name = 'Data-detail.html'
    queryset = Data.objects.all()
    context_object_name = 'Data_list'


class Airtime_to_Data_Create(generic.CreateView):
    form_class = Airtime_to_Data_pin_form
    template_name = 'data_form_2.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        Mtn = ['0703', '0903', '0906', '0706', '0803',
               '0806', '0810', '0813', '0816', '0814']
        ETISALATE = ['0809', '0817', '0818', '0909', '0908']
        GLO = ['0705', '0805', '0811', '0807', '0815', '0905']
        AIRTEL = ['0708', '0802', '0808', '0812',
                  '0907', '0701', '0902', '0901', '0902']
        net = str(object.network)
        mobilenumber = str(object.mobile_number)
        num = mobilenumber.replace(" ", "")

        if object.Ported_number == True:
            if len(num) != 11:
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'Invalid mobile number'])
                return self.form_invalid(form)

        else:

            if len(num) != 11:
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'Invalid mobile number'])
                return self.form_invalid(form)

            elif net == '9MOBILE' and not num.startswith(tuple(ETISALATE)):
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'Please check entered number is not 9MOBILE user'])
                return self.form_invalid(form)

            elif net == 'MTN' and not num.startswith(tuple(Mtn)):
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'Please check entered number is not MTN user'])
                return self.form_invalid(form)

            elif net == 'GLO' and not num.startswith(tuple(GLO)):
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'Please check entered number is not GLO user'])
                return self.form_invalid(form)

            elif net == 'AIRTEL' and not num.startswith(tuple(AIRTEL)):
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'Please check entered number is not AIRTEL user'])
                return self.form_invalid(form)

            def sendmessage(sender,message,to,route):
                   payload={
                     'sender':sender,
                     'to': to,
                     'message': message,
                     'type': '0',
                     'routing':route,
                     'token':'EGZ1zr8wYJUajiAcxrOsCkMfv0EaTnGsHGHLePhZjlnsDQnOfD',
                     'schedule':'',
                          }

                   url = "https://app.smartsmssolutions.ng/io/api/client/v1/sms/"
                   response = requests.post(url, params=payload, verify=False)
            # def sendmessage(sender, message, to, route):
            #     payload = {
            #         'sender': sender,
            #         'to': to,
            #         'message': message,
            #         'type': '0',
            #         'routing': route,
            #         'token': 'cYTj0CCFuGM4PSrvABkoANCBNlNF2SoipZFSNlz5hmKnejg6fubGLFu7Ph2URDj22dWGYjlRqDILQz7kHxARBlAwdC4CpTKHGC5D',
            #         'schedule': '',
            #     }

            #     baseurl = f'https://sms.hollatags.com/api/send/?user={config.hollatag_username}&pass={config.hollatag_password}&to={to}&from={sender}&msg={urllib.parse.quote(message)}'
            #     response = requests.get(baseurl, verify=False)

            sendmessage("Msorg", "{0} want to buy  data plan  plan size:{1} network{2} https://www.Husmodata.com/page-not-found-error/page/vtuapp/data/".format(
                object.user.username, object.plan.plan_size, object.network), "2348166171824", "02")

        form.save()
        return super(Airtime_to_Data_Create, self).form_valid(form)


def loadplans_2(request):
    network_id = request.GET.get('network')
    plans = Airtime_to_data_Plan.objects.filter(
        network_id=network_id).order_by('plan_amount')
    return render(request, 'planslist_1.html', {'plans': plans})


class Airtime_to_Data__success(generic.DetailView):
    model = Data
    template_name = 'Airtime_to_Data_detail.html'
    queryset = Airtime_to_Data_pin.objects.all()
    context_object_name = 'Data_list'


class Airtime_to_Data_tranfer_Create(generic.CreateView):
    form_class = Airtime_to_Data_tranfer_form
    template_name = 'data_form_3.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        Mtn = ['0703', '0903', '0906', '0706', '0803',
               '0806', '0810', '0813', '0816', '0814']

        net = str(object.network)
        mobilenumber = str(object.Transfer_number)
        num = mobilenumber.replace(" ", "")

        if len(num) != 11:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Invalid mobile number'])
            return self.form_invalid(form)

        elif not num.startswith(tuple(Mtn)):
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Please check entered Tranfer from number is not MTN user'])
            return self.form_invalid(form)

        def sendmessage(sender,message,to,route):
                   payload={
                     'sender':sender,
                     'to': to,
                     'message': message,
                     'type': '0',
                     'routing':route,
                     'token':'EGZ1zr8wYJUajiAcxrOsCkMfv0EaTnGsHGHLePhZjlnsDQnOfD',
                     'schedule':'',
                          }

                   url = "https://app.smartsmssolutions.ng/io/api/client/v1/sms/"
                   response = requests.post(url, params=payload, verify=False)
        # def sendmessage(sender, message, to, route):
        #     payload = {
        #         'sender': sender,
        #         'to': to,
        #         'message': message,
        #         'type': '0',
        #         'routing': route,
        #         'token': 'cYTj0CCFuGM4PSrvABkoANCBNlNF2SoipZFSNlz5hmKnejg6fubGLFu7Ph2URDj22dWGYjlRqDILQz7kHxARBlAwdC4CpTKHGC5D',
        #         'schedule': '',
        #     }

        #     baseurl = f'https://sms.hollatags.com/api/send/?user={config.hollatag_username}&pass={config.hollatag_password}&to={to}&from={sender}&msg={urllib.parse.quote(message)}'
        #     response = requests.get(baseurl, verify=False)

        sendmessage("Msorg", "{0} want to buy  data plan  plan size:{1} network{2} https://www.Husmodata.com/page-not-found-error/page/vtuapp/data/".format(
            object.user.username, object.plan.plan_size, object.network), "2348166171824", "02")

        form.save()
        return super(Airtime_to_Data_tranfer_Create, self).form_valid(form)


class Airtime_to_Data_tranfer_success(generic.DetailView):
    model = Data
    template_name = 'Airtime_to_Data_tranfer_detail.html'
    queryset = Airtime_to_Data_tranfer.objects.all()
    context_object_name = 'Data_list'

    def get_context_data(self, **kwargs):

        context = super(Airtime_to_Data_tranfer_success,
                        self).get_context_data(**kwargs)
        context['net_1'] = Admin_number.objects.get(network='MTN')
        return context


class TransferCreate(generic.CreateView):
    form_class = Transferform
    template_name = 'Transfer_form.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user

        if float(object.amount) > object.user.Account_Balance:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'You can\'t Tranfer to other due to insufficientr balance, Current Balance #{}'.format(object.user.Account_Balance)])
            return self.form_invalid(form)

        elif not CustomUser.objects.filter(username__iexact=object.receiver_username).exists():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Invalid user or no user with that username.'])
            return self.form_invalid(form)

        elif  object.user.is_superuser == False and Transfer.objects.filter(create_date__date=datetimex.date.today()).count > 2:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Exceed Maximum tranfer limit for today.'])

        elif object.user.username.lower() == object.receiver_username.lower():
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'You cannot transfer to yourself.'])
            return self.form_invalid(form)

        else:
            mb = CustomUser.objects.get(pk=object.user.pk)
            mb_2 = CustomUser.objects.get(
                username__iexact=object.receiver_username)
            ms = object.amount
            previous_bal1 = mb.Account_Balance
            previous_bal2 = mb_2.Account_Balance
            check = mb.withdraw(mb.id,float(ms))
            if check == False:
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'You can\'t Tranfer to other due to insufficientr balance, Current Balance #{}'.format(object.user.Account_Balance)])
                return self.form_invalid(form)

            mb_2.deposit(mb_2.id, float(ms),True ,"Wallet to Wallet Transfer")
            notify.send(mb_2, recipient=mb_2, verb='You Received sum of #{} from {} '.format(
                object.amount, object.user))

            Wallet_summary.objects.create(user=mb, product="Transfer N{} to {}".format(
                object.amount, mb_2.username), amount=object.amount, previous_balance=previous_bal1, after_balance=(previous_bal1 - float(object.amount)))

            Wallet_summary.objects.create(user=mb_2, product="Received sum N{} from {}".format(
                object.amount, mb.username), amount=object.amount, previous_balance=previous_bal2, after_balance=(previous_bal2 + float(object.amount)))

            messages.success(self.request, 'Transfer sum of #{} to {} was successful'.format(
                object.amount, object.receiver_username))

        form.save()
        return super(TransferCreate, self).form_valid(form)


class BuybtcCreate(generic.CreateView):
    form_class = Buybtcform
    template_name = 'buybitcoin_form.html'

    def get_context_data(self, **kwargs):

        context = super(BuybtcCreate, self).get_context_data(**kwargs)
        context['buyrate'] = Btc_rate.objects.get(rate="Selling_rate").amount

        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user

        response = requests.get(
            "https://api.coindesk.com/v1/bpi/currentprice/usd.json")
        data = json.loads(response.text)
        amt = data["bpi"]["USD"]["rate_float"]
        rate = Btc_rate.objects.get(rate="Buying_rate").amount
        object.Btc = round((object.amount / (amt * rate)), 5)
        btc_amount = round((object.Btc * amt * rate), 2)

        if float(object.amount) > object.user.Account_Balance:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u' insufficientr balance, Current Balance #{}'.format(object.user.Account_Balance)])
            return self.form_invalid(form)

        def sendmessage(sender,message,to,route):
                   payload={
                     'sender':sender,
                     'to': to,
                     'message': message,
                     'type': '0',
                     'routing':route,
                     'token':'EGZ1zr8wYJUajiAcxrOsCkMfv0EaTnGsHGHLePhZjlnsDQnOfD',
                     'schedule':'',
                          }

                   url = "https://app.smartsmssolutions.ng/io/api/client/v1/sms/"
                   response = requests.post(url, params=payload, verify=False)
        # def sendmessage(sender, message, to, route):
        #     payload = {
        #         'sender': sender,
        #         'to': to,
        #         'message': message,
        #         'type': '0',
        #         'routing': route,
        #         'token': 'cYTj0CCFuGM4PSrvABkoANCBNlNF2SoipZFSNlz5hmKnejg6fubGLFu7Ph2URDj22dWGYjlRqDILQz7kHxARBlAwdC4CpTKHGC5D',
        #         'schedule': '',
        #     }

        #     baseurl = f'https://sms.hollatags.com/api/send/?user={config.hollatag_username}&pass={config.hollatag_password}&to={to}&from={sender}&msg={urllib.parse.quote(message)}'
        #     response = requests.get(baseurl, verify=False)

        sendmessage('Msorg', "{0} want to do buy bitcoin wallet address {1} amount {2}".format(
            object.user.username, object.Btc_address, object.amount), "2348166171824", "02")
        mb = CustomUser.objects.get(pk=object.user.pk)
        check = mb.withdraw(mb.id, object.amount)
        if check == False:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u' insufficientr balance, Current Balance #{}'.format(object.user.Account_Balance)])
            return self.form_invalid(form)

        form.save()
        return super(BuybtcCreate, self).form_valid(form)


class Buybtc_success(generic.DetailView):
    model = Buybtc
    template_name = 'Buybtc_success.html'
    queryset = Buybtc.objects.all()
    context_object_name = 'buybtc_list'


class SellbtcCreate(generic.CreateView):
    form_class = SellBtcform
    template_name = 'sellbitcoin_form.html'

    def get_context_data(self, **kwargs):

        context = super(SellbtcCreate, self).get_context_data(**kwargs)
        context['sellrate'] = Btc_rate.objects.get(rate="Buying_rate").amount

        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user

        response = requests.get(
            "https://api.coindesk.com/v1/bpi/currentprice/usd.json")
        data = json.loads(response.text)
        amt = data["bpi"]["USD"]["rate_float"]
        rate = Btc_rate.objects.get(rate="Selling_rate").amount
        object.Btc = round(object.Btc, 5)
        object.amount = round((object.Btc * float(amt) * rate), 2)

        def sendmessage(sender,message,to,route):
                   payload={
                     'sender':sender,
                     'to': to,
                     'message': message,
                     'type': '0',
                     'routing':route,
                     'token':'EGZ1zr8wYJUajiAcxrOsCkMfv0EaTnGsHGHLePhZjlnsDQnOfD',
                     'schedule':'',
                          }

                   url = "https://app.smartsmssolutions.ng/io/api/client/v1/sms/"
                   response = requests.post(url, params=payload, verify=False)
        # def sendmessage(sender, message, to, route):
        #     payload = {
        #         'sender': sender,
        #         'to': to,
        #         'message': message,
        #         'type': '0',
        #         'routing': route,
        #         'token': 'cYTj0CCFuGM4PSrvABkoANCBNlNF2SoipZFSNlz5hmKnejg6fubGLFu7Ph2URDj22dWGYjlRqDILQz7kHxARBlAwdC4CpTKHGC5D',
        #         'schedule': '',
        #     }

        #     baseurl = 'https://smartsmssolutions.com/api/json.php?'
        #     response = requests.post(baseurl, params=payload, verify=False)
        sendmessage('Msorg', "{0} want to do sell amount {1}".format(
            object.user.username, object.amount), "2348166171824", "02")

        form.save()
        return super(SellbtcCreate, self).form_valid(form)


class Sellbtc_success(generic.DetailView):
    model = SellBtc
    template_name = 'SellBtc_success.html'
    queryset = SellBtc.objects.all()
    context_object_name = 'sellbtc_list'

    def get_context_data(self, **kwargs):

        context = super(Sellbtc_success, self).get_context_data(**kwargs)
        context['adminwallet'] = Btc_rate.objects.get(
            rate="Selling_rate").btc_wallet_address

        return context


class Transfer_success(generic.DetailView):
    model = Transfer
    template_name = 'Transfer.html'
    queryset = Transfer.objects.all()
    context_object_name = 'Transfer_list'


class Notify_User(generic.CreateView):
    form_class = Notify_user_form
    template_name = 'Notify_user_form.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user

        if CustomUser.objects.filter(username=object.username).exists():
            mb = CustomUser.objects.get(pk=object.user.pk)
            mb_2 = CustomUser.objects.get(username=object.username)
            notify.send(mb_2, recipient=mb_2,
                        verb='{} from admin'.format(object.message))
            messages.success(
                self.request, 'Message sent successful to {}'.format(object.username))

        elif (object.username).lower() == 'all':
            #user_number = [musa.Phone  for musa in CustomUser.objects.all()]
            for name in CustomUser.objects.all():
                mb = CustomUser.objects.get(pk=object.user.pk)
                mb_2 = CustomUser.objects.get(username=name.username)
                notify.send(mb, recipient=mb_2,
                            verb='{} from admin'.format(object.message))
                #emails = [x.email for x in CustomUser.objects.all()]
                try:
                    sendmail(" New Notification from Husmodata.com",
                             f"{object.message} ", name.email, name.username)
                except:
                    pass

            messages.success(self.request, 'Message sent successful ')

        else:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'Invalid user or no user with that username.'])
            return self.form_invalid(form)

        form.save()
        return super(Notify_User, self).form_valid(form)


class AirtimeTopupCreate(generic.CreateView):
    form_class = AirtimeTopupform
    template_name = 'AirtimeTopup_form.html'

    def get_context_data(self, **kwargs):

        context = super(AirtimeTopupCreate, self).get_context_data(**kwargs)

        if self.request.user.user_type == "Affilliate":
            context['mtn'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="MTN")).Affilliate_percent)/100
            context['glo'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="GLO")).Affilliate_percent)/100
            context['airtel'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="AIRTEL")).Affilliate_percent)/100
            context['mobile'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="9MOBILE")).Affilliate_percent)/100

            context['mtn_s'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="MTN")).share_n_sell_affilliate_percent)/100
            context['glo_s'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="GLO")).share_n_sell_affilliate_percent)/100
            context['airtel_s'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="AIRTEL")).share_n_sell_affilliate_percent)/100
            context['mobile_s'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="9MOBILE")).share_n_sell_affilliate_percent)/100

        elif self.request.user.user_type == "API":
            context['mtn'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="MTN")).api_percent)/100
            context['glo'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="GLO")).api_percent)/100
            context['airtel'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="AIRTEL")).api_percent)/100
            context['mobile'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="9MOBILE")).api_percent)/100

            context['mtn_s'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="MTN")).share_n_sell_api_percent)/100
            context['glo_s'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="GLO")).share_n_sell_api_percent)/100
            context['airtel_s'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="AIRTEL")).share_n_sell_api_percent)/100
            context['mobile_s'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="9MOBILE")).share_n_sell_api_percent)/100

        elif self.request.user.user_type == "TopUser":
            context['mtn'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="MTN")).Affilliate_percent)/100
            context['glo'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="GLO")).Affilliate_percent)/100
            context['airtel'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="AIRTEL")).Affilliate_percent)/100
            context['mobile'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="9MOBILE")).Affilliate_percent)/100

            context['mtn_s'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="MTN")).share_n_sell_topuser_percent)/100
            context['glo_s'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="GLO")).share_n_sell_topuser_percent)/100
            context['airtel_s'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="AIRTEL")).share_n_sell_topuser_percent)/100
            context['mobile_s'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="9MOBILE")).share_n_sell_topuser_percent)/100

        else:
            context['mtn'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="MTN")).percent)/100
            context['glo'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="GLO")).percent)/100
            context['airtel'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="AIRTEL")).percent)/100
            context['mobile'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="9MOBILE")).percent)/100

            context['mtn_s'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="MTN")).share_n_sell_percent)/100
            context['glo_s'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="GLO")).share_n_sell_percent)/100
            context['airtel_s'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="AIRTEL")).share_n_sell_percent)/100
            context['mobile_s'] = (TopupPercentage.objects.get(
                network=Network.objects.get(name="9MOBILE")).share_n_sell_percent)/100

        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
            [u'use updated browser and retry'])
        return self.form_invalid(form)

        return super(AirtimeTopupCreate, self).form_valid(form)


class AirtimeTopup_success(generic.DetailView):
    model = AirtimeTopup
    template_name = 'AirtimeTopup.html'
    queryset = AirtimeTopup.objects.all()
    context_object_name = 'AirtimeTopup_list'


class AirtimeswapCreate(generic.CreateView):
    form_class = Airtimeswapform
    template_name = 'Airtimeswap_form.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        Mtn = ['0703', '0903', '0906', '0706', '0803',
               '0806', '0810', '0813', '0816', '0814']
        ETISALATE = ['0809', '0817', '0818', '0909', '0908']
        GLO = ['0705', '0805', '0811', '0807', '0815', '0905']
        AIRTEL = ['0708', '0802', '0808', '0812',
                  '0907', '0701', '0901', '0902']
        net = str(object.swap_to_network)
        net1 = str(object.swap_from_network)
        mobilenumber = str(object.mobile_number)
        num = mobilenumber.replace(" ", "")

        if object.Ported_number == True:

            if len(num) != 11:
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'Invalid mobile number'])
                return self.form_invalid(form)

            elif object.swap_from_network == object.swap_to_network:
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'You cannot swap to same network'])
                return self.form_invalid(form)

        else:

            if len(num) != 11:
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'Invalid mobile number'])
                return self.form_invalid(form)

            elif object.swap_from_network == object.swap_to_network:
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'You cannot swap to same network'])
                return self.form_invalid(form)

            elif net == '9MOBILE' and not num.startswith(tuple(ETISALATE)):
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'Please check entered number is not 9MOBILE user'])
                return self.form_invalid(form)

            elif net == 'MTN' and not num.startswith(tuple(Mtn)):
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'Please check entered number is not MTN user'])
                return self.form_invalid(form)

            elif net == 'GLO' and not num.startswith(tuple(GLO)):
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'Please check entered number is not GLO user'])
                return self.form_invalid(form)

            elif net == 'AIRTEL' and not num.startswith(tuple(AIRTEL)):
                form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                    [u'Please check entered number is not AIRTEL user'])
                return self.form_invalid(form)

            elif net == 'MTN':
                object.Receivece_amount = float(object.amount) * 0.9

            elif net == 'GLO':
                object.Receivece_amount = float(object.amount) * 0.8

            elif net == '9MOBILE':
                object.Receivece_amount = float(object.amount) * 0.85

            elif net == 'AIRTEL':
                object.Receivece_amount = float(object.amount) * 0.85

        form.save()
        return super(AirtimeswapCreate, self).form_valid(form)


class Airtimeswap_success(generic.DetailView):
    model = Airtimeswap
    template_name = 'Airtimeswap.html'
    queryset = Airtimeswap.objects.all()
    context_object_name = 'Airtimeswap_list'

    def get_context_data(self, **kwargs):

        context = super(Airtimeswap_success, self).get_context_data(**kwargs)
        context['net'] = Network.objects.get(name='MTN')
        context['net_2'] = Network.objects.get(name='GLO')
        context['net_3'] = Network.objects.get(name='9MOBILE')
        context['plan_4'] = Network.objects.get(name='AIRTEL')
        context['num_1'] = Admin_number.objects.get(network='MTN')
        context['num_2'] = Admin_number.objects.get(network='GLO')
        context['num_3'] = Admin_number.objects.get(network='9MOBILE')
        context['num_4'] = Admin_number.objects.get(network='AIRTEL')
        return context

def validate_meter_number(request):

    meternumber = request.GET.get('meternumber', None)
    disconame = request.GET.get('disconame', None)
    mtype = request.GET.get('mtype', None)


    invalid = False
    name = "NO NAME RETURN"
    #print("hello")
    #print(disconame)

    url = "https://www.api.ringo.ng/api/agent/p2"
    payload = {
        "serviceCode" : "V-ELECT",
        "disco" :Disco_provider_name.objects.get(name = str(disconame)).p_id,
        "meterNo": meternumber,
        "type" : mtype
    }

    #print(payload)

    headers = {'email': 'usmanreal43@gmail.com','password': 'Hafsayn20','Content-Type': 'application/json'  }

    response = requests.post(url, headers=headers, data = json.dumps(payload))
    #print(response.text)
    a = json.loads(response.text)

    status  = a["status"]

    if status == '200':
             name = a["customerName"]
             invalid = False

    else:
         name  = "NO NAME RETURN"
         invalid = True



    data = {
        'invalid': invalid,
        'name': name
    }
    return JsonResponse(data)

def validate_iuc(request):

    iuc = request.GET.get('smart_card_number', None)
    cable_id = request.GET.get('cablename', None)
    if cable_id == "STARTIME":
        cable_id = "STARTIMES"

    url = "https://www.api.ringo.ng/api/agent/p2"
    payload = {
        "serviceCode" : "V-TV",
        "type" : cable_id,
        "smartCardNo" : iuc
    }

    #print(payload)

    headers = { 'email': 'usmanreal43@gmail.com','password': 'Hafsayn20','Content-Type': 'application/json' }

    response = requests.post(url, headers=headers, data = json.dumps(payload))
    #print(response.text)
    a = json.loads(response.text)



    if response.status_code == 200:
             name = a["customerName"]
             invalid = False

    else:
         name  = "INVALID_SMARTCARDNO"
         invalid = True


    data = {
        'invalid': invalid,
        'name': name
    }

    return JsonResponse(data)
###################################################################
# def validate_meter_number(request):
#     meternumber = request.GET.get('meternumber', None)
#     disconame = request.GET.get('disconame', None)
#     mtype = request.GET.get('mtype', None)

#     #print(meternumber, disconame, mtype)
#     if disconame == "Ikeja Electric":
#         disconame = "ikeja-electric"

#     elif disconame == 'Eko Electric':
#         disconame = "eko-electric"

#     elif disconame == "Kaduna Electric":
#         disconame = "kaduna-electric"

#     elif disconame == "Port Harcourt Electric":
#         disconame = "portharcourt-electric"

#     elif disconame == "Jos Electric":
#         disconame = "jos-electric"

#     elif disconame == "Ibadan Electric":
#         disconame = "ibadan-electric"

#     elif disconame == "Kano Electric":
#         disconame = "kano-electric"

#     elif disconame == "Abuja Electric":
#         disconame = "abuja-electric"

#     data = {"billersCode": meternumber, "serviceID": disconame, "type": mtype}
#     invalid = False
#     authentication = (f'{config.vtpass_email}', f'{config.vtpass_password}')

#     resp = requests.post(
#         "https://vtpass.com/api/merchant-verify", data=data, auth=authentication)
#     #print(resp.text)
#     res = json.loads(resp.text)
#     dat = res['content']
#     if 'Customer_Name' in dat:
#         name = res['content']['Customer_Name']
#         address = res['content']["Address"]
#     else:
#         invalid = True
#         name = "INVALID METER NUMBER"
#         address = "INVALID METER NUMBER"

#     data = {
#         'invalid': invalid,
#         'name': name,
#         'address': address
#     }

#     return JsonResponse(data)


# def validate_iuc(request):
#     iuc = request.GET.get('smart_card_number', None)
#     cable_id = request.GET.get('cablename', None)
#     if cable_id == "DSTV":
#         data = {"billersCode": iuc, "serviceID": "dstv"}

#     elif cable_id == 'GOTV':
#         data = {"billersCode": iuc, "serviceID": "gotv"}

#     elif cable_id == "STARTIME":
#         data = {"billersCode": iuc, "serviceID": "startimes"}

#     invalid = False
#     authentication = (f'{config.vtpass_email}', f'{config.vtpass_password}')

#     resp = requests.post(
#         "https://vtpass.com/api/merchant-verify", data=data, auth=authentication)
#     #print(resp.text)
#     res = json.loads(resp.text)
#     dat = res['content']
#     if 'Customer_Name' in dat:
#         name = res['content']['Customer_Name']

#     else:
#         invalid = True
#         name = "INVALID IUC/SMARTCARD"

#     data = {
#         'invalid': invalid,
#         'name': name

#     }
#     return JsonResponse(data)


class Cablesubscription(generic.CreateView):
    form_class = cableform
    template_name = 'cable_form.html'

    def get_context_data(self, **kwargs):
        context = super(Cablesubscription, self).get_context_data(**kwargs)
        service = ServicesCharge.objects.get(service="Cablesub")
        if self.request.user.user_type == "Affilliate":
            if service.Affilliate_charge > 0.0:
                context['charge'] = f"N{service.Affilliate_charge } Charge "

            elif service.Affilliate_discount > 0.0:
                context['charge'] = f"{service.Affilliate_discount} Percent Discount "

        elif self.request.user.user_type == "TopUser":
            if service.topuser_charge > 0.0:
                context['charge'] = f"N{service.topuser_charge } Charge "

            elif service.topuser_discount > 0.0:
                context['charge'] = f"{service.topuser_discount} Percent Discount "

        elif self.request.user.user_type == "API":
            if service.api_charge > 0.0:
                context['charge'] = f"N{service.api_charge } Charge "

            elif service.api_discount > 0.0:
                context['charge'] = f"{service.api_discount} Percent Discount "

        else:
            if service.charge > 0.0:
                context['charge'] = f"N{service.charge } Charge "

            elif service.discount > 0.0:
                context['charge'] = f"{service.discount} Percent Discount "

        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
            [u'use updated browser and retry'])
        return self.form_invalid(form)

        return super(Cablesubscription, self).form_valid(form)


class BillpaymentView(generic.CreateView):
    form_class = Billpaymentform
    template_name = 'bill_form.html'

    def get_context_data(self, **kwargs):
        context = super(BillpaymentView, self).get_context_data(**kwargs)
        service = ServicesCharge.objects.get(service="Bill")

        if self.request.user.user_type == "Affilliate":
            if service.Affilliate_charge > 0.0:
                context['charge'] = f"N{service.Affilliate_charge } Charge "

            elif service.Affilliate_discount > 0.0:
                context['charge'] = f"{service.Affilliate_discount} Percent Discount "

        elif self.request.user.user_type == "TopUser":
            if service.topuser_charge > 0.0:
                context['charge'] = f"N{service.topuser_charge } Charge "

            elif service.topuser_discount > 0.0:
                context['charge'] = f"{service.topuser_discount} Percent Discount "

        elif self.request.user.user_type == "API":
            if service.api_charge > 0.0:
                context['charge'] = f"N{service.api_charge } Charge "

            elif service.api_discount > 0.0:
                context['charge'] = f"{service.api_discount} Percent Discount "

        else:
            if service.charge > 0.0:
                context['charge'] = f"N{service.charge } Charge "

            elif service.discount > 0.0:
                context['charge'] = f"{service.discount} Percent Discount "

        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
            [u'use updated browser and retry'])
        return self.form_invalid(form)

        return super(BillpaymentView, self).form_valid(form)


def loadcableplans(request):
    cablename_id = request.GET.get('cablename')
    cableplans = CablePlan.objects.filter(
        cablename_id=cablename_id).order_by('plan_amount')
    return render(request, 'cableplanslist.html', {'cableplans': cableplans})


class Cablesub_success(generic.DetailView):
    model = Cablesub
    template_name = 'cablesuccess.html'
    context_object_name = 'cable_list'

    def get_queryset(self):
        return Cablesub.objects.filter(user=self.request.user)


class BillPayment_success(generic.DetailView):
    model = Billpayment
    template_name = 'billsuccess.html'
    context_object_name = 'bill_list'

    def get_queryset(self):
        return Billpayment.objects.filter(user=self.request.user)


class BookList(generic.ListView):
    template_name = 'book-list.html'
    paginate_by = 20
    queryset = Book.objects.all().order_by('-created_at')
    context_object_name = 'book_list'
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookList, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()

        return context


class BookDetail(FormMixin, generic.DetailView):
    model = Book
    template_name = 'Book_detail.html'
    context_object_name = 'book'
    form_class = Book_order_Form

    def get_success_url(self):
        return reverse('book_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(BookDetail, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['form'] = Book_order_Form(initial={'book_name': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.price = self.object.price
        object.book_name = self.object

        if float(object.price) > object.user.Account_Balance:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u'You can\'t purchase this book due to insufficientr balance, Current Balance #{}'.format(object.user.Account_Balance)])
            messages.error(self.request, 'You can\'t purchase this book due to insufficientr balance, Current Balance #{}'.format(
                object.user.Account_Balance))
            return self.form_invalid(form)
        mb = CustomUser.objects.get(pk=object.user.pk)
        ms = object.price
        check = mb.withdraw(mb.id, float(ms))
        if check == False:
            form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
                [u' insufficientr balance, Current Balance #{}'.format(object.user.Account_Balance)])
            return self.form_invalid(form)
        messages.success(
            self.request, 'Your order has been sent you receive download link on email you provided')

        def sendmessage(sender,message,to,route):
                   payload={
                     'sender':sender,
                     'to': to,
                     'message': message,
                     'type': '0',
                     'routing':route,
                     'token':'EGZ1zr8wYJUajiAcxrOsCkMfv0EaTnGsHGHLePhZjlnsDQnOfD',
                     'schedule':'',
                          }

                   url = "https://app.smartsmssolutions.ng/io/api/client/v1/sms/"
                   response = requests.post(url, params=payload, verify=False)
        # def sendmessage(sender, message, to, route):
        #     payload = {
        #         'sender': sender,
        #         'to': to,
        #         'message': message,
        #         'type': '0',
        #         'routing': route,
        #         'token': 'cYTj0CCFuGM4PSrvABkoANCBNlNF2SoipZFSNlz5hmKnejg6fubGLFu7Ph2URDj22dWGYjlRqDILQz7kHxARBlAwdC4CpTKHGC5D',
        #         'schedule': '',
        #     }

        #     baseurl = f'https://sms.hollatags.com/api/send/?user={config.hollatag_username}&pass={config.hollatag_password}&to={to}&from={sender}&msg={urllib.parse.quote(message)}'
        #     response = requests.get(baseurl, verify=False)

        sendmessage('Msorg', "{0} order {1} email address {2}".format(
            object.user.username, object.book_name, object.email), "2348166171824", "02")

        form.save()

        return super(BookDetail, self).form_valid(form)


def ravepaymentdone(request):

    ref = request.GET.get('txref')
    user = request.user.username

    headers = {
        'content-type': 'application/json',
    }

    data = {"txref": ref, "SECKEY": "FLWSECK-fd7f78dd615d0d7b2f87447f60979fba-X"}
    data = json.dumps(data)
    response = requests.post(
        'https://api.ravepay.com/flwv3-pug/getpaidx/api/v2/verify', headers=headers, data=data)

    data = json.loads(response.text)
    context = {'data': response.text}
    if data['data']['status'] == 'successful':

        if data['data']['chargecode'] == '00' or data['data']['chargecode'] == '0':
            amt = float(data['data']['amount'])
            payamount = amt / 100
            amt = (payamount * 0.02)
            paynow = round(payamount - amt)
            mb = CustomUser.objects.get(pk=request.user.pk)
            context = {'data': data}

            mb = CustomUser.objects.get(pk=request.user.pk)
            if not "reference" in request.session:
                mb.deposit(mb.id, paynow,False ,"Flutterwave Funding")
                notify.send(
                    mb, recipient=mb, verb='Flutterwave Payment successful you account has been credited with sum of #{}'.format(paynow))

                paymentgateway.objects.create(
                    user=request.user, reference=ref, amount=paynow, Status="successful")
                request.session["reference"] = ref
            else:
                refere = request.session["reference"]
                if ref == refere:
                    pass
                else:
                    mb.deposit(mb.id, paynow,False ,"Paystack Funding")
                    notify.send(
                        mb, recipient=mb, verb='Paystack Payment successful you account has been credited with sum of #{}'.format(paynow))

                    paymentgateway.objects.create(
                        user=request.user, reference=ref, amount=paynow, Status="successful")
                    request.session["reference"] = ref

    else:
        messages.error(request, 'Our payment gateway return Payment tansaction failed status {}'.format(
            data["data"]["status"]))

    return render(request, 'ravepaymentdone.html', context)


def paymentrave(request):
    if request.method == 'POST':
        form = paymentraveform(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            username = request.user.username
            email = request.user.email
            phone = request.user.Phone
            amount = ((amount * 100) + (0.02 * amount * 100))

            headers = {
                'Authorization': f'Bearer {config.Paystack_secret_key}',
                'Content-Type': 'application/json',
            }

            ab = {"amount": amount, "email": email}
            data = json.dumps(ab)
            response = requests.post(
                'https://api.paystack.co/transaction/initialize', headers=headers, data=data)
            #print(response.text)
            loaddata = json.loads(response.text)
            amt = loaddata["data"]["authorization_url"]

            #print(username, email, phone)

            return HttpResponseRedirect(amt)

    else:
        form = paymentraveform()

    return render(request, 'payonline.html', {'form': form})


@require_POST
@csrf_exempt
# @require_http_methods(["GET", "POST"])
def payonlinedone(request):
    a = f'{config.Paystack_secret_key}'
    secret = bytes(a, encoding="ascii")
    payload = request.body
    sign = hmac.new(secret, payload, hashlib.sha512).hexdigest()
    code = request.META.get('HTTP_X_PAYSTACK_SIGNATURE')

    bodydata = json.loads(payload)
    ref = bodydata['data']['reference']

    forwarded_for = u'{}'.format(request.META.get('HTTP_X_FORWARDED_FOR'))
    whitelist = ["52.31.139.75", "52.49.173.169", "52.214.14.220"]
    if forwarded_for in whitelist:
        if code == sign:
            url = "https://api.paystack.co/transaction/verify/{}".format(ref)
            response = requests.get(url, headers={
                                    'Authorization': f'Bearer {config.Paystack_secret_key}', "Content-Type": "application/json"})
            ab = json.loads(response.text)

            if (response.status_code == 200 and ab['status'] == True) and (ab["message"] == "Verification successful" and ab["data"]["status"] == "success"):
                user = ab['data']["customer"]['email']
                mb = CustomUser.objects.get(email__iexact=user)
                amount = (ab['data']['amount'])
                paynow = (round(amount/100 - 0.02 * amount/100))

                if not paymentgateway.objects.filter(reference=ref).exists():
                    try:
                        previous_bal = mb.Account_Balance
                        mb.deposit(mb.id, paynow + 1,False ,"Paystack Funding")
                        paymentgateway.objects.create(
                            user=mb, reference=ref, amount=paynow, Status="successful", gateway="monnify")
                        Wallet_summary.objects.create(user=mb, product=" N{} paystack Funding ".format(
                            paynow), amount=paynow, previous_balance=previous_bal, after_balance=(previous_bal + paynow))
                        notify.send(
                            mb, recipient=mb, verb='Paystack Payment successful you account has been credited with sum of #{}'.format(paynow))
                    except:
                        return HttpResponse(status=200)
                else:
                    pass

            else:
                messages.error(
                    request, 'Our payment gateway return Payment tansaction failed status {}'.format(ab["message"]))

    else:
        return HttpResponseForbidden('Permission denied.')
    #print("hello")
    return HttpResponse(status=200)


@csrf_exempt
# @require_http_methods(["GET", "POST"])
def ussdcallback(request):

    #print("ussd callback herer")
    #print(request.body)
    #print("ussd callback herer 2")

    return HttpResponse(status=200)


def create_id():
    num = random.randint(1, 10)
    num_2 = random.randint(1, 10)
    num_3 = random.randint(1, 10)
    return str(num_2)+str(num_3)+str(uuid.uuid4())


def flutterwavepayment(request):
    if request.method == 'POST':
        form = paymentraveform(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            username = request.user.username
            email = request.user.email
            phone = request.user.Phone
            amount = (amount) + (0.015 * amount)

            headers = {
                'content-type': 'application/json',

            }

            ab = {"txref": create_id(), "PBFPubKey": "FLWPUBK-7e02397bad16e051a49495ef37b4cc23-X", "customer_email": email,
                  "amount": amount, "currency": "NGN", "redirect_url": "https://www.Husmodata.com/web/profile/"}
            data = json.dumps(ab)
            #print(data)
            #data = '{"txref":"MC-1520443531487","PBFPubKey":"FLWPUBK-d029dfa2c4130538504aa1fb7e85a7cd-X", "customer_email": "user@example.com", "amount": 1000, "currency": "NGN", "redirect_url": "https://www.dataworld.com/ravepaymentdone"}'

            #response = requests.post('https://api.ravepay.co/flwv3-pug/getpaidx/api/v2/hosted/pay', headers=headers, data=data)

            response = requests.post(
                'https://api.ravepay.co/flwv3-pug/getpaidx/api/v2/hosted/pay', headers=headers, data=data)

            #print(response)

            loaddata = json.loads(response.text)
            amt = loaddata["data"]["link"]

            #print(username, email, phone)

            return HttpResponseRedirect(amt)

    else:
        form = paymentraveform()

    return render(request, 'ravepayment.html', {'form': form})


@require_POST
@csrf_exempt
# @require_http_methods(["GET", "POST"])
def flutterwavepaymentdone(request):
    #print(request.body)
    hash_code = request.META.get('HTTP_VERIF_HASH')
    #print(hash_code)
    #print(type(hash_code))

    if hash_code == 'MSORGHOOT$@#$$#%':
        #print("hurray")
        data = json.loads(request.body)
        #print(data["txRef"])
        #print(data["status"])
        #print(data["amount"])

        data = json.loads(request.body)
        headers = {
            'content-type': 'application/json',
        }

        ab = {"txref": data["txRef"],
              "SECKEY": "FLWSECK-ce1767f49ae239374339ff27e0cf2659-X"}
        data = json.dumps(ab)

        response = requests.post(
            'https://api.ravepay.co/flwv3-pug/getpaidx/api/v2/verify', headers=headers, data=data)
        #print(response.text)
        data = json.loads(response.text)

        #print(data["data"]["txref"])
        #print(data["data"]["status"])
        #print(data["data"]["amount"])
        #print(data["data"]["chargecode"])
        #print(data["data"]["chargemessage"])

        if (response.status_code == 200 and data["data"]["chargecode"] == "00" and data["data"]["status"] == "successful"):
            #print("processing")
            ab = json.loads(request.body)
            user = ab["customer"]['email']
            #print(user)
            mb = CustomUser.objects.get(email__iexact=user)
            amount = (data["data"]["amount"])
            paynow = (round(amount - (0.015 * amount)))

            if not paymentgateway.objects.filter(reference=data["data"]["txref"]).exists():
                mb.deposit(mb.id, paynow + 1,False ,"Flutterwave Funding")
                notify.send(
                    mb, recipient=mb, verb='flutterwave Payment successful you account has been credited with sum of #{}'.format(paynow))

                paymentgateway.objects.create(
                    user=mb, reference=data["data"]["txref"], amount=paynow, gateway="Flutterwave", Status="successful")

                #print("done")
            else:
                pass

        else:
            messages.error(
                request, 'Our payment gateway return Payment tansaction failed statuss')

    return HttpResponse(status=200)


# API VIEW START HERE CREATED BY MUSA ABDUL GANIYU


class UserCreate(APIView):
    """
    Creates the user.
    """

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=200)

        return Response(serializer.errors, status=400)


# API VIEW START HERE CREATED BY MUSA ABDUL GANIYU


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class ApiDoc(TemplateView):
    template_name = 'swagger-ui.html'

    def get_context_data(self, **kwargs):
        context = super(ApiDoc, self).get_context_data(**kwargs)
        context['plans'] = Plan.objects.all()
        context['network'] = Network.objects.all()
        context['cableplans'] = CablePlan.objects.all()
        context['cable'] = Cable.objects.all()
        context['disco'] = Disco_provider_name.objects.all()

        if Token.objects.filter(user=self.request.user).exists():
            context['token'] = Token.objects.get(user=self.request.user)
        else:
            Token.objects.create(user=self.request.user)
            context['token'] = Token.objects.get(user=self.request.user)

        return context


###API ####


class PasswordChangeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            serializer = PasswordChangeSerializer(data=request.data)
            if serializer.is_valid():
                if not request.user.check_password(serializer.data.get('old_password')):
                    return Response({'old_password': 'Wrong old password entered.'}, status=400)

                elif str(serializer.data.get('new_password1')) != str(serializer.data.get('new_password2')):
                    return Response({'new_password2': 'new Passwords are not match'}, status=400)

                elif len(serializer.data.get('new_password1')) < 8:
                    return Response({'new_password1': 'new password too short, minimum of 8 character.'}, status=400)

                # set_password also hashes the password that the user will get
                request.user.set_password(serializer.data.get('new_password1'))
                request.user.save()

            return Response({'status': 'New password has been saved.'}, status=200)

            # return Response(serializer.errors,status=400)

        except CustomUser.DoesNotExist:
            return Response(status=500)


class CustomUserCreate(APIView):

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=201)

        return Response(serializer.errors, status=400)


class Api_History(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None, **kwargs):
        data = Data.objects.filter(
            user=request.user).order_by('-create_date')[:10]
        data_serializer = DataSerializer(data, many=True)
        airtimetopup = AirtimeTopup.objects.filter(
            user=request.user).order_by('-create_date')[:10]
        airtimetopup_serializer = AirtimeTopupSerializer(
            airtimetopup, many=True)
        payment = paymentgateway.objects.filter(
            user=request.user).order_by('-created_on')[:10]
        payment_serializer = paymentgatewaySerializer(payment, many=True)
        cablesub = Cablesub.objects.filter(
            user=request.user).order_by('-create_date')[:10]
        cablesub_serializer = CablesubSerializer(cablesub, many=True)

        return Response({
            'data': data_serializer.data,
            'topup': airtimetopup_serializer.data,
            'paymentgateway': payment_serializer.data,
            'cablesub': cablesub_serializer.data,

        })


class UserListView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer



class UserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:

            def create_id():
                num = random.randint(1, 10)
                num_2 = random.randint(1, 10)
                num_3 = random.randint(1, 10)
                return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]

            body = {
                "accountReference": create_id(),
                "accountName": request.user.username,
                "currencyCode": "NGN",
                "contractCode": f"{config.monnify_contract_code}",
                "customerEmail": request.user.email,
                "incomeSplitConfig": [],
                "restrictPaymentSource": False,
                "allowedPaymentSources": {},
                "customerName": request.user.username,
                "getAllAvailableBanks": True,
            }

            if not request.user.accounts:

                data = json.dumps(body)
                ad = requests.post("https://api.monnify.com/api/v1/auth/login", auth=HTTPBasicAuth(f'{config.monnify_API_KEY}', f'{config.monnify_SECRET_KEY}'))
                mydata = json.loads(ad.text)
                headers = {'Content-Type': 'application/json',"Authorization": "Bearer {}" .format(mydata['responseBody']["accessToken"])}
                ab = requests.post("https://api.monnify.com/api/v2/bank-transfer/reserved-accounts",headers=headers, data=data)

                mydata = json.loads(ab.text)

                user = request.user
                user.reservedaccountNumber = mydata["responseBody"]["accounts"][0]["accountNumber"]
                user.reservedbankName = mydata["responseBody"]["accounts"][0]["bankName"]
                user.reservedaccountReference = mydata["responseBody"]["accountReference"]
                user.accounts = json.dumps({"accounts":mydata["responseBody"]["accounts"]})
                user.save()

            else:
                pass

        except:
            pass


        try:
                    if request.user.user_type == "Affilliate":
                                mtn = (TopupPercentage.objects.get(network=Network.objects.get(name="MTN")).Affilliate_percent)
                                glo = (TopupPercentage.objects.get(network=Network.objects.get(name="GLO")).Affilliate_percent)
                                airtel = (TopupPercentage.objects.get(network=Network.objects.get(name="AIRTEL")).Affilliate_percent)
                                mobile = (TopupPercentage.objects.get(network=Network.objects.get(name="9MOBILE")).Affilliate_percent)

                                mtn_s = (TopupPercentage.objects.get(network=Network.objects.get(name="MTN")).share_n_sell_affilliate_percent)
                                glo_s = (TopupPercentage.objects.get( network=Network.objects.get(name="GLO")).share_n_sell_affilliate_percent)
                                airtel_s = (TopupPercentage.objects.get(network=Network.objects.get(name="AIRTEL")).share_n_sell_affilliate_percent)
                                mobile_s = (TopupPercentage.objects.get(network=Network.objects.get(name="9MOBILE")).share_n_sell_affilliate_percent)



                    elif request.user.user_type == "TopUser":
                                mtn = (TopupPercentage.objects.get(network=Network.objects.get(name="MTN")).topuser_percent)
                                glo = (TopupPercentage.objects.get(network=Network.objects.get(name="GLO")).topuser_percent)
                                airtel = (TopupPercentage.objects.get(network=Network.objects.get(name="AIRTEL")).topuser_percent)
                                mobile = (TopupPercentage.objects.get(network=Network.objects.get(name="9MOBILE")).topuser_percent)

                                mtn_s = (TopupPercentage.objects.get(network=Network.objects.get(name="MTN")).share_n_sell_topuser_percent)
                                glo_s = (TopupPercentage.objects.get( network=Network.objects.get(name="GLO")).share_n_sell_topuser_percent)
                                airtel_s = (TopupPercentage.objects.get(network=Network.objects.get(name="AIRTEL")).share_n_sell_topuser_percent)
                                mobile_s = (TopupPercentage.objects.get(network=Network.objects.get(name="9MOBILE")).share_n_sell_topuser_percent)

                    else:
                                mtn = (TopupPercentage.objects.get(network=Network.objects.get(name="MTN")).percent)
                                glo = (TopupPercentage.objects.get(network=Network.objects.get(name="GLO")).percent)
                                airtel = (TopupPercentage.objects.get(network=Network.objects.get(name="AIRTEL")).percent)
                                mobile = (TopupPercentage.objects.get(network=Network.objects.get(name="9MOBILE")).percent)

                                mtn_s = (TopupPercentage.objects.get(network=Network.objects.get(name="MTN")).share_n_sell_percent)
                                glo_s = (TopupPercentage.objects.get( network=Network.objects.get(name="GLO")).share_n_sell_percent)
                                airtel_s = (TopupPercentage.objects.get(network=Network.objects.get(name="AIRTEL")).share_n_sell_percent)
                                mobile_s = (TopupPercentage.objects.get(network=Network.objects.get(name="9MOBILE")).share_n_sell_percent)

        except:
            pass



        try:

                    plan_item = Plan.objects.filter(network=Network.objects.get(name="MTN")).order_by('plan_amount')
                    plan_item_2 = Plan.objects.filter(
                        network=Network.objects.get(name="GLO")).order_by('plan_amount')
                    plan_item_3 = Plan.objects.filter(
                        network=Network.objects.get(name="AIRTEL")).order_by('plan_amount')
                    plan_item_4 = Plan.objects.filter(
                        network=Network.objects.get(name="9MOBILE")).order_by('plan_amount')

                    user = request.user
                    if user.user_type == "Affilliate":
                            plan_serializer = PlanSerializer2(plan_item,many=True)
                            plan_serializerG = PlanSerializer2(Plan.objects.filter(network=Network.objects.get(name="MTN")).filter(plan_type="GIFTING"),many=True)
                            plan_serializerSME = PlanSerializer2(Plan.objects.filter(network=Network.objects.get(name="MTN")).filter(plan_type="SME"),many=True)


                            plan_serializer_2 = PlanSerializer2(plan_item_2,many=True)
                            plan_serializer_3 = PlanSerializer2(plan_item_3,many=True)
                            plan_serializer_4 = PlanSerializer2(plan_item_4,many=True)




                    elif user.user_type == "TopUser":

                            plan_serializer = PlanSerializer3(plan_item,many=True)
                            plan_serializerG = PlanSerializer3(Plan.objects.filter(network=Network.objects.get(name="MTN")).filter(plan_type="GIFTING"),many=True)
                            plan_serializerSME = PlanSerializer3(Plan.objects.filter(network=Network.objects.get(name="MTN")).filter(plan_type="SME"),many=True)


                            plan_serializer_2 = PlanSerializer3(plan_item_2,many=True)
                            plan_serializer_3 = PlanSerializer3(plan_item_3,many=True)
                            plan_serializer_4 = PlanSerializer3(plan_item_4,many=True)
                    else:
                            plan_serializer = PlanSerializer(plan_item,many=True)
                            plan_serializerG = PlanSerializer(Plan.objects.filter(network=Network.objects.get(name="MTN")).filter(plan_type="GIFTING"),many=True)
                            plan_serializerSME = PlanSerializer(Plan.objects.filter(network=Network.objects.get(name="MTN")).filter(plan_type="SME"),many=True)


                            plan_serializer_2 = PlanSerializer(plan_item_2,many=True)
                            plan_serializer_3 = PlanSerializer(plan_item_3,many=True)
                            plan_serializer_4 = PlanSerializer(plan_item_4,many=True)

        except:
            pass


        try:
            item = request.user
            cplan_item = CablePlan.objects.filter(
                cablename=Cable.objects.get(name="GOTV")).order_by('plan_amount')
            cplan_item_2 = CablePlan.objects.filter(
                cablename=Cable.objects.get(name="DSTV")).order_by('plan_amount')
            cplan_item_3 = CablePlan.objects.filter(
                cablename=Cable.objects.get(name="STARTIME")).order_by('plan_amount')
            cable_item = CablenameSerializer(Cable.objects.all(), many=True)



        except:
            pass


        try:
                if request.user.user_type == "Affilliate":
                    amt1 = Result_Checker_Pin.objects.get(
                        exam_name="WAEC").Affilliate_price
                    amt2 = Result_Checker_Pin.objects.get(
                        exam_name="NECO").Affilliate_price
                elif request.user.user_type == "TopUser":
                    amt1 = Result_Checker_Pin.objects.get(
                        exam_name="WAEC").TopUser_price
                    amt2 = Result_Checker_Pin.objects.get(
                        exam_name="NECO").TopUser_price


                else:
                    amt1 = Result_Checker_Pin.objects.get(
                        exam_name="WAEC").amount
                    amt2  = Result_Checker_Pin.objects.get(
                        exam_name="NECO").amount

        except:
            pass


        try:
            item = request.user
            user_serializer = CustomUserSerializer(item)
            if request.user.notifications.all():
                x = [x.verb for x in request.user.notifications.all()[:1]][0]
            else:
                x = ""





            return Response({
                'user': user_serializer.data,
                "notification": {"message": x},

                "percentage": PercentageSerializer(Percentage.objects.all(), many=True).data,
                "topuppercentage":  [
                                {
                                    "network": 1,
                                    "percent": mtn,
                                    "percent_s": mtn_s
                                },
                                {
                                    "network": 2,
                                    "percent": glo,
                                    "percent_s": glo_s
                                },
                                {
                                    "network": 3,
                                    "percent": mobile,
                                    "percent_s": mobile_s
                                },
                                {
                                    "network": 4,
                                    "percent": airtel,
                                    "percent_s": airtel_s
                                }],

                "Admin_number": Admin_numberSerializer(Admin_number.objects.all(), many=True).data,
                "Exam":Result_Checker_PinSerializer(Result_Checker_Pin.objects.all(),many=True).data,
                 "Exam": [
                        {
                            "exam_name": "WAEC",
                            "amount": amt1
                        },
                        {
                            "exam_name": "NECO",
                            "amount": amt2
                        }
                    ],
                 "banks":BankAccount_PinSerializer(BankAccount.objects.all(),many=True).data,
                 "Dataplans":{ 'MTN_PLAN': { "SME": plan_serializerSME.data,"GIFTING": plan_serializerG.data,"ALL":  plan_serializer.data},
                               'GLO_PLAN': {"ALL":  plan_serializer_2.data},
                               'AIRTEL_PLAN': { "ALL":  plan_serializer_3.data},
                               '9MOBILE_PLAN': { "ALL":  plan_serializer_4.data},},
                 "Cableplan":{'GOTVPLAN': CablePlanSerializer(cplan_item, many=True).data,
                                'DSTVPLAN': CablePlanSerializer(cplan_item_2, many=True).data,
                                'STARTIME': CablePlanSerializer(cplan_item_3, many=True).data,
                                'cablename':  cable_item.data,},
                "support_phone_number":config.support_phone_number,
                 "recharge": {
                    "mtn": Recharge_pin.objects.filter(network=Network.objects.get(name="MTN")).filter(available=True).count(),
                    "glo": Recharge_pin.objects.filter(network=Network.objects.get(name="GLO")).filter(available=True).count(),
                    "airtel": Recharge_pin.objects.filter(network=Network.objects.get(name="AIRTEL")).filter(available=True).count(),
                    "9mobile": Recharge_pin.objects.filter(network=Network.objects.get(name="9MOBILE")).filter(available=True).count(),
                     "mtn_pin":RechargeSerializer(Recharge.objects.filter(network=Network.objects.get(name="MTN")), many=True).data,
                     "glo_pin":RechargeSerializer(Recharge.objects.filter(network=Network.objects.get(name="GLO")), many=True).data,
                     "airtel_pin":RechargeSerializer(Recharge.objects.filter(network=Network.objects.get(name="AIRTEL")), many=True).data,
                     "9mobile_pin":RechargeSerializer(Recharge.objects.filter(network=Network.objects.get(name="9MOBILE")), many=True).data

                }



            })

        except CustomUser.DoesNotExist:
            return Response(status=404)


class AlertAPIView(APIView):

    def get(self, request, format=None):

        if Info_Alert.objects.all():
            y = [x.message for x in Info_Alert.objects.all()[:1]][0]

        else:
            y = ""

        return Response({

            "alert": y


        })


class CablenameAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            item = request.user
            cplan_item = CablePlan.objects.filter(
                cablename=Cable.objects.get(name="GOTV")).order_by('plan_amount')
            cplan_item_2 = CablePlan.objects.filter(
                cablename=Cable.objects.get(name="DSTV")).order_by('plan_amount')
            cplan_item_3 = CablePlan.objects.filter(
                cablename=Cable.objects.get(name="STARTIME")).order_by('plan_amount')
            cable_item = CablenameSerializer(Cable.objects.all(), many=True)

            return Response({

                'GOTVPLAN': CablePlanSerializer(cplan_item, many=True).data,
                'DSTVPLAN': CablePlanSerializer(cplan_item_2, many=True).data,
                'STARTIME': CablePlanSerializer(cplan_item_3, many=True).data,
                'cablename':  cable_item.data,



            })

        except:
            return Response(status=404)


class DiscoAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:

            disko_item = DiscoSerializer(
                Disco_provider_name.objects.all(), many=True)

            return Response({


                'disko':  disko_item.data,


            })

        except:
            return Response(status=404)


class NetworkAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:

            plan_item = Plan.objects.filter(
                network=Network.objects.get(name="MTN")).order_by('plan_amount')
            plan_item_2 = Plan.objects.filter(
                network=Network.objects.get(name="GLO")).order_by('plan_amount')
            plan_item_3 = Plan.objects.filter(
                network=Network.objects.get(name="AIRTEL")).order_by('plan_amount')
            plan_item_4 = Plan.objects.filter(
                network=Network.objects.get(name="9MOBILE")).order_by('plan_amount')

            plan_serializer = PlanSerializer(plan_item, many=True)
            plan_serializer_2 = PlanSerializer(plan_item_2, many=True)
            plan_serializer_3 = PlanSerializer(plan_item_3, many=True)
            plan_serializer_4 = PlanSerializer(plan_item_4, many=True)

            return Response({

                'MTN_PLAN': plan_serializer.data,
                'GLO_PLAN': plan_serializer_2.data,
                'AIRTEL_PLAN': plan_serializer_3.data,
                '9MOBILE_PLAN': plan_serializer_4.data,



            })

        except:
            return Response(status=404)



class DataAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, format=None):
        try:
            item = Data.objects.filter(user=request.user).get(pk=id)
            serializer = DataSerializer(item)
            return Response(serializer.data)
        except Data.DoesNotExist:
            return Response(status=404)


class DataAPIListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        items = Data.objects.filter(user=request.user).order_by('-create_date')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = DataSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        status = "processing"

        serializer = DataSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            order_username = (serializer.validated_data["user"]).username
            num = serializer.validated_data["mobile_number"]
            plan = serializer.validated_data["plan"]


            net = str(serializer.validated_data["network"])
            user = (serializer.validated_data["user"])
            errors = {}


            def create_id():
                    num = random.randint(1,10)
                    num_2 = random.randint(1,10)
                    num_3 = random.randint(1,10)
                    return str(num_2)+str(num_3)+str(uuid.uuid4())

            ident = create_id()


            previous_bal = user.Account_Balance

            if user.user_type == "Affilliate":
                amount = float(plan.Affilliate_price)

            elif user.user_type == "API":
                amount = float(plan.api_price)

            elif user.user_type == "TopUser":

                amount = float(plan.TopUser_price)
            else:
                amount = float(plan.plan_amount)

            with transaction.atomic():
                check = user.withdraw(user.id, amount)
                if check == False:
                    errors['error'] = u'Y insufficient balance '
                    raise serializers.ValidationError(errors)
                Wallet_summary.objects.create(user=user, product="{} {}{}   N{}  DATA topup topup  with {} ".format(
                    net, plan.plan_size, plan.plan_Volume, amount, num), amount=amount, previous_balance=previous_bal, after_balance=(previous_bal - amount))

            def sendmessage(sender,message,to,route):
                   payload={
                     'sender':sender,
                     'to': to,
                     'message': message,
                     'type': '0',
                     'routing':route,
                     'token':'EGZ1zr8wYJUajiAcxrOsCkMfv0EaTnGsHGHLePhZjlnsDQnOfD',
                     'schedule':'',
                          }

                   url = "https://app.smartsmssolutions.ng/io/api/client/v1/sms/"
                   response = requests.post(url, params=payload, verify=False)

            # def sendmessage(sender, message, to, route):
            #     payload = {
            #         'sender': sender,
            #         'to': to,
            #         'message': message,
            #         'type': '0',
            #         'routing': route,
            #         'token': 'cYTj0CCFuGM4PSrvABkoANCBNlNF2SoipZFSNlz5hmKnejg6fubGLFu7Ph2URDj22dWGYjlRqDILQz7kHxARBlAwdC4CpTKHGC5D',
            #         'schedule': '', }
            #     baseurl = f'https://sms.hollatags.com/api/send/?user={config.hollatag_username}&pass={config.hollatag_password}&to={to}&from={sender}&msg={urllib.parse.quote(message)}'
            #     response = requests.get(baseurl, verify=False)

            def senddatasmeplug(net,plan_id,num):
                    url = "https://smeplug.ng/api/v1/data/purchase"
                    payload = {"network_id": net,"plan_id":plan_id,"phone": num}
                    payload = json.dumps(payload)

                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {config.sme_plug_secret_key}'
                    }
                    #print("payload",payload)
                    response = requests.request("POST", url, headers=headers, data = payload)
                    return response

            # def sendsmedata(shortcode,servercode,message,mytype):
            def sendsmedata(shortcode,servercode,message,token,mytype):
                        payload={
                            'shortcode':shortcode,
                            'servercode': servercode,
                            'message':message,
                            'token': f"{config.simhost_API_key}",
                            'type':mytype

                                }

                        baseurl ='https://ussd.simhosting.ng/api/?'
                        response = requests.get(baseurl,params=payload,verify=False)
                        #print(response.text)


            def senddata(ussd,servercode,mytype):
                    payload={
                        'ussd':ussd,
                        'servercode': servercode,
                            'token': f"{config.simhost_API_key}",
                        'type':mytype

                            }

                    baseurl ='https://ussd.simhosting.ng/api/?'
                    response = requests.get(baseurl,params=payload,verify=False)
                    #print(response.text)

            def msorg_senddata(netid,num,plan_id):

                        url = f"{config.msorg_web_url}/api/data/"

                        headers = {
                        'Content-Type':'application/json',
                        'Authorization': f'Token {config.msorg_web_api_key}'
                        }
                        param = {"network": netid,"mobile_number": num,"plan": plan_id,"Ported_number":True}
                        #print(url)
                        #print("hello mojeed ", param)
                        param_data = json.dumps(param)
                        # response = requests.post(url, headers=headers, data=param_data, verify=False)
                        response = requests.post(url, headers=headers, data=param_data)
                        return response

            def Msplug_Data_vending(net,plan,num,sim,rtype,device_id):
                    url = "https://www.msplug.com/api/buy-data/"
                    payload = {"network":net,
                                "plan_id": plan,
                                "phone":num,
                                "device_id":device_id,
                                "sim_slot":sim,
                                "request_type":rtype,
                                "webhook_url":"http://www.husmodata.com/buydata/webhook/"
                                }
                    headers = {
                    'Authorization': f'Token {config.msplug_API_key}',
                    'Content-Type': 'application/json'
                    }

                    response = requests.post(url, headers=headers, data = json.dumps(payload))
                    #print(response.text)

            def VTUAUTO_Shortcode(shortcode,message,device_id,slot):
                    payload = {
                            "device_id":device_id,
                            "message":message,
                            "message_recipient":shortcode,
                            "sim":slot}
                    response = requests.post("https://vtuauto.ng/api/v1/request/sms", auth=HTTPBasicAuth(f'{config.vtu_auto_email}', f'{config.vtu_auto_password}'), data=payload)
                    #print(response.text)


            def VTUAUTO_USSD(ussd,device_id,sim):
                        payload = {
                                "device_id":device_id,
                                "ussd_string":ussd,
                                "sim":sim}
                        response = requests.post("https://vtuauto.ng/api/v1/request/ussd", auth=HTTPBasicAuth(f'{config.vtu_auto_email}', f'{config.vtu_auto_password}'), data=payload)
                        #print(response.text)

            def senddatasmeify(net,plan,num,validity):
                    headers = { 'Content-Type': 'application/json', 'Authorization': f'Bearer {SmeifyAuth.objects.first().get_token()}'}
                    url =   f"https://auto.smeify.com/api/v1/online/data?network={net}&&volume={int(plan)}&&phone={num}&&plan={validity}"
                    respons = requests.request("POST", url, headers=headers)
                    #print(respons.text)



            if net == 'MTN':
                            mtn_text = SME_text.objects.get(network=Network.objects.get(name='MTN'))

                            if plan.plan_type == "CORPORATE GIFTING":
                                        if Network.objects.get(name=net).corporate_data_vending_medium == "SMEPLUG":
                                             resp = senddatasmeplug("1",plan.smeplug_id,num)
                                             status = "successful"

                                        elif Network.objects.get(name=net).corporate_data_vending_medium == "CG_KONNECT":
                                                url = "https://www.cgkonnect.com/api/data/"
                                                payload = {
                                                    "network": 1,
                                                    "mobile_number": num,
                                                    "plan": plan.cgkonnect_id,
                                                    "Ported_number": True
                                                }
                                                payload = json.dumps(payload)
                                                headers = {
                                                  'Authorization': 'Token dd335622635f245bac022687bd37988589eba19d',
                                                  'Content-Type': 'application/json'
                                                }

                                                response = requests.post(url, headers=headers, data = payload)
                                                result = json.loads(response.text)

                                                if response.status_code == 200 or response.status_code == 201:
                                                    status = "successful"
                                                    # messages.success(self.request,"success {}".format(result['Status']))
                                                else:
                                                    return Response(serializer.errors, status=400)


                                        elif Network.objects.get(name=net).corporate_data_vending_medium == "MSORG_DEVELOPED_WEBSITE":
                                                  msorg_senddata(Network.objects.get(name=net).msorg_web_net_id,num,plan.smeplug_id)
                                                  status = "successful"

                                        elif Network.objects.get(name=net).corporate_data_vending_medium == "USSD":

                                                    def sendsmedata(ussd,num,servercode):
                                                        payload={
                                                            'ussd':ussd,
                                                            'servercode': servercode,
                                                            'multistep':num,
                                                            'token': f"{config.simhost_API_key}",
                                                           }

                                                        baseurl ="https://ussd.simhosting.ng/api/ussd/?"
                                                        response = requests.get(baseurl,params=payload,verify=False)
                                                        #print(response.text)

                                                    ussd =  plan.ussd_string
                                                    senddata(f"{ussd}",num,mtn_text.sim_host_server_id)
                                                    status = 'successful'


                                        elif Network.objects.get(name=net).corporate_data_vending_medium == "UWS":

                                                def create_id():
                                                    num = random.randint(1,10)
                                                    num_2 = random.randint(1,10)
                                                    num_3 = random.randint(1,10)
                                                    return str(num_2)+str(num_3)+str(uuid.uuid4())

                                                ident = create_id()

                                                while Data.objects.filter(ident= ident).exists():
                                                        ident = create_id()


                                                url = "https://api.uws.com.ng/api/v1/mtn_coperate_data/purchase"

                                                headers = {
                                                    'Content-Type': 'application/json',
                                                    'Accept': 'application/json',
                                                    'Authorization': f'Bearer {config.uws_token}'
                                                }
                                                payload = {"phone" : num, "plan_id" : str(plan.uws_plan_name_id), "customRef" : ident}

                                                response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
                                                result = json.loads(response.text)
                                                # print(result)
                                                # print(response.status_code)

                                                if result['status'] == "success":
                                                    status = 'successful'

                                                elif result['status'] == "failed":
                                                    status = 'failed'

                                                else:
                                                    status = 'processing'


                                        else:
                                                    try:
                                                        sendmessage('myweb',"{0} want to buy {1}{3}  M_TN data on {2} ".format(user.username,plan.plan_size,num,plan.plan_Volume),mtn_text.number,"02")
                                                        status = 'successful'
                                                    except:
                                                            pass

                            elif plan.plan_type == "GIFTING":

                                        if Network.objects.get(name=net).gifting_data_vending_medium == "SMEPLUG":
                                             resp = senddatasmeplug("1",plan.smeplug_id,num)
                                             status = "successful"


                                        elif Network.objects.get(name=net).gifting_data_vending_medium == "MSORG_DEVELOPED_WEBSITE":
                                                  msorg_senddata(Network.objects.get(name=net).msorg_web_net_id,num,plan.plan_name_id)
                                                  status = "successful"

                                        elif Network.objects.get(name=net).gifting_data_vending_medium == "USSD":

                                                    def sendgiftdata(ussd,num,servercode):
                                                        payload={
                                                            'ussd':ussd,
                                                            'servercode': servercode,
                                                            'multistep':num,
                                                            'token': f"{config.simhost_API_key}",
                                                           }

                                                        baseurl ="https://ussd.simhosting.ng/api/ussd/?"
                                                        response = requests.get(baseurl,params=payload,verify=False)
                                                        #print(response.text)

                                                    ussd =  plan.ussd_string
                                                    sendgiftdata(f"{ussd}",num,mtn_text.sim_host_server_id)
                                                    status = 'successful'


                                        elif Network.objects.get(name=net).gifting_data_vending_medium == "UWS":

                                                        def create_id():
                                                                num = random.randint(1,10)
                                                                num_2 = random.randint(1,10)
                                                                num_3 = random.randint(1,10)
                                                                return str(num_2)+str(num_3)+str(uuid.uuid4())

                                                        ident = create_id()

                                                        while Data.objects.filter(ident= ident).exists():
                                                              ident = create_id()


                                                        url = "https://api.uws.com.ng/api/v1/mtn_coperate_data/purchase"

                                                        payload = {"phone" : num,"plan_id" : str(plan.plan_name_id),"customRef" : ident}

                                                        headers = {
                                                                    'Content-Type': 'application/json',
                                                                    'Accept': 'application/json',
                                                                    'Authorization': f'Bearer {config.uws_token}'
                                                                    }

                                                        response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
                                                        status = 'successful'
                                                        #print(response.text)


                                        else:
                                                    try:
                                                        sendmessage('myweb',"{0} want to buy {1}{3}  M_TN data on {2} ".format(user.username,plan.plan_size,num,plan.plan_Volume),mtn_text.number,"02")
                                                        status = 'successful'
                                                    except:
                                                            pass

                            else:
                                        if Network.objects.get(name=net).data_vending_medium ==  "SIMHOST":

                                                         if float(plan.plan_size) == 500.0:
                                                            if mtn_text.new_data_vending_medium_for_random == "NORMAL_SLOT":
                                                                   sendsmedata("131",'1R5PHM42DVAYOZPHQ29E','SMEB {} 500 {}'.format(num,mtn_text.pin2),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                                   status = 'successful'

                                                            elif mtn_text.new_data_vending_medium_for_random == "OLDSIM":
                                                              sendsmedata("131",'PU7KFKHP9RZKY75XQ4H4','SMEB {} 500 {}'.format(num,mtn_text.pin),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                              #print("hello mojeed 500mb this is old sim")
                                                              status = 'successful'

                                                            elif mtn_text.new_data_vending_medium_for_random == "NEWSIM":
                                                              sendsmedata("131",'PHG62KSN79ONJ6F9IJTY','SMEB {} 500 {}'.format(num,mtn_text.pin3),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                              #print("hello mojeed 500mb this is new sim")
                                                              status = 'successful'

                                                         elif float(plan.plan_size) == 1.0:
                                                            if mtn_text.data_vending_medium_for_1_gb == "OLDSIM":
                                                              sendsmedata("131",'PU7KFKHP9RZKY75XQ4H4','SMEC {} 1000 {}'.format(num,mtn_text.pin),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                              #print("hello mojeed this is old sim")
                                                              status = 'successful'

                                                            elif mtn_text.data_vending_medium_for_1_gb == "NEWSIM":
                                                              sendsmedata("131",'PHG62KSN79ONJ6F9IJTY','SMEC {} 1000 {}'.format(num,mtn_text.pin3),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                              #print("hello mojeed this is new sim")
                                                              status = 'successful'

                                                         elif float(plan.plan_size) == 2.0:
                                                            if mtn_text.new_data_vending_medium_for_random == "NORMAL_SLOT":
                                                                  sendsmedata("131",'1R5PHM42DVAYOZPHQ29E','SMED {} 2000 {}'.format(num,mtn_text.pin2),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                                  status = 'successful'

                                                            elif mtn_text.new_data_vending_medium_for_random == "OLDSIM":
                                                              sendsmedata("131",'PU7KFKHP9RZKY75XQ4H4','SMED {} 2000 {}'.format(num,mtn_text.pin),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                              #print("hello mojeed 2gb this is old sim")
                                                              status = 'successful'

                                                            elif mtn_text.new_data_vending_medium_for_random == "NEWSIM":
                                                              sendsmedata("131",'PHG62KSN79ONJ6F9IJTY','SMED {} 2000 {}'.format(num,mtn_text.pin3),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                              #print("hello mojeed 2gb this is new sim")
                                                              status = 'successful'



                                                         elif float(plan.plan_size) == 5.0:
                                                            if mtn_text.new_data_vending_medium_for_random == "NORMAL_SLOT":
                                                                 sendsmedata("131",'1R5PHM42DVAYOZPHQ29E','SMEE {} 5000 {}'.format(num,mtn_text.pin2),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                                 status = 'successful'

                                                            elif mtn_text.new_data_vending_medium_for_random == "OLDSIM":
                                                              sendsmedata("131",'PU7KFKHP9RZKY75XQ4H4','SMEE {} 5000 {}'.format(num,mtn_text.pin),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                              #print("hello mojeed 5gb this is old sim")
                                                              status = 'successful'

                                                            elif mtn_text.new_data_vending_medium_for_random == "NEWSIM":
                                                              sendsmedata("131",'PHG62KSN79ONJ6F9IJTY','SMEE {} 5000 {}'.format(num,mtn_text.pin3),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                              #print("hello mojeed 5gb this is new sim")
                                                              status = 'successful'

                                                         elif float(plan.plan_size) == 3.0:
                                                            if mtn_text.new_data_vending_medium_for_random == "NORMAL_SLOT":
                                                                 sendsmedata("131",'1R5PHM42DVAYOZPHQ29E','SMEF {} 3000 {}'.format(num,mtn_text.pin2),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                                 status = 'successful'

                                                            elif mtn_text.new_data_vending_medium_for_random == "OLDSIM":
                                                              sendsmedata("131",'PU7KFKHP9RZKY75XQ4H4','SMEF {} 3000 {}'.format(num,mtn_text.pin),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                              #print("hello mojeed 3gb this is old sim")
                                                              status = 'successful'

                                                            elif mtn_text.new_data_vending_medium_for_random == "NEWSIM":
                                                              sendsmedata("131",'PHG62KSN79ONJ6F9IJTY','SMEF {} 3000 {}'.format(num,mtn_text.pin3),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                              #print("hello mojeed 3gb this is new sim")
                                                              status = 'successful'

                                                         elif float(plan.plan_size) == 10.0:
                                                            if mtn_text.new_data_vending_medium_for_random == "NORMAL_SLOT":
                                                                 sendsmedata("131",'1R5PHM42DVAYOZPHQ29E','SMEG {} 10000 {}'.format(num,mtn_text.pin2),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                                 status = 'successful'

                                                            elif mtn_text.new_data_vending_medium_for_random == "OLDSIM":
                                                              sendsmedata("131",'PU7KFKHP9RZKY75XQ4H4','SMEG {} 10000 {}'.format(num,mtn_text.pin),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                              #print("hello mojeed 10gb this is old sim")
                                                              status = 'successful'

                                                            elif mtn_text.new_data_vending_medium_for_random == "NEWSIM":
                                                              sendsmedata("131",'PHG62KSN79ONJ6F9IJTY','SMEG {} 10000 {}'.format(num,mtn_text.pin3),'	N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','SHORTCODE')
                                                              #print("hello mojeed 10gb this is new sim")
                                                              status = 'successful'


                                                         else:


                                                               sendmessage('HusmoData',"{0} want to buy {1}{3}  M_TN data on {2} ".format(user.username,plan.plan_size,num,plan.plan_Volume),mtn_text.number,"02")

                                                        # if plan.plan_type == "SME":
                                                        #         if mtn_text.mtn_sme_route  == "SMS":
                                                        #             command =  plan.sms_command.replace("n",num).replace("p",mtn_text.pin)
                                                        #             sendsmedata("131",mtn_text.sim_host_server_id,f'{command}','SHORTCODE')
                                                        #             status = 'successful'
                                                        #         else:
                                                        #             ussd =  plan.ussd_string.replace("n",num).replace("p",mtn_text.pin)
                                                        #             senddata(f"{ussd}",mtn_text.sim_host_server_id,'USSD')
                                                        #             status = 'successful'
                                                        # else:
                                                        #     sendmessage('myweb',"{0} want to buy {1}{3}  M_TN data on {2} ".format(user.username,plan.plan_size,num,plan.plan_Volume),mtn_text.number,"02")

                                        elif Network.objects.get(name=net).data_vending_medium == "UWS":

                                                    def create_id():
                                                            num = random.randint(1,10)
                                                            num_2 = random.randint(1,10)
                                                            num_3 = random.randint(1,10)
                                                            return str(num_2)+str(num_3)+str(uuid.uuid4())

                                                    ident = create_id()

                                                    while Data.objects.filter(ident= ident).exists():
                                                          ident = create_id()


                                                    url = "https://api.uws.com.ng/api/v1/sme_data/purchase"

                                                    payload = {
                                                        "phone" : num,
                                                        "network_id" : "2",
                                                        "plan_id" : str(plan.uws_plan_name_id),
                                                        "customRef" : ident
                                                    }

                                                    headers = {
                                                        'Content-Type': 'application/json',
                                                        'Accept': 'application/json',
                                                        'Authorization': f'Bearer {config.uws_token}'
                                                    }

                                                    response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
                                                    result = json.loads(response.text)
                                                    # print(result)
                                                    # print(response.status_code)

                                                    if result['status'] == "success":
                                                        status = 'successful'

                                                    elif result['status'] == "failed":
                                                        status = 'failed'

                                                    else:
                                                        status = 'processing'

                                        elif Network.objects.get(name=net).data_vending_medium =='SMEPLUG':
                                                        resp = senddatasmeplug("1",plan.smeplug_id,num)
                                                        status = "successful"

                                        elif Network.objects.get(name=net).data_vending_medium =='SMS':
                                                sendmessage('myweb', "{0} want to buy {1}{3}  M_TN data on {2} ".format(user.username, plan.plan_size, num, plan.plan_Volume),mtn_text.number, "02")

                                        elif Network.objects.get(name=net).data_vending_medium  == "MSORG_DEVELOPED_WEBSITE":
                                                  msorg_senddata(Network.objects.get(name=net).msorg_web_net_id,num,plan.plan_name_id)
                                                  status = "successful"

                                        elif Network.objects.get(name=net).data_vending_medium =='VTUAUTO':

                                                if mtn_text.mtn_sme_route  == "SMS":
                                                        command =  plan.sms_command.replace("n",num).replace("p",mtn_text.pin)
                                                        VTUAUTO_Shortcode("131",f'{command}',mtn_text.vtu_auto_device_id ,mtn_text.vtu_sim_slot)

                                                        status = 'successful'
                                                else:
                                                        ussd =  plan.ussd_string.replace("n",num).replace("p",mtn_text.pin)
                                                        VTUAUTO_USSD(f"{ussd}",mtn_text.vtu_auto_device_id, mtn_text.vtu_sim_slot)
                                                        status = 'successful'

                                        elif Network.objects.get(name=net).data_vending_medium =='MSPLUG':
                                            if mtn_text.mtn_sme_route  == "SMS":
                                                    Msplug_Data_vending(net,plan.msplug_plan_name_id,num,mtn_text.msplug_sim_slot,"SMS",mtn_text.msplug_device_id)
                                                    status = 'successful'
                                            else:
                                                    Msplug_Data_vending(net,plan.msplug_plan_name_id,num,mtn_text.msplug_sim_slot,"USSD",mtn_text.msplug_device_id)
                                                    status = 'successful'


                                        elif Network.objects.get(name=net).data_vending_medium =='SMEIFY':
                                                         senddatasmeify(net,plan.smeify_plan_name_id,num,plan.month_validate)
                                                         status = 'successful'



            elif net == 'GLO':
                            glo_text = SME_text.objects.get(network=Network.objects.get(name='GLO'))
                            ussd = plan.ussd_string.replace("p",num)


                            if Network.objects.get(name=net).data_vending_medium ==  "SIMHOST":

                                         def senddata(ussd,servercode,token,mytype):
                                                    payload={
                                                        'ussd':ussd,
                                                        'servercode': servercode,
                                                        'token': token,
                                                        'type':mytype

                                                            }

                                                    baseurl ='https://ussd.simhosting.ng/api/?'
                                                    try:
                                                        response = requests.get(baseurl,params=payload,verify=False)
                                                    except:
                                                        pass



                                         if float(plan.plan_size) == 1.05:

                                             senddata("*127*57*{}#".format(num),'PEA9M9IYOCDJKG5K2D94','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                             status = 'successful'


                                         elif float(plan.plan_size) == 2.5:

                                             senddata("*127*53*{}#".format(num),'PEA9M9IYOCDJKG5K2D94','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                             status = 'successful'

                                         elif float(plan.plan_size) == 4.1:

                                              senddata("*127*16*{}#".format(num),'PEA9M9IYOCDJKG5K2D94','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                              status = 'successful'

                                         elif float(plan.plan_size) == 5.8:

                                              senddata("*127*55*{}#".format(num),'PEA9M9IYOCDJKG5K2D94','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                              status = 'successful'

                                         elif float(plan.plan_size) == 7.7:


                                              senddata("*127*58*{}#".format(num),'PEA9M9IYOCDJKG5K2D94','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                              status = 'successful'



                                         elif float(plan.plan_size) == 10.0:

                                              senddata("*127*54*{}#".format(num),'PEA9M9IYOCDJKG5K2D94','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                              status = 'successful'


                                         elif float(plan.plan_size) == 13.25:

                                              senddata("*127*59*{}#".format(num),'PEA9M9IYOCDJKG5K2D94','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                              status = 'successful'



                                         elif float(plan.plan_size) == 18.25:

                                             senddata("*127*2*{}#".format(num),'PEA9M9IYOCDJKG5K2D94','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                             status = 'successful'


                                         elif float(plan.plan_size) == 29.5:

                                              senddata("*127*1*{}#".format(num),'PEA9M9IYOCDJKG5K2D94','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                              status = 'successful'


                                         elif float(plan.plan_size) == 50.0:

                                              senddata("*127*11*{}#".format(num),'PEA9M9IYOCDJKG5K2D94','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                              status = 'successful'


                                         elif float(plan.plan_size) == 93.0:

                                              senddata("*127*12*{}#".format(num),'PEA9M9IYOCDJKG5K2D94','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                              status = 'successful'


                                         elif float(plan.plan_size) == 119.0:

                                              senddata("*127*13*{}#".format(num),'PEA9M9IYOCDJKG5K2D94','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                              status = 'successful'



                                         elif float(plan.plan_size) == 138.0:

                                              senddata("*127*33*{}#".format(num),'PEA9M9IYOCDJKG5K2D94','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')


                                              status = 'successful'

                                        #  senddata(f"{ussd}",glo_text.sim_host_server_id,'USSD')
                                        #  status = 'successful'

                            elif Network.objects.get(name=net).data_vending_medium == "UWS":

                                    def create_id():
                                            num = random.randint(1,10)
                                            num_2 = random.randint(1,10)
                                            num_3 = random.randint(1,10)
                                            return str(num_2)+str(num_3)+str(uuid.uuid4())

                                    ident = create_id()

                                    while Data.objects.filter(ident= ident).exists():
                                          ident = create_id()


                                    url = "https://api.uws.com.ng/api/v1/sme_data/purchase"

                                    payload = {
                                        "phone" : num,
                                        "network_id" : "3",
                                        "plan_id" : str(plan.uws_plan_name_id),
                                        "customRef" : ident
                                    }

                                    headers = {
                                        'Content-Type': 'application/json',
                                        'Accept': 'application/json',
                                        'Authorization': f'Bearer {config.uws_token}'
                                    }

                                    response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
                                    result = json.loads(response.text)
                                    # print(result)
                                    # print(response.status_code)

                                    if result['status'] == "success":
                                        status = 'successful'

                                    elif result['status'] == "failed":
                                        status = 'failed'

                                    else:
                                        status = 'processing'

                            elif Network.objects.get(name=net).data_vending_medium =='SMEPLUG':
                                            resp = senddatasmeplug("4",plan.smeplug_id,num)
                                            status = "successful"


                            elif Network.objects.get(name=net).data_vending_medium  == "MSORG_DEVELOPED_WEBSITE":
                                        msorg_senddata(Network.objects.get(name=net).msorg_web_net_id,num,plan.plan_name_id)
                                        status = "successful"

                            elif Network.objects.get(name=net).data_vending_medium =='SMS':
                                    sendmessage('myweb', "{0} want to buy {1}{3}  GLO-DATA data on {2} ".format(user.username, plan.plan_size, num, plan.plan_Volume), glo_text.number, "02")

                            elif Network.objects.get(name=net).data_vending_medium =='VTUAUTO':
                                         VTUAUTO_USSD(f"{ussd}",glo_text.vtu_auto_device_id, glo_text.vtu_sim_slot)
                                         status = 'successful'



                            elif Network.objects.get(name=net).data_vending_medium =='MSPLUG':
                                Msplug_Data_vending(net,plan.msplug_plan_name_id,num,glo_text.msplug_sim_slot,"SMS",glo_text.msplug_device_id)
                                status = 'successful'

                            elif Network.objects.get(name=net).data_vending_medium =='SMEIFY':
                                            senddatasmeify(net,plan.smeify_plan_name_id,num,plan.month_validate)
                                            status = 'successful'

            elif net == 'AIRTEL':
                            airtel_text = SME_text.objects.get(network=Network.objects.get(name='AIRTEL'))
                            # ussd = plan.ussd_string.replace("n",num).replace("p",airtel_text.pin)

                            if Network.objects.get(name=net).data_vending_medium ==  "SIMHOST":


                                    def senddata(ussd,servercode,token,mytype):
                                                    payload={
                                                        'ussd':ussd,
                                                        'servercode': servercode,
                                                        'token': token,
                                                        'type':mytype

                                                            }

                                                    baseurl ='https://ussd.simhosting.ng/api/?'
                                                    try:
                                                        response = requests.get(baseurl,params=payload,verify=False)
                                                    except:
                                                        pass

                                    if float(plan.plan_size) == 11.0:

                                        #  senddata("*141*7*2*1*1*1*{}*6090#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                         senddata("*432*2*2*1*1*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                         status = 'successful'

                                    # elif float(plan.plan_size) == 10.0:

                                    #      senddata("*141#",'6,2,1,2,1,{},6090'.format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                    #      status = 'successful'

                                    elif float(plan.plan_size) == 10.0:

                                         senddata("*432*2*2*1*2*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                         status = 'successful'

                                    elif float(plan.plan_size) == 6.0:

                                         senddata("*432*2*2*1*3*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                         status = 'successful'

                                    elif float(plan.plan_size) == 4.5:

                                         senddata("*432*2*2*1*4*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                         status = 'successful'

                                    elif float(plan.plan_size) == 3.0:

                                         senddata("*432*2*2*1*5*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                         status = 'successful'


                                    elif float(plan.plan_size) == 2.0:

                                         senddata("*432*2*2*1*6*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                         status = 'successful'


                                    elif float(plan.plan_size) == 1.5:
                                        senddata("*141*8*2*1*7*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                        status = 'successful'

                                        # def senddata(ussd,nums,servercode,token):
                                        #     payload={
                                        #         'ussd':ussd,
                                        #         'multistep':nums,
                                        #         'servercode': servercode,
                                        #         'token': token,
                                        #         # 'type':mytype


                                        #             }

                                        #     baseurl ="https://ussd.simhosting.ng/api/ussd/?"
                                        #     response = requests.get(baseurl,params=payload,verify=False)

                                        #     #print('..........................hello mojeed.........................')
                                        #     #print(response)
                                        #     #print('..........................hello mojeed.........................')
                                        #     #print(payload)

                                        # senddata("*141#",'7,2,1,7,1,{},1939'.format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn')
                                        # status = 'successful'

                                        # # senddata("*432*2*2*1*7*1*{}*6090# ".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                        # # status = 'successful'

                                    elif float(plan.plan_size) == 6000.0:

                                         senddata("*432*2*2*2*1*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                         status = 'successful'


                                    elif float(plan.plan_size) == 1.0:

                                         senddata("*141*7*2*2*2*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                         status = 'successful'


                                    elif float(plan.plan_size) == 750.0:

                                          senddata("*432*2*2*2*3*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                          status = 'successful'

                                    elif float(plan.plan_size) == 2000.0:


                                          senddata("*432*2*2*3*1*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                          status = 'successful'


                                    elif float(plan.plan_size) == 1000.0:

                                          senddata("*432*2*2*3*3*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                          status = 'successful'


                                    elif float(plan.plan_size) == 350.0:

                                         senddata("*432*2*2*3*4*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                         status = 'successful'


                                    elif float(plan.plan_size) == 200.0:

                                          senddata("*141*7*2*3*5*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                          status = 'successful'

                                    elif float(plan.plan_size) == 110.0:

                                          senddata("*432*2*2*4*1*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                          status = 'successful'

                                    elif float(plan.plan_size) == 75.0:

                                          senddata("432*2*2*4*2*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                          status = 'successful'

                                    elif float(plan.plan_size) == 40.0:

                                          senddata("*432*2*2*4*3*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                          status = 'successful'

                                    elif float(plan.plan_size) == 20.0:

                                          senddata("*432*2*2*4*4*1*{}*1939#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                          status = 'successful'


                                    # if float(plan.plan_size) == 200.0:

                                    #          senddata("*141*6*2*3*5*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 1000.0:

                                    #          senddata("*141*6*2*3*3*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 2000.0:

                                    #          senddata("*141*6*2*3*1*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 350.0:

                                    #          senddata("*141*6*2*3*4*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 1.0:

                                    #          senddata("*141*6*2*2*2*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 6000.0:

                                    #          senddata("*141*6*2*2*1*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 750.0:

                                    #          senddata("*141*6*2*2*3*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 1.5:
                                    #         #  #print("... airtel 2GB .......")
                                    #          senddata("*141*6*2*1*7*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                    #         #  #print("... airtel 2GB getting .......")
                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 2.0:

                                    #          senddata("*141*6*2*1*6*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 3.0:

                                    #          senddata("*141*6*2*1*5*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 4.5:

                                    #          senddata("*141*6*2*1*4*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 6.0:

                                    #          senddata("*141*6*2*1*3*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 10.0:

                                    #          senddata("*141*6*2*1*2*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 11.0:

                                    #          senddata("*141*6*2*1*1*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 20.0:

                                    #          senddata("*141*6*2*4*4*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 40.0:

                                    #          senddata("*141*6*2*4*3*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 75.0:

                                    #          senddata("*141*6*2*4*2*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                    # elif float(plan.plan_size) == 110.0:

                                    #          senddata("*141*6*2*4*1*1*{}*9735#".format(num),'8XCX4RX3MI9PFSGWJK87','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                    #          status = 'successful'

                                        # senddata(f"{ussd}",airtel_text.sim_host_server_id,'USSD')
                                        # senddata("*123#".format(num),airtel_text.sim_host_server_id,'USSD')
                                        # status = 'successful'

                            elif Network.objects.get(name=net).data_vending_medium == "UWS":
                                                    print('--------------------------------- AIRTEL DATA TO UWS')
                                                    def create_id():
                                                            num = random.randint(1,10)
                                                            num_2 = random.randint(1,10)
                                                            num_3 = random.randint(1,10)
                                                            return str(num_2)+str(num_3)+str(uuid.uuid4())

                                                    ident = create_id()

                                                    while Data.objects.filter(ident= ident).exists():
                                                          ident = create_id()


                                                    url = "https://api.uws.com.ng/api/v1/sme_data/purchase"

                                                    payload = {
                                                        "phone" : num,
                                                        "network_id" : "1",
                                                        "plan_id" : str(plan.uws_plan_name_id),
                                                        "customRef" : ident
                                                    }

                                                    headers = {
                                                        'Content-Type': 'application/json',
                                                        'Accept': 'application/json',
                                                        'Authorization': f'Bearer {config.uws_token}'
                                                    }

                                                    response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
                                                    result = json.loads(response.text)
                                                    print(payload)
                                                    print(response.text)
                                                    # print(response.status_code)

                                                    if result['status'] == "success":
                                                        status = 'successful'

                                                    elif result['status'] == "failed":
                                                        status = 'failed'

                                                    else:
                                                        status = 'processing'

                            elif Network.objects.get(name=net).data_vending_medium =='SMEPLUG':
                                            resp = senddatasmeplug("2",plan.smeplug_id,num)
                                            status = "successful"

                            elif Network.objects.get(name=net).data_vending_medium =='SMS':
                                    sendmessage('myweb', "{0} want to buy {1}{3}  AIRTEL-DATA data on {2} ".format(user.username, plan.plan_size, num, plan.plan_Volume), "08101238850", "02")

                            elif Network.objects.get(name=net).data_vending_medium  == "MSORG_DEVELOPED_WEBSITE":
                                        msorg_senddata(Network.objects.get(name=net).msorg_web_net_id,num,plan.plan_name_id)
                                        status = "successful"

                            elif Network.objects.get(name=net).data_vending_medium =='VTUAUTO':

                                        VTUAUTO_USSD(f"{ussd}",airtel_text.vtu_auto_device_id, airtel_text.vtu_sim_slot)
                                        VTUAUTO_USSD("*123#".format(num),airtel_text.vtu_auto_device_id, airtel_text.vtu_sim_slot)
                                        status = 'successful'


                            elif Network.objects.get(name=net).data_vending_medium =='MSPLUG':
                                   Msplug_Data_vending(net,plan.msplug_plan_name_id,num,airtel_text.msplug_sim_slot,"USSD",airtel_text.msplug_device_id)
                                   status = 'successful'

                            elif Network.objects.get(name=net).data_vending_medium =='SMEIFY':
                                    senddatasmeify(net,plan.smeify_plan_name_id,num,plan.month_validate)
                                    status = 'successful'

            elif net == "9MOBILE":

                            mobile_text = SME_text.objects.get(network=Network.objects.get(name='9MOBILE'))
                            # ussd = plan.ussd_string.replace("n",num)

                            if Network.objects.get(name=net).data_vending_medium ==  "SIMHOST":

                                    def senddata(ussd,nums,servercode,token):
                                            payload={
                                                'ussd':ussd,
                                                'multistep':nums,
                                                'servercode': servercode,
                                                'token': token,
                                                # 'type':mytype


                                                    }

                                            baseurl ="https://ussd.simhosting.ng/api/ussd/?"
                                            response = requests.get(baseurl,params=payload,verify=False)
                                            # nums = plan.ussd_nums.replace("n",num)
                                            # #print(nums)

                                            # senddata(f"{ussd}",'IMRVF5SJ3AVNOG5GC278','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')

                                            #print('..........................hello mojeed.........................')
                                            #print(response)
                                            #print('..........................hello mojeed.........................')
                                            #print(payload)

                                    if float(plan.plan_size) == 25.0:

                                         senddata("*200*3*5*1*1*1#",'1*{}#'.format(num),'IMRVF5SJ3AVNOG5GC278','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn')
                                         status = 'successful'

                                    elif float(plan.plan_size) == 100.0:

                                         senddata("*200*3*5*1*2*1#",'1*{}#'.format(num),'IMRVF5SJ3AVNOG5GC278','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn')
                                         status = 'successful'

                                    elif float(plan.plan_size) == 650.0:

                                         senddata("*200*3*5*1*3*1#",'1*{}#'.format(num),'IMRVF5SJ3AVNOG5GC278','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn')
                                         status = 'successful'

                                    elif float(plan.plan_size) == 1.0:

                                         senddata("*200*3*5*1*4*1#",'1*{}#'.format(num),'IMRVF5SJ3AVNOG5GC278','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn')
                                         status = 'successful'

                                    elif float(plan.plan_size) == 2000.0:

                                         senddata("*200*3*5*1*5*1#",'1*{}#'.format(num),'IMRVF5SJ3AVNOG5GC278','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn')
                                         status = 'successful'


                                    elif float(plan.plan_size) == 250.0:

                                         senddata("*200*3*5*1*6*1#",'1*{}#'.format(num),'IMRVF5SJ3AVNOG5GC278','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn')
                                         status = 'successful'


                                    elif float(plan.plan_size) == 500.0:

                                         senddata("*200*3*5*1*7*1#",'1*{}#'.format(num),'IMRVF5SJ3AVNOG5GC278','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn')
                                         status = 'successful'

                                    elif float(plan.plan_size) == 1.5:

                                         senddata("*200*3*5*1*8*1#",'1*{}#'.format(num),'IMRVF5SJ3AVNOG5GC278','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn')
                                         status = 'successful'


                                    elif float(plan.plan_size) == 2.0:

                                         senddata("*200*3*5*1*9*1#",'1*{}#'.format(num),'IMRVF5SJ3AVNOG5GC278','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn')
                                         status = 'successful'


                                    elif float(plan.plan_size) == 4.5:

                                          senddata("*200*3*5*2*1*1#",'1*{}#'.format(num),'IMRVF5SJ3AVNOG5GC278','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn')
                                          status = 'successful'

                                    elif float(plan.plan_size) == 11.0:


                                          senddata("*200*3*5*2*2*1#",'1*{}#'.format(num),'IMRVF5SJ3AVNOG5GC278','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn')
                                          status = 'successful'


                                    elif float(plan.plan_size) == 15.0:

                                          senddata("*200*3*5*2*3*1#",'1*{}#'.format(num),'IMRVF5SJ3AVNOG5GC278','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn')
                                          status = 'successful'


                                    elif float(plan.plan_size) == 40.0:

                                         senddata("*200*3*5*2*4*1#",'1*{}#'.format(num),'IMRVF5SJ3AVNOG5GC278','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn')
                                         status = 'successful'


                                    elif float(plan.plan_size) == 75.0:

                                          senddata("*200*3*5*2*5*1#",'1*{}#'.format(num),'IMRVF5SJ3AVNOG5GC278','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn')
                                          status = 'successful'

                                    else:

                                                def senddata(ussd,servercode,token,mytype):
                                                    payload={
                                                        'ussd':ussd,
                                                        # 'multistep':num,
                                                        'servercode': servercode,
                                                        'token': token,
                                                        'type':mytype


                                                            }

                                                    baseurl ='https://ussd.simhosting.ng/api/?'
                                                    response = requests.get(baseurl,params=payload,verify=False)
                                                    #print('..........................hello mojeed.........................')
                                                    #print(response)
                                                    #print('..........................hello mojeed.........................')
                                                    #print(payload)

                                                if float(plan.plan_size) == 3.0:

                                                     senddata("*229*2*3*{}#".format(num),'IMRVF5SJ3AVNOG5GC278','N1T8Wx7aHXeSzYhYVty5yUdQUqnUZhrfFp8TTnzH1uIcqUoIJn','USSD')
                                                     status = 'successful'

                                    # senddata(f"{ussd}",mobile_text.sim_host_server_id,'USSD')
                                    # senddata("*232#".format(num),mobile_text.sim_host_server_id,'USSD')
                                    # status = 'successful'

                            elif Network.objects.get(name=net).data_vending_medium == "UWS":

                                                    def create_id():
                                                            num = random.randint(1,10)
                                                            num_2 = random.randint(1,10)
                                                            num_3 = random.randint(1,10)
                                                            return str(num_2)+str(num_3)+str(uuid.uuid4())

                                                    ident = create_id()

                                                    while Data.objects.filter(ident= ident).exists():
                                                          ident = create_id()


                                                    url = "https://api.uws.com.ng/api/v1/sme_data/purchase"

                                                    payload = {
                                                        "phone" : num,
                                                        "network_id" : "4",
                                                        "plan_id" : str(plan.uws_plan_name_id),
                                                        "customRef" : ident
                                                    }

                                                    headers = {
                                                        'Content-Type': 'application/json',
                                                        'Accept': 'application/json',
                                                        'Authorization': f'Bearer {config.uws_token}'
                                                    }

                                                    response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
                                                    result = json.loads(response.text)
                                                    # print(result)
                                                    # print(response.status_code)

                                                    if result['status'] == "success":
                                                        status = 'successful'

                                                    elif result['status'] == "failed":
                                                        status = 'failed'

                                                    else:
                                                        status = 'processing'

                            elif Network.objects.get(name=net).data_vending_medium =='SMEPLUG':
                                            resp = senddatasmeplug("3",plan.smeplug_id,num)
                                            status = "successful"

                            elif Network.objects.get(name=net).data_vending_medium =='SMS':
                                    sendmessage('myweb', "{0} want to buy {1}{3}  9MOBILE-DATA data on {2} ".format(user.username, plan.plan_size, num, plan.plan_Volume), mobile_text.number, "02")


                            elif Network.objects.get(name=net).data_vending_medium  == "MSORG_DEVELOPED_WEBSITE":
                                        msorg_senddata(Network.objects.get(name=net).msorg_web_net_id,num,plan.plan_name_id)
                                        status = "successful"

                            elif Network.objects.get(name=net).data_vending_medium =='VTUAUTO':
                                    VTUAUTO_USSD(f"{ussd}",mobile_text.vtu_auto_device_id,mobile_text.vtu_sim_slot)
                                    VTUAUTO_USSD("*232#".format(num),mobile_text.vtu_auto_device_id,mobile_text.vtu_sim_slot)
                                    status = 'successful'

                            elif Network.objects.get(name=net).data_vending_medium =='MSPLUG':
                                   Msplug_Data_vending(net,plan.msplug_plan_name_id,num,mobile_text.msplug_sim_slot,"USSD",mobile_text.msplug_device_id)
                                   status = 'successful'

                            elif Network.objects.get(name=net).data_vending_medium =='SMEIFY':
                                        senddatasmeify("ETISALAT",plan.smeify_plan_name_id,num,plan.month_validate)
                                        status = 'successful'





            elif net == 'SMILE':

                def create_id():
                    num = random.randint(1, 10)
                    num_2 = random.randint(1, 10)
                    num_3 = random.randint(1, 10)
                    return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]

                ident = create_id()

                payload = {"billersCode": num, "serviceID": "smile-direct", "request_id": ident,"amount": plan.plan_amount, "variation_code": plan.vtpass_vairiation_code, "phone": num}
                authentication = (f'{config.vtpass_email}', f'{config.vtpass_password}')

                resp = requests.post( "https://vtpass.com/api/pay", data=payload, auth=authentication)
                #print(resp.text)
                status = 'successful'

            serializer.save(Status=status, ident=ident, plan_amount=amount, medium='API',balance_before=previous_bal, balance_after=(previous_bal - amount))

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# airtime topup api

class AirtimeTopupAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, format=None):
        try:
            item = AirtimeTopup.objects.filter(user=request.user).get(pk=id)
            serializer = AirtimeTopupSerializer(item)
            return Response(serializer.data)
        except AirtimeTopup.DoesNotExist:
            return Response(status=404)


class AirtimeTopupAPIListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        items = AirtimeTopup.objects.filter(
            user=request.user).order_by('-create_date')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = AirtimeTopupSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        status = "processing"
        fund = 0
        serializer = AirtimeTopupSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            order_username = (serializer.validated_data["user"]).username
            num = serializer.validated_data["mobile_number"]
            amt = serializer.validated_data["amount"]
            net = str(serializer.validated_data["network"])
            order_user = (serializer.validated_data["user"])
            user = serializer.validated_data["user"]
            previous_bal = order_user.Account_Balance
            airtime_type = (serializer.validated_data["airtime_type"])
            errors = {}

            def create_id():
                num = random.randint(1, 10)
                num_2 = random.randint(1, 10)
                num_3 = random.randint(1, 10)
                return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]

            ident = create_id()

            if user.user_type == "Affilliate":
                perc = TopupPercentage.objects.get(
                    network=Network.objects.get(name=net)).Affilliate_percent
                perc2 = TopupPercentage.objects.get(
                    network=Network.objects.get(name=net)).share_n_sell_affilliate_percent

            elif user.user_type == "API":
                perc = TopupPercentage.objects.get(
                    network=Network.objects.get(name=net)).api_percent
                perc2 = TopupPercentage.objects.get(
                    network=Network.objects.get(name=net)).share_n_sell_api_percent

            elif user.user_type == "TopUser":

                perc = TopupPercentage.objects.get(
                    network=Network.objects.get(name=net)).topuser_percent
                perc2 = TopupPercentage.objects.get(
                    network=Network.objects.get(name=net)).share_n_sell_topuser_percent
            else:
                perc = TopupPercentage.objects.get(
                    network=Network.objects.get(name=net)).percent
                perc2 = TopupPercentage.objects.get(
                    network=Network.objects.get(name=net)).share_n_sell_percent


            def senddata(ussd,servercode,mytype):
                    payload={
                        'ussd':ussd,
                        'servercode': servercode,
                        'token': f"{config.simhost_API_key}",
                        'type':mytype
                    }

                    baseurl ='https://ussd.simhosting.ng/api/?'
                    response = requests.get(baseurl,params=payload,verify=False)



            def VTUAUTO_USSD(ussd,device_id,sim):
                    payload = {
                            "device_id":device_id,
                            "ussd_string":ussd,
                            "sim":sim}
                    response = requests.post("https://vtuauto.ng/api/v1/request/ussd", auth=HTTPBasicAuth(f'{config.vtu_auto_email}', f'{config.vtu_auto_password}'), data=payload)
                    #print(response.text)


            def sendairtime(net,num,amount):
                        url = "https://smeplug.ng/api/v1/vtu"

                        payload = json.dumps({"network_id": net,"amount":amount,"phone_number": num})

                        headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {config.sme_plug_secret_key}'
                        }

                        #print(payload)
                        response = requests.request("POST", url, headers=headers, data = payload)
                        #print(response.text)
                        return response



            def sendairtimeVtpass(net, amount, num):
                authentication = (f'{config.vtpass_email}', f'{config.vtpass_password}')

                payload = {"serviceID": net, "request_id": ident,
                           "amount": amount, "phone": num}

                response = requests.post(
                    "https://vtpass.com/api/pay", data=payload, auth=authentication)
                #print(response.text)
                return response.text

            def Msplug_AIRTIME_vending(net,amt,num,sim,rtype,device_id):
                        url = "https://www.msplug.com/api/buy-data/"
                        payload = {"network":net,
                                    "amount": str(amt),
                                    "phone":num,
                                    "device_id":device_id,
                                    "sim_slot":sim,
                                    "airtime_type":rtype,
                                    "webhook_url":"http://www.fastlink.com.ng/buydata/webhook/"
                                    }
                        headers = {
                        'Authorization': f'Token {config.msplug_API_key}',
                        'Content-Type': 'application/json'
                        }

                        response = requests.post(url, headers=headers, data = json.dumps(payload))
                        #print(response.text)

            def sendairtimesmeify(net,amt,num):
                    headers = { 'Content-Type': 'application/json', 'Authorization': f'Bearer {SmeifyAuth.objects.first().get_token()}'}
                    url = f"https://auto.smeify.com/api/v1/online/vtu?network={net}&&amount={amt}&&phone={num}"
                    respons = requests.request("POST", url, headers=headers)

                    #print(respons.text)

            def msorg_sendairtime(netid,num,amt):

                    url = f"{config.msorg_web_url}/api/topup/"

                    headers = {
                    'Content-Type':'application/json',
                    'Authorization': f'Token {config.msorg_web_api_key}'
                    }
                    param = {"network": netid,"mobile_number": num,"amount":amt,"Ported_number":True,"airtime_type":"VTU"}
                    param_data = json.dumps(param)
                    response = requests.post(url, headers=headers, data=param_data, verify=False)
                    #print(response.text)
                    return response

            #print('')

            if airtime_type == "VTU":
                amount = float(amt) * int(perc)/100
                check = user.withdraw(user.id, amount)
                if check == False:
                    errors['error'] = u' insufficient balance '
                    raise serializers.ValidationError(errors)
                fund = amount
                Wallet_summary.objects.create(user=order_user, product="{} {} Airtime VTU topup  with {} ".format(net, amt, num), amount=fund, previous_balance=previous_bal, after_balance=(previous_bal - amount))





                amt = int(amt)
                if net == 'MTN':
                        mtn_text = SME_text.objects.get(network=Network.objects.get(name='MTN'))

                        if Network.objects.get(name=net).vtu_vending_medium ==  "SIMHOST":
                            # senddata(f"*456*1*2*{amt}*{num}*1*{mtn_text.vtu_pin}#" ,mtn_text.sim_host_server_id,'USSD')
                            senddata("*456*1*2*{0}*{1}*1*1234#".format(amt,num),'PUFCNGWH94E33HZJ23AQ','USSD')
                            status = 'successful'

                        elif Network.objects.get(name=net).vtu_vending_medium =='SMEPLUG':
                            sendairtime('1',num,amt)
                            status = "successful"

                        elif Network.objects.get(name=net).vtu_vending_medium =='SMS':
                            sendmessage('myweb',f"{user.username} want to buy  {amt} NAIRA  MTN-TOPUP  to {num} ",mtn_text.number,"02")

                        elif Network.objects.get(name=net).vtu_vending_medium =='VTUAUTO':

                             VTUAUTO_USSD(f"*456*1*2*{amt}*{num}*1*{mtn_text.vtu_pin}#",mtn_text.vtu_auto_device_id ,mtn_text.vtu_sim_slot)
                             status = 'successful'
                        elif Network.objects.get(name=net).vtu_vending_medium =='VTPASS':
                             sendairtimeVtpass("mtn",amt,num)
                             status = 'successful'
                        elif Network.objects.get(name=net).vtu_vending_medium =='MSPLUG':
                             Msplug_AIRTIME_vending(net,amt,num,mtn_text.msplug_sim_slot,"VTU",mtn_text.msplug_device_id)
                             status = 'successful'
                        elif Network.objects.get(name=net).vtu_vending_medium =='SMEIFY':
                                sendairtimesmeify(net,amt,num)
                                status = 'successful'
                        elif Network.objects.get(name=net).vtu_vending_medium  == "MSORG_DEVELOPED_WEBSITE":
                                msorg_sendairtime(Network.objects.get(name=net).msorg_web_net_id,num,amt)
                                status = "successful"

                elif net == 'GLO':
                        glo_text = SME_text.objects.get(network=Network.objects.get(name='GLO'))

                        if Network.objects.get(name=net).vtu_vending_medium ==  "SIMHOST":
                            senddata("*202*2*{1}*{0}*2009*1#".format(amt,num),'PEA9M9IYOCDJKG5K2D94','USSD')
                            # senddata("*202*2*{1}*{0}*{2}#".format(amt,num,glo_text.vtu_pin),glo_text.sim_host_server_id,'USSD')
                            status = 'successful'

                        elif Network.objects.get(name=net).vtu_vending_medium =='SMEPLUG':
                            sendairtime('4',num,amt)
                            status = "successful"

                        elif Network.objects.get(name=net).vtu_vending_medium =='SMS':
                            sendmessage('myweb',f"{user.username} want to buy  {amt} NAIRA  GLO-TOPUP  to {num} ",glo_text.number,"02")

                        elif Network.objects.get(name=net).vtu_vending_medium =='VTUAUTO':

                             VTUAUTO_USSD(f"*202*2*{num}*{amt}*{glo_text.vtu_pin}*1#",glo_text.vtu_auto_device_id ,glo_text.vtu_sim_slot)
                             status = 'successful'
                        elif Network.objects.get(name=net).vtu_vending_medium =='VTPASS':
                             sendairtimeVtpass("glo",amt,num)
                             status = 'successful'
                        elif Network.objects.get(name=net).vtu_vending_medium =='MSPLUG':
                             Msplug_AIRTIME_vending(net,amt,num,glo_text.msplug_sim_slot,"VTU",glo_text.msplug_device_id)
                             status = 'successful'
                        elif Network.objects.get(name=net).vtu_vending_medium  == "MSORG_DEVELOPED_WEBSITE":
                                msorg_sendairtime(Network.objects.get(name=net).msorg_web_net_id,num,amt)
                                status = "successful"

                        elif Network.objects.get(name=net).vtu_vending_medium =='SMEIFY':
                                     sendairtimesmeify(net,amt,num)
                                     status = 'successful'


                elif net == 'AIRTEL':
                        airtel_text = SME_text.objects.get(network=Network.objects.get(name='AIRTEL'))

                        if Network.objects.get(name=net).vtu_vending_medium ==  "SIMHOST":
                            # senddata(f"*605*2*1*{num}*{amt}*{airtel_text.vtu_pin}#",airtel_text.sim_host_server_id,'USSD')
                            senddata("*605*2*1*{0}*{1}*9735#".format(num,amt),'8XCX4RX3MI9PFSGWJK87','USSD')
                            status = 'successful'

                        elif Network.objects.get(name=net).vtu_vending_medium =='SMEPLUG':
                            sendairtime('2',num,amt)
                            status = "successful"

                        elif Network.objects.get(name=net).vtu_vending_medium =='SMS':
                            sendmessage('myweb',f"{user.username} want to buy  {amt} NAIRA  AIRTEL-TOPUP  to {num} ",airtel_text.number,"02")

                        elif Network.objects.get(name=net).vtu_vending_medium =='VTUAUTO':

                             VTUAUTO_USSD(f"*605*2*1*{num}*{amt}*{airtel_text.vtu_pin}#",airtel_text.vtu_auto_device_id ,airtel_text.vtu_sim_slot)
                             status = 'successful'
                        elif Network.objects.get(name=net).vtu_vending_medium =='VTPASS':
                             sendairtimeVtpass("airtel",amt,num)
                             status = 'successful'
                        elif Network.objects.get(name=net).vtu_vending_medium =='MSPLUG':
                             Msplug_AIRTIME_vending(net,amt,num,airtel_text.msplug_sim_slot,"VTU",airtel_text.msplug_device_id)
                             status = 'successful'

                        elif Network.objects.get(name=net).vtu_vending_medium =='SMEIFY':
                                     sendairtimesmeify(net,amt,num)
                                     status = 'successful'
                        elif Network.objects.get(name=net).vtu_vending_medium  == "MSORG_DEVELOPED_WEBSITE":
                                msorg_sendairtime(Network.objects.get(name=net).msorg_web_net_id,num,amt)
                                status = "successful"

                elif net == '9MOBILE':
                        mobile_text = SME_text.objects.get(network=Network.objects.get(name='9MOBILE'))

                        if Network.objects.get(name=net).vtu_vending_medium ==  "SIMHOST":
                            senddata(f"*224*{amt}*{num}*{mobile_text.vtu_pin}#",mobile_text.sim_host_server_id,'USSD')
                            status = 'successful'

                        elif Network.objects.get(name=net).vtu_vending_medium =='SMEPLUG':
                            sendairtime('3',num,amt)
                            status = "successful"

                        elif Network.objects.get(name=net).vtu_vending_medium =='SMS':
                            sendmessage('myweb',f"{user.username} want to buy  {amt} NAIRA  9MOBILE-TOPUP  to {num} ",mobile_text.number,"02")

                        elif Network.objects.get(name=net).vtu_vending_medium =='VTUAUTO':

                             VTUAUTO_USSD(f"*224*{amt}*{num}*{mobile_text.vtu_pin}#",mobile_text.vtu_auto_device_id ,mobile_text.vtu_sim_slot)
                             status = 'successful'
                        elif Network.objects.get(name=net).vtu_vending_medium =='VTPASS':
                             sendairtimeVtpass("etisalat",amt,num)
                             status = 'successful'
                        elif Network.objects.get(name=net).vtu_vending_medium =='MSPLUG':
                             Msplug_AIRTIME_vending(net,amt,num,mobile_text.msplug_sim_slot,"VTU",mobile_text.msplug_device_id)
                             status = 'successful'

                        elif Network.objects.get(name=net).vtu_vending_medium =='SMEIFY':
                                     sendairtimesmeify("ETISALAT",amt,num)
                                     status = 'successful'
                        elif Network.objects.get(name=net).vtu_vending_medium  == "MSORG_DEVELOPED_WEBSITE":
                                msorg_sendairtime(Network.objects.get(name=net).msorg_web_net_id,num,amt)
                                status = "successful"

            else:
                #print(Network.objects.get(name=net).share_and_sell_vending_medium)
                def msorg_sendairtime2(netid,num,amt):

                            url = f"{config.msorg_web_url}/api/topup/"

                            headers = {
                            'Content-Type':'application/json',
                            'Authorization': f'Token {config.msorg_web_api_key}'
                            }
                            param = {"network": netid,"mobile_number": num,"amount":amt,"Ported_number":True,"airtime_type":"Share and Sell"}
                            param_data = json.dumps(param)
                            response = requests.post(url, headers=headers, data=param_data, verify=False)
                            #print(response.text)
                            return response

                def sendairtimesmeify(net,amt,num):
                    headers = { 'Content-Type': 'application/json', 'Authorization': f'Bearer {SmeifyAuth.objects.first().get_token()}'}
                    url = f"https://auto.smeify.com/api/v1/online/sas?network={net}&&amount={amt}&&phone={num}"
                    respons = requests.request("POST", url, headers=headers)
                    #print(respons.text)


                amount = float(amt) * int(perc2)/100
                check = user.withdraw(user.id, amount)
                if check == False:
                    errors['error'] = u'Y insufficient balance '
                    raise serializers.ValidationError(errors)

                fund = amount
                Wallet_summary.objects.create(user=order_user, product="{} {} Airtime share and sell topup  with {} ".format(
                    net, amt, num), amount=fund, previous_balance=previous_bal, after_balance=(previous_bal - amount))

                amt = int(amt)
                if net == 'MTN':
                    mtn_text = SME_text.objects.get(network=Network.objects.get(name='MTN'))

                    if Network.objects.get(name=net).share_and_sell_vending_medium ==  "SIMHOST":
                            #  senddata(f"*600*{num}*{amt}*{mtn_text.share_and_sell_pin}#", mtn_text.sim_host_server_id, 'USSD')
                             senddata(f"*600*{num}*{amt}*9735#", 'PU7KFKHP9RZKY75XQ4H4', 'USSD')
                             status = 'successful'
                    elif Network.objects.get(name=net).share_and_sell_vending_medium =='VTUAUTO':
                             VTUAUTO_USSD(f"*600*{num}*{amt}*{mtn_text.share_and_sell_pin}#",mtn_text.vtu_auto_device_id ,mtn_text.vtu_sim_slot)
                             status = 'successful'

                    elif Network.objects.get(name=net).share_and_sell_vending_medium =='SMS':
                            sendmessage('myweb',f"{user.username} want to buy  {amt} NAIRA  MTN-SHARE AND SELL  to {num} ",mtn_text.number,"02")

                    elif Network.objects.get(name=net).share_and_sell_vending_medium =='MSPLUG':
                             Msplug_AIRTIME_vending(net,amt,num,mtn_text.msplug_sim_slot,"SNS",mtn_text.msplug_device_id)
                             status = 'successful'
                    elif Network.objects.get(name=net).share_and_sell_vending_medium == "MSORG_DEVELOPED_WEBSITE":
                                msorg_sendairtime2(Network.objects.get(name=net).msorg_web_net_id,num,amt)
                                status = "successful"

                    elif Network.objects.get(name=net).share_and_sell_vending_medium =='SMEIFY':
                                     sendairtimesmeify("MTN",amt,num)
                                     status = 'successful'

                    else:
                        errors['error'] = u'Share and sell not available on this network'
                        raise serializers.ValidationError(errors)

                elif net == 'AIRTEL':
                    airtel_text = SME_text.objects.get(network=Network.objects.get(name='AIRTEL'))

                    if Network.objects.get(name=net).share_and_sell_vending_medium ==  "SIMHOST":
                             senddata(f"*432*1*{num}*{amt}*{airtel_text.share_and_sell_pin}#", airtel_text.sim_host_server_id, 'USSD')
                             status = 'successful'
                    elif Network.objects.get(name=net).share_and_sell_vending_medium =='VTUAUTO':
                             VTUAUTO_USSD(f"*432*1*{num}*{amt}*{airtel_text.share_and_sell_pin}#",airtel_text.vtu_auto_device_id ,airtel_text.vtu_sim_slot)
                             status = 'successful'
                    elif Network.objects.get(name=net).share_and_sell_vending_medium =='SMS':
                            sendmessage('myweb',f"{user.username} want to buy  {amt} NAIRA  AIRTEL-SHARE AND SELL  to {num} ",mtn_text.number,"02")

                    elif Network.objects.get(name=net).share_and_sell_vending_medium =='MSPLUG':
                             Msplug_AIRTIME_vending(net,amt,num,airtel_text.msplug_sim_slot,"SNS",airtel_text.msplug_device_id)
                             status = 'successful'
                    elif Network.objects.get(name=net).share_and_sell_vending_medium == "MSORG_DEVELOPED_WEBSITE":
                                msorg_sendairtime2(Network.objects.get(name=net).msorg_web_net_id,num,amt)
                                status = "successful"

                    elif Network.objects.get(name=net).share_and_sell_vending_medium =='SMEIFY':
                                     sendairtimesmeify("AIRTEL",amt,num)
                                     status = 'successful'
                    else:
                        errors['error'] = u'Share and sell not available on this network'
                        raise serializers.ValidationError(errors)


                elif net == '9MOBILE':
                    mobile_text = SME_text.objects.get(
                        network=Network.objects.get(name='9MOBILE'))

                    if Network.objects.get(name=net).share_and_sell_vending_medium ==  "SIMHOST":
                             senddata(f"*223*{mobile_text.share_and_sell_pin}*{amt}*{num}*#", mobile_text.sim_host_server_id, 'USSD')
                             status = 'successful'
                    elif Network.objects.get(name=net).share_and_sell_vending_medium =='VTUAUTO':
                             VTUAUTO_USSD(f"*223*{mobile_text.share_and_sell_pin}*{amt}*{num}*#",mobile_text.vtu_auto_device_id ,mobile_text.vtu_sim_slot)
                             status = 'successful'
                    elif Network.objects.get(name=net).share_and_sell_vending_medium =='SMS':
                            sendmessage('myweb',f"{user.username} want to buy  {amt} NAIRA  9MOBILE-SHARE AND SELL  to {num} ",mtn_text.number,"02")


                    elif Network.objects.get(name=net).share_and_sell_vending_medium =='MSPLUG':
                             Msplug_AIRTIME_vending(net,amt,num,mobile_text.msplug_sim_slot,"SNS",mobile_text.msplug_device_id)
                             status = 'successful'
                    elif Network.objects.get(name=net).share_and_sell_vending_medium  == "MSORG_DEVELOPED_WEBSITE":
                                msorg_sendairtime2(Network.objects.get(name=net).msorg_web_net_id,num,amt)
                                status = "successful"

                    elif Network.objects.get(name=net).share_and_sell_vending_medium =='SMEIFY':
                                     sendairtimesmeify("ETISALAT",amt,num)
                                     status = 'successful'
                    else:
                        errors['error'] = u'Share and sell not available on this network'
                        raise serializers.ValidationError(errors)


                elif net == 'GLO':
                    glo_text = SME_text.objects.get(network=Network.objects.get(name='GLO'))

                    if Network.objects.get(name=net).share_and_sell_vending_medium ==  "SIMHOST":
                             senddata(f"*131*{num}*{amt}*{glo_text.share_and_sell_pin}#", glo_text.sim_host_server_id, 'USSD')
                             status = 'successful'
                    elif Network.objects.get(name=net).share_and_sell_vending_medium =='VTUAUTO':
                             VTUAUTO_USSD(f"*131*{num}*{amt}*{glo_text.share_and_sell_pin}#",glo_text.vtu_auto_device_id ,glo_text.vtu_sim_slot)
                             status = 'successful'
                    elif Network.objects.get(name=net).share_and_sell_vending_medium =='SMS':
                            sendmessage('myweb',f"{user.username} want to buy  {amt} NAIRA   GLO-SHARE AND SELL  to {num} ",glo_text.number,"02")


                    elif Network.objects.get(name=net).share_and_sell_vending_medium =='MSPLUG':
                             Msplug_AIRTIME_vending(net,amt,num,glo_text.msplug_sim_slot,"SNS",glo_text.msplug_device_id)
                             status = 'successful'
                    elif Network.objects.get(name=net).share_and_sell_vending_medium == "MSORG_DEVELOPED_WEBSITE":
                                msorg_sendairtime2(Network.objects.get(name=net).msorg_web_net_id,num,amt)
                                status = "successful"

                    elif Network.objects.get(name=net).share_and_sell_vending_medium =='SMEIFY':
                                     sendairtimesmeify("GLO",amt,num)
                                     status = 'successful'
                    else:
                        errors['error'] = u'Share and sell not available on this network'
                        raise serializers.ValidationError(errors)

                else:

                    errors['error'] = u'Share and sell not available on this network currently'
                    raise serializers.ValidationError(errors)

            serializer.save(Status=status, ident=ident, paid_amount=fund, medium='API',balance_before=previous_bal, balance_after=(previous_bal - amount))

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)














# Cable subscriptions api

class CableSubAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, format=None):
        try:
            item = Cablesub.objects.filter(user=request.user).get(pk=id)
            serializer = CablesubSerializer(item)
            return Response(serializer.data)
        except Cablesub.DoesNotExist:
            return Response(status=404)

class CableSubAPIListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        items = Cablesub.objects.filter(user=request.user).order_by('-create_date')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = CablesubSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        status = "processing"
        fund = 0
        serializer = CablesubSerializer(data=request.data,context={'request': request})

        if serializer.is_valid():
                       user = (serializer.validated_data["user"])
                       cableplan = serializer.validated_data["cableplan"]
                       cable_name = serializer.validated_data["cablename"]
                       smart_card_number = serializer.validated_data["smart_card_number"]
                       previous_bal = user.Account_Balance
                       plan_amount = float(cableplan.plan_amount)
                       errors = {}

                       service = ServicesCharge.objects.get(service = "Cablesub")

                       if service.charge > 0.0 :
                            amount = plan_amount + service.charge

                       elif service.discount > 0.0 :
                            amount = plan_amount - (plan_amount * service.discount/100)

                       else:
                           amount = plan_amount

                       if str(cable_name) == 'DSTV':

                                        def create_id():
                                            num = random.randint(1,10)
                                            num_2 = random.randint(1,10)
                                            num_3 = random.randint(1,10)
                                            return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]
                                        ident = create_id()
                                        url = "https://www.api.ringo.ng/api/agent/p2"
                                        payload = {
                                                "serviceCode" : "P-TV",
                                                "type" : "DSTV",
                                                "smartCardNo" : smart_card_number,
                                                "name" : cableplan.package,
                                                "code": cableplan.product_code,
                                                "period": "1",
                                                "request_id": ident,
                                                "hasAddon" : str(cableplan.hasAddon),
                                                "addondetails": {
                                                    "name" : cableplan.Addon_name,
                                                    "addoncode" : cableplan.addoncode
                                                }
                                        }


                                        headers = {'email': 'usmanreal43@gmail.com','password': 'Hafsayn20','Content-Type': 'application/json'  }


                                        # try:

                                        check = user.withdraw(user.id, amount)

                                        if check == False:
                                             errors['error'] = u'Insufficient Fund'
                                             raise serializers.ValidationError(errors)

                                        Wallet_summary.objects.create(user= user, product="{}  N{} Cable tv Sub with {} ".format(str(cableplan.package) + str(cableplan.Addon_name), amount,smart_card_number), amount = amount, previous_balance = previous_bal, after_balance= (previous_bal - amount))

                                        response = requests.request("POST", url, headers=headers, data = json.dumps(payload),verify=False)
                                        #print(f' ')
                                        #print(f'response = {response.text}')
                                        #print("hello mojeed am going to ringo")
                                        #print("payload", payload)
                                        status = 'successful'

                                        # except:
                                            # pass




                       elif str(cable_name) == 'GOTV':

                                        def create_id():
                                                    num = random.randint(1,10)
                                                    num_2 = random.randint(1,10)
                                                    num_3 = random.randint(1,10)
                                                    return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]
                                        ident = create_id()
                                        url = "https://www.api.ringo.ng/api/agent/p2"
                                        payload = {
                                                "serviceCode" : "P-TV",
                                                "type" : "GOTV",
                                                "smartCardNo" : smart_card_number,
                                                "name" : cableplan.package,
                                                "code": cableplan.product_code,
                                                "period": "1",
                                                "request_id": ident,

                                                }


                                        headers = {'email': 'usmanreal43@gmail.com','password': 'Hafsayn20','Content-Type': 'application/json' }


                                        # try:

                                        check = user.withdraw(user.id, amount)

                                        if check == False:
                                             errors['error'] = u'Insufficient Fund'
                                             raise serializers.ValidationError(errors)
                                        Wallet_summary.objects.create(user= user, product="{}  N{} Cable tv Sub with {} ".format(cableplan.package, amount,smart_card_number), amount = amount, previous_balance = previous_bal, after_balance= (previous_bal - amount))

                                        response = requests.request("POST", url, headers=headers, data = json.dumps(payload),verify=False)
                                        #print(f' ')
                                        #print(f'response = {response.text}')
                                        status = 'successful'

                                        # except:
                                        #         pass


                       elif str(cable_name) == 'STARTIME':

                                        def create_id():
                                                    num = random.randint(1,10)
                                                    num_2 = random.randint(1,10)
                                                    num_3 = random.randint(1,10)
                                                    return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]
                                        ident = create_id()
                                        url = "https://www.api.ringo.ng/api/agent/p2"
                                        payload = {
                                                "serviceCode" : "P-TV",
                                                "type" : "STARTIMES",
                                                "smartCardNo" : smart_card_number,
                                                "price" : cableplan.plan_amount,
                                                  "request_id": ident,

                                                }



                                        headers = {'email': 'usmanreal43@gmail.com','password': 'Hafsayn20','Content-Type': 'application/json' }


                                        try:



                                                                check = user.withdraw(user.id, amount)

                                                                if check == False:
                                                                     errors['error'] = u'Insufficient Fund'
                                                                     raise serializers.ValidationError(errors)
                                                                Wallet_summary.objects.create(user= user, product="{}  N{} Cable tv Sub with {} ".format(cableplan.package, amount,smart_card_number), amount = amount, previous_balance = previous_bal, after_balance= (previous_bal - amount))

                                                                response = requests.request("POST", url, headers=headers, data = json.dumps(payload),verify=False)
                                                                status = 'successful'

                                        except:
                                                        pass


                       serializer.save(Status = status, ident=ident , balance_before = previous_bal, balance_after =(previous_bal - amount),plan_amount= amount)

                       return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
##################################################################################
# class CableSubAPIListView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request, format=None):
#         items = Cablesub.objects.filter(
#             user=request.user).order_by('-create_date')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CablesubSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         status = "processing"
#         fund = 0
#         serializer = CablesubSerializer(
#             data=request.data, context={'request': request})

#         if serializer.is_valid():
#             user = (serializer.validated_data["user"])
#             cableplan = serializer.validated_data["cableplan"]
#             cable_name = serializer.validated_data["cablename"]
#             smart_card_number = serializer.validated_data["smart_card_number"]
#             previous_bal = user.Account_Balance
#             plan_amount = float(cableplan.plan_amount)
#             errors = {}

#             service = ServicesCharge.objects.get(service="Cablesub")

#             if user.user_type == "Affilliate":
#                 if service.Affilliate_charge > 0.0:
#                     amount = float(plan_amount) +  float(service.Affilliate_charge)

#                 elif service.Affilliate_discount > 0.0:
#                     amount = float(plan_amount) - (float(plan_amount) * service.Affilliate_discount/100)
#                 else:
#                     amount = float(plan_amount)

#             elif user.user_type == "TopUser":
#                 if service.topuser_charge > 0.0:
#                     amount = float(plan_amount) + float(service.topuser_charge)

#                 elif service.topuser_discount > 0.0:
#                     amount = float(plan_amount) - (float(plan_amount) * service.topuser_discount/100)
#                 else:
#                     amount = float(plan_amount)

#             elif user.user_type == "API":
#                 if service.api_charge > 0.0:
#                     amount = float(plan_amount) + float(service.api_charge)

#                 elif service.api_discount > 0.0:
#                     amount = float(plan_amount) - (float(plan_amount) * service.api_discount/100)

#                 else:
#                     amount = float(plan_amount)
#             else:

#                 if service.charge > 0.0:
#                     amount = float(plan_amount) + float(service.charge)

#                 elif service.discount > 0.0:
#                     amount = float(plan_amount) -  (float(plan_amount) * service.discount/100)

#                 else:
#                     amount = float(plan_amount)



#             if str(cable_name) == 'DSTV':

#                 def create_id():
#                     num = random.randint(1, 10)
#                     num_2 = random.randint(1, 10)
#                     num_3 = random.randint(1, 10)
#                     return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]
#                 ident = create_id()
#                 authentication = (f'{config.vtpass_email}',
#                                   f'{config.vtpass_password}')

#                 payload = {"billersCode": smart_card_number, "serviceID": "dstv",
#                           "request_id": ident, "variation_code": cableplan.product_code, "phone": user.Phone}

#                 try:

#                     check = user.withdraw(user.id, amount)
#                     if check == False:
#                         errors['error'] = u'Y insufficient balance '
#                         raise serializers.ValidationError(errors)

#                     Wallet_summary.objects.create(user= user, product="{}  N{} Cable tv Sub with {} ".format(cableplan.package, amount,smart_card_number), amount = amount, previous_balance = previous_bal, after_balance= (previous_bal - amount))
#                     resp = requests.post("https://vtpass.com/api/pay", data=payload, auth=authentication)
#                     status = 'successful'

#                 except:
#                     pass

#             elif str(cable_name) == 'GOTV':

#                 def create_id():
#                     num = random.randint(1, 10)
#                     num_2 = random.randint(1, 10)
#                     num_3 = random.randint(1, 10)
#                     return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]
#                 ident = create_id()
#                 authentication = (f'{config.vtpass_email}',
#                                   f'{config.vtpass_password}')

#                 payload = {"billersCode": smart_card_number, "serviceID": "gotv",
#                           "request_id": ident, "variation_code": cableplan.product_code, "phone": user.Phone}

#                 try:

#                     check = user.withdraw(user.id, amount)
#                     if check == False:
#                         errors['error'] = u' insufficient balance '
#                         raise serializers.ValidationError(errors)
#                     Wallet_summary.objects.create(user= user, product="{}  N{} Cable tv Sub with {} ".format(cableplan.package, amount,smart_card_number), amount = amount, previous_balance = previous_bal, after_balance= (previous_bal - amount))
#                     resp = requests.post("https://vtpass.com/api/pay", data=payload, auth=authentication)
#                     status = 'successful'

#                 except:
#                     pass

#             elif str(cable_name) == 'STARTIME':

#                 def create_id():
#                     num = random.randint(1, 10)
#                     num_2 = random.randint(1, 10)
#                     num_3 = random.randint(1, 10)
#                     return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]
#                 ident = create_id()
#                 authentication = (f'{config.vtpass_email}',
#                                   f'{config.vtpass_password}')

#                 payload = {"billersCode": smart_card_number, "serviceID": "startimes",
#                           "request_id": ident, "variation_code": cableplan.product_code, "phone": user.Phone}

#                 try:

#                     check = user.withdraw(user.id, amount)
#                     if check == False:
#                         errors['error'] = u'Y insufficient balance '
#                         raise serializers.ValidationError(errors)
#                     Wallet_summary.objects.create(user= user, product="{}  N{} Cable tv Sub with {} ".format(cableplan.package, amount,smart_card_number), amount = amount, previous_balance = previous_bal, after_balance= (previous_bal - amount))
#                     resp = requests.post("https://vtpass.com/api/pay", data=payload, auth=authentication)
#                     status = 'successful'

#                 except:
#                     pass

#             serializer.save(Status=status, ident=ident, balance_before=previous_bal, balance_after=(
#                 previous_bal - amount), plan_amount=amount)

#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


class ValidateIUCAPIView(APIView):


    def get(self,request):
        iuc = request.GET.get('smart_card_number', None)
        cable_id = request.GET.get('cablename', None)
        if cable_id == "DSTV":
            data = {"billersCode": iuc, "serviceID": "dstv"}

        elif cable_id == 'GOTV':
            data = {"billersCode": iuc, "serviceID": "gotv"}

        elif cable_id == "STARTIME":
            data = {"billersCode": iuc, "serviceID": "startimes"}

        invalid = False
        authentication = (f'{config.vtpass_email}',
                          f'{config.vtpass_password}')

        resp = requests.post(
            "https://vtpass.com/api/merchant-verify", data=data, auth=authentication)
        ##print(resp.text)
        res = json.loads(resp.text)
        dat = res['content']
        if 'Customer_Name' in dat:
            name = res['content']['Customer_Name']
        else:
            invalid = True
            name = "INVALID IUC/SMARTCARD"

        data = {
            'invalid': invalid,
            'name': name
        }

        return Response(data)


class ValidateMeterAPIView(APIView):


    def get(self, request):

        meternumber = request.GET.get('meternumber', None)
        disconame = request.GET.get('disconame', None)
        mtype = request.GET.get('mtype', None)

        disconame = Disco_provider_name.objects.get(id=disconame).name
        ##print(meternumber, disconame, mtype)

        if disconame == "Ikeja Electric":
            disconame = "ikeja-electric"

        elif disconame == 'Eko Electric':
            disconame = "eko-electric"

        elif disconame == "Kaduna Electric":
            disconame = "kaduna-electric"

        elif disconame == "Port Harcourt Electric":
            disconame = "portharcourt-electric"

        elif disconame == "Jos Electric":
            disconame = "jos-electric"

        elif disconame == "Ibadan Electric":
            disconame = "ibadan-electric"

        elif disconame == "Kano Electric":
            disconame = "kano-electric"

        elif disconame == "Abuja Electric":
            disconame = "abuja-electric"

        data = {"billersCode": meternumber,
                "serviceID": disconame, "type": mtype}
        invalid = False
        authentication = (f'{config.vtpass_email}',
                          f'{config.vtpass_password}')

        resp = requests.post("https://vtpass.com/api/merchant-verify", data=data, auth=authentication)
        ##print(resp.text)
        res = json.loads(resp.text)
        dat = res['content']
        if 'Customer_Name' in dat:
            name = res['content']['Customer_Name']
            address = res['content']["Address"]
        else:
            invalid = True
            name = "INVALID METER NUMBER"
            address = "INVALID METER NUMBER"

        data = {
            'invalid': invalid,
            'name': name,
            'address': address
        }

        return Response(data)


class BillPaymentAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, format=None):
        try:
            item = Billpayment.objects.filter(user=request.user).get(pk=id)
            serializer = BillpaymentSerializer(item)
            return Response(serializer.data)
        except Billpayment.DoesNotExist:
            return Response(status=404)

class BillPaymentAPIListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        items = Billpayment.objects.filter(user=request.user).order_by('-create_date')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = BillpaymentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        status = "processing"
        fund = 0
        serializer = BillpaymentSerializer(data=request.data,context={'request': request})

        if serializer.is_valid():
                        user = (serializer.validated_data["user"])
                        meter_number = serializer.validated_data["meter_number"]
                        mtype = serializer.validated_data["MeterType"]
                        disco_name = serializer.validated_data["disco_name"]
                        amount = serializer.validated_data["amount"]
                        number = serializer.validated_data["Customer_Phone"]
                        previous_bal = user.Account_Balance
                        token = ""
                        errors = {}



                        service = ServicesCharge.objects.get(service = "Bill")

                        if service.charge > 0.0 :
                               paid_amount = float(amount) + float(service.charge)

                        elif service.discount > 0.0 :
                            paid_amount = float(amount) - (float(amount) * service.discount/100)

                        else:
                            paid_amount = float(amount)

                        def create_id():
                            num = random.randint(1,10)
                            num_2 = random.randint(1,10)
                            num_3 = random.randint(1,10)

                            return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]
                        ident = create_id()


                        check = user.withdraw(user.id, paid_amount)

                        if check == False:
                            errors['error'] = u'Y insufficient balance'
                            raise serializers.ValidationError(errors)


                        Wallet_summary.objects.create(user= user, product="{}  N{} Electricity Bill Payment  with {} ".format(disco_name.name, amount,meter_number), amount = paid_amount, previous_balance = previous_bal, after_balance= (previous_bal - paid_amount))


                        url = "https://www.api.ringo.ng/api/agent/p2"
                        payload = {
                                    "serviceCode" : "P-ELECT",
                                    "disco" : disco_name.p_id,
                                    "meterNo": meter_number,
                                    "type" :  mtype.upper(),
                                    "amount": amount,
                                    "phonenumber":number,
                                    "request_id" : ident
                                    }
                        headers = {'email': 'usmanreal43@gmail.com','password': 'Hafsayn20','Content-Type': 'application/json' }

                        #print(payload)
                        response = requests.post(url, headers=headers, data = json.dumps(payload))


                        try:
                            if response.status_code == 200 or response.status_code == 201:
                                a = json.loads(response.text)
                                status = 'successful'
                                token = a["token"]

                            else:
                                url = "https://www.api.ringo.ng//api/b2brequery"
                                payload = {'request_id': ident}
                                headers = {'email': 'usmanreal43@gmail.com','password': 'Hafsayn20','Content-Type': 'application/json' }
                                response = requests.post(url, headers=headers, data = json.dumps(payload))
                                #print(payload)
                                #print(response.text)
                                a = json.loads(response.text)
                                status = 'successful'
                                token = a["token"]

                        except:
                                pass

                        serializer.save(Status = status,token=token, ident=ident , balance_before = previous_bal, balance_after =(previous_bal - float(amount)),paid_amount= paid_amount)

                        return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# class BillPaymentAPIListView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request, format=None):
#         items = Billpayment.objects.filter(
#             user=request.user).order_by('-create_date')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = BillpaymentSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         status = "processing"
#         fund = 0
#         serializer = BillpaymentSerializer(
#             data=request.data, context={'request': request})

#         if serializer.is_valid():
#             user = (serializer.validated_data["user"])
#             meter_number = serializer.validated_data["meter_number"]
#             mtype = serializer.validated_data["MeterType"]
#             disco_name = serializer.validated_data["disco_name"]
#             amount = serializer.validated_data["amount"]
#             number = serializer.validated_data["Customer_Phone"]
#             previous_bal = user.Account_Balance
#             token = ""
#             errors = {}

#             service = ServicesCharge.objects.get(service="Bill")

#             if user.user_type == "Affilliate":
#                 if service.Affilliate_charge > 0.0:
#                     paid_amount = float(amount) + float(service.Affilliate_charge)

#                 elif service.Affilliate_discount > 0.0:
#                     paid_amount = float(
#                         amount) - (float(amount) * service.Affilliate_discount/100)
#                 else:
#                     paid_amount = float(amount)

#             elif user.user_type == "TopUser":
#                 if service.topuser_charge > 0.0:
#                     paid_amount = float(amount) + float(service.topuser_charge)

#                 elif service.topuser_discount > 0.0:
#                     paid_amount = float(
#                         amount) - (float(amount) * service.topuser_discount/100)
#                 else:
#                     paid_amount = float(amount)

#             elif user.user_type == "API":
#                 if service.api_charge > 0.0:
#                     paid_amount = float(amount) + float(service.api_charge)

#                 elif service.api_discount > 0.0:
#                     paid_amount = float(
#                         amount) - (float(amount) * service.api_discount/100)

#                 else:
#                     paid_amount = float(amount)
#             else:

#                 if service.charge > 0.0:
#                     paid_amount = float(amount) + float(service.charge)

#                 elif service.discount > 0.0:
#                     paid_amount = float(amount) -(float(amount) * service.discount/100)

#                 else:
#                     paid_amount = float(amount)

#             def create_id():
#                 num = random.randint(1, 10)
#                 num_2 = random.randint(1, 10)
#                 num_3 = random.randint(1, 10)

#                 return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]
#             ident = create_id()

#             check = user.withdraw(user.id, paid_amount)
#             if check == False:
#                 errors['error'] = u'Y insufficient balance '
#                 raise serializers.ValidationError(errors)

#             Wallet_summary.objects.create(user=user, product="{}  N{} Electricity Bill Payment  with {} ".format(
#                 disco_name.name, amount, meter_number), amount=paid_amount, previous_balance=previous_bal, after_balance=(previous_bal - paid_amount))



#             if disco_name.name == "Ikeja Electric":
#                 disconame = "ikeja-electric"

#             elif disco_name.name == 'Eko Electric':
#                 disconame = "eko-electric"

#             elif disco_name.name == "Kaduna Electric":
#                 disconame = "kaduna-electric"

#             elif disco_name.name == "Port Harcourt Electric":
#                 disconame = "portharcourt-electric"

#             elif disco_name.name == "Jos Electric":
#                 disconame = "jos-electric"

#             elif disco_name.name == "Ibadan Electric":
#                 disconame = "ibadan-electric"

#             elif disco_name.name == "Kano Electric":
#                 disconame = "kano-electric"

#             elif disco_name.name == "Abuja Electric":
#                 disconame = "abuja-electric"

#             authentication = (f'{config.vtpass_email}',
#                               f'{config.vtpass_password}')

#             payload = {"billersCode": meter_number, "amount": amount, "serviceID": disconame,
#                       "request_id": ident, "variation_code": mtype, "phone": number, }

#             response = requests.post(
#                 "https://vtpass.com/api/pay", data=payload, auth=authentication)
#             #print(response.text)
#             try:
#                 if response.status_code == 200 or response.status_code == 201:
#                     status = 'successful'
#                     a = json.loads(response.text)
#                     token = a["purchased_code"]

#                 else:
#                     payload = {'request_id': ident}

#                     response = requests.post(
#                         "https://vtpass.com/api/requery", data=payload, auth=authentication)
#                     status = 'successful'
#                     a = json.loads(response.text)
#                     token = a["purchased_code"]

#             except:
#                 pass

#             serializer.save(Status=status, token=token, ident=ident, balance_before=previous_bal, balance_after=(
#                 previous_bal - float(amount)), paid_amount=paid_amount)

#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


class PINCCHECKAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        pin = request.GET.get('pin', None)
        #print(pin)
        #print(request.user.pin)

        if pin != str(request.user.pin):
            return Response({"error": "  Incorrect pin"}, status=400)

        else:
            data = {"message": "pin correct"}

        return Response(data, status=200)


class PINCHANGEAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        pin1 = request.GET.get('pin1', None)
        pin2 = request.GET.get('pin2', None)
        oldpin = request.GET.get('oldpin', None)
        #print(oldpin)
        #print(request.user.pin)
        if oldpin != str(request.user.pin):
            return Response({"error": "Old pin is incorrect"}, status=400)

        elif pin1 != pin2:
            return Response({"error": "Two Fields are not match"}, status=400)

        elif len(str(pin1)) > 5 or len(str(pin1)) < 5:
            return Response({"error": "Your pin must be 5 digit in length"}, status=400)

        elif len(str(pin2)) > 5 or len(str(pin2)) < 5:
            return Response({"error": "Your pin must be 5 digit in length"}, status=400)

        elif pin1.isdigit() != True and pin2.isdigit() != True:
            return Response({"error": "The pin must be Digit"}, status=400)

        elif oldpin == str(request.user.pin):
            return Response({"error": "The old pin must not be the same as the new pin"}, status=400)

        else:
            request.user.pin = pin1
            request.user.save()
            data = {"message": "pin Changed successfully"}

        return Response(data, status=200)


class PINRESETAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        pin1 = request.GET.get('pin1', None)
        pin2 = request.GET.get('pin2', None)
        password = request.GET.get('password', None)
        #print(password)
        #print(request.user.password)
        if not request.user.check_password(password):
            return Response({"error": "incorrect password"}, status=400)

        elif pin1 != pin2:
            return Response({"error": "pin1 and pin2  are not match"}, status=400)

        elif len(str(pin1)) > 5 or len(str(pin1)) < 5:
            return Response({"error": "Your pin must be 5 digit in length"}, status=400)

        elif len(str(pin2)) > 5 or len(str(pin2)) < 5:
            return Response({"error": "Your pin must be 5 digit in length"}, status=400)

        elif pin1.isdigit() != True and pin2.isdigit() != True:
            return Response({"error": "The pin must be Digit"}, status=400)

        else:
            request.user.pin = pin1
            request.user.save()
            data = {"message": "pin Reset successfully"}

        return Response(data, status=200)


class PINSETUPAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        pin1 = request.GET.get('pin1', None)
        pin2 = request.GET.get('pin2', None)

        if pin1 != pin2:
            return Response({"error": "Two Fields are not match"}, status=400)

        elif len(str(pin1)) > 5 or len(str(pin1)) < 5:
            return Response({"error": "Your pin must be 5 digit in length"}, status=400)

        elif len(str(pin2)) > 5 or len(str(pin2)) < 5:
            return Response({"error": "Your pin must be 5 digit in length"}, status=400)

        elif pin1.isdigit() != True and pin2.isdigit() != True:
            return Response({"error": "The pin must be Digit"}, status=400)

        else:
            request.user.pin = pin1
            request.user.save()
            data = {"message": "pin setup successfully"}

        return Response(data, status=200)


class CouponPaymentAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        items = CouponPayment.objects.filter(
            user=request.user).order_by('-create_date')
        serializer = CouponPaymentSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        status = "successful"
        fund = 0
        serializer = CouponPaymentSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            user = (serializer.validated_data["user"])
            Code = serializer.validated_data["Code"]

            if Couponcode.objects.filter(Coupon_Code=Code).exists():

                ms = Couponcode.objects.get(Coupon_Code=Code).amount
                amount = Couponcode.objects.get(Coupon_Code=Code).amount
                previous_bal1 = user.Account_Balance
                user.deposit(user.id, float(ms),False ,"Coupon payment from API")
                sta = Couponcode.objects.get(Coupon_Code=Code)
                sta.Used = True

                sta.save()
                Wallet_summary.objects.create(user=user, product="Coupon Payment  N{} ".format(
                    amount), amount=amount, previous_balance=previous_bal1, after_balance=(previous_bal1 - float(amount)))

            serializer.save(Status=status, amount=amount)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class Airtime_fundingAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        items = Airtime_funding.objects.filter(
            user=request.user).order_by('-create_date')
        serializer = Airtime_fundingSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        status = "pending"
        fund = 0
        serializer = Airtime_fundingSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            user = (serializer.validated_data["user"])
            network = (serializer.validated_data["network"])
            amount = (serializer.validated_data["amount"])
            number = (serializer.validated_data["mobile_number"])

            perc = Percentage.objects.get(
                network=Network.objects.get(name=network))
            Receivece_amount = float(amount) * int(perc.percent)/100

            def sendmessage(sender,message,to,route):
                   payload={
                     'sender':sender,
                     'to': to,
                     'message': message,
                     'type': '0',
                     'routing':route,
                     'token':'EGZ1zr8wYJUajiAcxrOsCkMfv0EaTnGsHGHLePhZjlnsDQnOfD',
                     'schedule':'',
                          }

                   url = "https://app.smartsmssolutions.ng/io/api/client/v1/sms/"
                   response = requests.post(url, params=payload, verify=False)
            # def sendmessage(sender, message, to, route):
            #     payload = {
            #         'sender': sender,
            #         'to': to,
            #         'message': message,
            #         'type': '0',
            #         'routing': route,
            #         'token': 'cYTj0CCFuGM4PSrvABkoANCBNlNF2SoipZFSNlz5hmKnejg6fubGLFu7Ph2URDj22dWGYjlRqDILQz7kHxARBlAwdC4CpTKHGC5D',
            #         'schedule': '',
            #     }

            #     baseurl = f'https://sms.hollatags.com/api/send/?user={config.hollatag_username}&pass={config.hollatag_password}&to={to}&from={sender}&msg={urllib.parse.quote(message)}'
            #     response = requests.get(baseurl, verify=False)

            sendmessage('Msorg', "{0} want to fund his/her account with  airtime transfer network: {1} amount:{2} Phone number:{3} https://www.Husmodata.com/page-not-found-error/page/vtuapp/Airtime_funding/".format(
                user.username, network, amount, number), '2348166171824', '03')

            serializer.save(Receivece_amount=Receivece_amount, AccountName=user.AccountName,
                            BankName=user.BankName, AccountNumber=user.AccountNumber)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class WithdrawAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        items = Withdraw.objects.filter(
            user=request.user).order_by('-create_date')
        serializer = WithdrawSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        status = "successful"
        fund = 0
        serializer = WithdrawSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            user = (serializer.validated_data["user"])
            amount = (serializer.validated_data["amount"])
            bankaccount = (serializer.validated_data['accountNumber'])
            name = (serializer.validated_data['accountName'])
            bankname = (serializer.validated_data['bankName'])
            errors = {}

            amt = float(amount) + 100

            def sendmessage(sender,message,to,route):
                   payload={
                     'sender':sender,
                     'to': to,
                     'message': message,
                     'type': '0',
                     'routing':route,
                     'token':'EGZ1zr8wYJUajiAcxrOsCkMfv0EaTnGsHGHLePhZjlnsDQnOfD',
                     'schedule':'',
                          }

                   url = "https://app.smartsmssolutions.ng/io/api/client/v1/sms/"
                   response = requests.post(url, params=payload, verify=False)
            # def sendmessage(sender, message, to, route):
            #     payload = {
            #         'sender': sender,
            #         'to': to,
            #         'message': message,
            #         'type': '0',
            #         'routing': route,
            #         'token': 'cYTj0CCFuGM4PSrvABkoANCBNlNF2SoipZFSNlz5hmKnejg6fubGLFu7Ph2URDj22dWGYjlRqDILQz7kHxARBlAwdC4CpTKHGC5D',
            #         'schedule': '',
            #     }

            #     baseurl = f'https://sms.hollatags.com/api/send/?user={config.hollatag_username}&pass={config.hollatag_password}&to={to}&from={sender}&msg={urllib.parse.quote(message)}'
            #     response = requests.get(baseurl, verify=False)

            previous_bal = user.Account_Balance

            check = user.withdraw(user.id, float(amt))
            if check == False:
                errors['error'] = u'Y insufficient balance '
                raise serializers.ValidationError(errors)
            Wallet_summary.objects.create(user=user, product="Withdraw   N{}  with N100 charge".format(
                amount), amount=amt, previous_balance=previous_bal, after_balance=(previous_bal - float(amt)))

            sendmessage('Husmodata', "{0} want to withdraw   amount:{1} to {2} {3} {4}   https://www.Husmodata.com/way/to/vtuapp/admin/app/withdraw/".format(
                user.username, amount, bankname, bankaccount, name), '2348162269770', '2')

            serializer.save(Status=status)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TransferAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        items = Transfer.objects.filter(
            user=request.user).order_by('-create_date')
        serializer = TransferSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        status = "successful"
        fund = 0
        serializer = TransferSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            user = (serializer.validated_data["user"])
            amount = (serializer.validated_data["amount"])
            receiver_username = (
                serializer.validated_data['receiver_username'])
            errors = {}

            mb_2 = CustomUser.objects.get(username__iexact=receiver_username)
            previous_bal1 = user.Account_Balance
            previous_bal2 = mb_2.Account_Balance

            check = user.withdraw(user.id, float(amount))
            if check == False:
                errors['error'] = u'Y insufficient balance '
                raise serializers.ValidationError(errors)

            mb_2.deposit(mb_2.id, float(amount),True ,"Wallet to Wallet from API")
            notify.send(mb_2, recipient=mb_2, verb='You Received sum of #{} from {} '.format(
                amount, user.username))

            Wallet_summary.objects.create(user=user, product="Transfer N{} to {}".format(
                amount, mb_2.username), amount=amount, previous_balance=previous_bal1, after_balance=(previous_bal1 - float(amount)))

            Wallet_summary.objects.create(user=mb_2, product="Received sum N{} from {}".format(
                amount, user.username), amount=amount, previous_balance=previous_bal2, after_balance=(previous_bal2 + float(amount)))

            serializer.save(Status=status, previous_balance=previous_bal1, after_balance=(
                previous_bal1 + float(amount)))

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class bonus_transferAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        items = bonus_transfer.objects.filter(
            user=request.user).order_by('-create_date')
        serializer = bonus_transferSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        status = "successful"
        fund = 0
        serializer = bonus_transferSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            user = (serializer.validated_data["user"])
            amount = (serializer.validated_data["amount"])

            previous_bal1 = user.Account_Balance

            user.ref_withdraw(float(amount))
            user.deposit(user.id, float(amount) ,True ,"Bonusto wallet from API")
            notify.send(user, recipient=user,
                        verb='#{} referer bonus has been added to your wallet,refer more people to get more bonus'.format(amount))

            Wallet_summary.objects.create(user=user, product="referer bonus to wallet N{} ".format(
                amount), amount=amount, previous_balance=previous_bal1, after_balance=(previous_bal1 - float(amount)))

            serializer.save(Status=status)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# whatappp bot


@require_POST
@csrf_exempt
def replybot(request):
    text1 = request.POST.get('Body')
    response = MessagingResponse()

    if not ("log_in" in request.session):
        request.session["log_in"] = False
        #print(request.session["log_in"], "ww2222")

    elif True:
        #print(request.session["log_in"], "ww223333333322")

        response.message(
            'Welcome to MsorgSMEBOT enter your username and password seperate with comma to start i.e musa,12345')
        #request.session["level"] = request.session["level"] + 1

        if not ',' in text1:
            #response = MessagingResponse()
            response.message(
                "Please enter your username and password seperate with comma to start i.e musa,12345")

        else:
            username = text1.split(',')[0]
            password = text1.split(',')[1]

            headers = {'Content-Type': 'application/json'}
            url = "https://www.IMCdata.com/rest-auth/login/"
            data = {"username": username, "password": password}
            c = requests.post(url, data=json.dumps(data), headers=headers)
            a = json.loads(c.text)

            if "key" in a:
                response = MessagingResponse()
                response.message("Login successful")
                request.session["log_in"] = True

                #request.session["log_in"] = True

            else:
                response = MessagingResponse()
                response.message("Unable to log in with provided credentials.")

    if request.session["log_in"] == True:
        #print(request.session["log_in"], "ww2233333tuyuyyu33322")

        response = MessagingResponse()
        response.message(
            'Welcome back {0}\n 1.Buy Data \n2.Buy Airtime \n3.Cable subscription \n4.Bill payment'.format(username))
        if text1 == "1":
            response = MessagingResponse()
            response.message("data")
        elif text1 == "2":
            response = MessagingResponse()
            response.message("airtime")
        elif text1 == "3":
            response = MessagingResponse()
            response.message("cable")
        elif text1 == "4":
            response = MessagingResponse()
            response.message("bill")

    return HttpResponse(response)


# Result_Checker_Pin_order api

class Result_Checker_Pin_orderAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, format=None):
        try:
            item = Result_Checker_Pin_order.objects.filter(
                user=request.user).get(pk=id)
            serializer = Result_Checker_Pin_orderSerializer(item)
            return Response(serializer.data)
        except Result_Checker_Pin_order.DoesNotExist:
            return Response(status=404)


# Result_Checker_Pin_order api

class Result_Checker_Pin_orderAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, format=None):
        try:
            item = Result_Checker_Pin_order.objects.filter(
                user=request.user).get(pk=id)
            serializer = Result_Checker_Pin_orderSerializer(item)
            return Response(serializer.data)
        except Result_Checker_Pin_order.DoesNotExist:
            return Response(status=404)


class Result_Checker_Pin_orderAPIListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        items = Result_Checker_Pin_order.objects.filter(
            user=request.user).order_by('-create_date')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = Result_Checker_Pin_orderSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        status = "processing"
        fund = 0
        serializer = Result_Checker_Pin_orderSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            order_username = (serializer.validated_data["user"]).username
            exam = serializer.validated_data["exam_name"]
            quantity = serializer.validated_data["quantity"]
            exam_name = exam
            errors = {}
            control = Result_Checker_Pin.objects.get(exam_name=exam)


            provider_amount = amount =control.provider_amount

            if request.user.user_type == "Affilliate":
                amount = Result_Checker_Pin.objects.get(
                    exam_name=exam).Affilliate_price

            elif request.user.user_type == "TopUser":
                amount = Result_Checker_Pin.objects.get(
                    exam_name=exam).TopUser_price

            elif request.user.user_type == "API":
                amount = Result_Checker_Pin.objects.get(
                    exam_name=exam).api_price
            else:
                amount = Result_Checker_Pin.objects.get(exam_name=exam).amount

            amt = amount * quantity
            user = (serializer.validated_data["user"])
            previous_bal = user.Account_Balance
            errors = {}
            data = {}

            def create_id():
                num = random.randint(1, 10070)
                num_2 = random.randint(1, 1056500)
                num_3 = random.randint(1, 1000)
                return str(num_2)+str(num_3)+str(uuid.uuid4())[:8]

            ident = create_id()

            if exam_name == "WAEC":

                if quantity == 1:
                    q = "WRCONE"

                elif quantity == 2:
                    q = "WRCTWO"
                elif quantity == 3:
                    q = "WRCTHR"
                elif quantity == 4:
                    q = "WRCFOU"
                elif quantity == 5:
                    q = "WRCFIV"

                if control.provider_api == "MOBILENIG":
                            # try:
                            check = user.withdraw(user.id, float(amt))
                            if check == False:
                                errors['error'] = u' insufficient balance '
                                raise serializers.ValidationError(errors)

                            Wallet_summary.objects.create(user=user, product="{} WAEC EPIN GENERATED  N{} ".format(
                                quantity, amt), amount=amt, previous_balance=previous_bal, after_balance=(previous_bal + float(amt)))

                            resp = requests.get(
                            f"https://mobilenig.com/API/bills/waec?username={config.mobilenig_username}&api_key={config.mobilenig_api_key}&product_code={q}&price={provider_amount*quantity}&trans_id={ident}")


                            # ab = json.loads(resp.text)
                            # data = ab["details"]["pins"]
                            ab = resp.text
                            data = ab
                            #print('.......... WAEC to mobilenig ............')
                            #print(resp.text)

                            status = 'successful'
                            # except:
                            #     pass

                elif control.provider_api == "EASYACCESS":

                        # try:
                            if quantity > 10:
                                errors['error'] = u'you can only generate up to 10 pins at a time'
                                raise serializers.ValidationError(errors)

                            else:
                                check = user.withdraw(user.id, float(amt))
                                if check == False:
                                    errors['error'] = u' insufficient balance '
                                    raise serializers.ValidationError(errors)

                                Wallet_summary.objects.create(user=user, product="{} WAEC EPIN GENERATED  N{} ".format(
                                    quantity, amt), amount=amt, previous_balance=previous_bal, after_balance=(previous_bal + float(amt)))

                                url = "https://easyaccess.com.ng/api/waec_v2.php"
                                payload={'no_of_pins': quantity}
                                files=[]
                                headers = {
                                  'AuthorizationToken': 'c5c59552e41f27ced0a3858e7a87f4d6'
                                }
                                headers.update({"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})

                                response = requests.request("POST", url, headers=headers, data=payload, files=files)
                                data = response.text
                                status = 'successful'

                        # except:
                        #     errors = {}
                        #     errors['error'] = u'Service is not currently available'
                        #     raise serializers.ValidationError(errors)

                else:
                                    check = user.withdraw(user.id,float(amt))
                                    if check == False:
                                        errors['error'] = u' insufficient balance '
                                        raise serializers.ValidationError(errors)

                                    Wallet_summary.objects.create(user= user, product="{} WAEC EPIN GENERATED  N{} ".format(quantity,amt), amount = amt, previous_balance = previous_bal, after_balance= (previous_bal + float(amt)))

                                    data = {"variation_code": "waecdirect","serviceID":"waec","phone":request.user.Phone,"request_id":ident,"quantity":quantity}
                                    #print(data)
                                    authentication = (f'{config.vtpass_email}', f'{config.vtpass_password}')
                                    resp = requests.post("https://vtpass.com/api/pay",data= data,auth=authentication)
                                    #print(resp.text)

                                    a = json.loads(resp.text)
                                    status = 'successful'
                                    data = a["purchased_code"]



            elif exam_name == "NECO":
                if quantity == 1:
                    q = "NECONE"

                elif quantity == 2:
                    q = "NECTWO"
                elif quantity == 3:
                    q = "NECTHR"
                elif quantity == 4:
                    q = "NECFOU"
                elif quantity == 5:
                    q = "NECFIV"

                if control.provider_api == "MOBILENIG":
                    # try:
                    check = user.withdraw(user.id, float(amt))
                    if check == False:
                        errors['error'] = u'Y insufficient balance '
                        raise serializers.ValidationError(errors)
                    Wallet_summary.objects.create(user=user, product="{} NECO EPIN GENERATED  N{} ".format(quantity, amt), amount=amt, previous_balance=previous_bal, after_balance=(previous_bal + float(amt)))
                    resp = requests.get(f"https://mobilenig.com/API/bills/neco?username={config.mobilenig_username}&api_key={config.mobilenig_api_key}&product_code={q}&price={provider_amount*quantity}&trans_id={ident}")
                    #print('.......... NECO to mobilenig ............')
                    #print(resp.text)
                    # ab = json.loads(resp.text)
                    # data = ab["details"]["pins"]
                    ab = resp.text
                    data = ab
                    status = 'successful'

                    # except:
                    #     errors['error'] = u"Something went wrong please contact admin before perform another transaction"
                    #     raise serializers.ValidationError(errors)

                elif control.provider_api == "EASYACCESS":
                    try:
                        if quantity > 10:
                            errors['error'] = u'you can only generate up to 10 pins at a time'
                            raise serializers.ValidationError(errors)

                        else:
                            check = user.withdraw(user.id, float(amt))
                            if check == False:
                                errors['error'] = u'Y insufficient balance '
                                raise serializers.ValidationError(errors)
                            Wallet_summary.objects.create(user=user, product="{} NECO EPIN GENERATED  N{} ".format(quantity, amt), amount=amt, previous_balance=previous_bal, after_balance=(previous_bal + float(amt)))

                            url = "https://easyaccess.com.ng/api/neco_v2.php"

                            payload={'no_of_pins': quantity}
                            files=[]
                            headers = {
                              'AuthorizationToken': 'c5c59552e41f27ced0a3858e7a87f4d6'
                            }
                            headers.update({"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})

                            response = requests.request("POST", url, headers=headers, data=payload, files=files)
                            data = response.text
                            status = 'successful'

                    except:
                        errors = {}
                        errors['error'] = u'Service is not currently available'
                        raise serializers.ValidationError(errors)

                else:
                      errors = {}
                      errors['error'] = u'Service is not currently available'
                      raise serializers.ValidationError(errors)




            serializer.save(data=data, amount=amt, previous_balance=previous_bal, after_balance=(
                previous_bal - amt))

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# class Result_Checker_Pin_orderAPIListView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request, format=None):
#         items = Result_Checker_Pin_order.objects.filter(
#             user=request.user).order_by('-create_date')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = Result_Checker_Pin_orderSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         status = "processing"
#         fund = 0
#         serializer = Result_Checker_Pin_orderSerializer(
#             data=request.data, context={'request': request})

#         if serializer.is_valid():
#             order_username = (serializer.validated_data["user"]).username
#             exam = serializer.validated_data["exam_name"]
#             quantity = serializer.validated_data["quantity"]
#             exam_name = exam
#             errors = {}
#             control = Result_Checker_Pin.objects.get(exam_name=exam)


#             provider_amount = round(control.provider_amount)
#             #print(provider_amount)

#             if request.user.user_type == "Affilliate":
#                 amount = Result_Checker_Pin.objects.get(
#                     exam_name=exam).Affilliate_price

#             elif request.user.user_type == "TopUser":
#                 amount = Result_Checker_Pin.objects.get(
#                     exam_name=exam).TopUser_price

#             elif request.user.user_type == "API":
#                 amount = Result_Checker_Pin.objects.get(
#                     exam_name=exam).api_price
#             else:
#                 amount = Result_Checker_Pin.objects.get(exam_name=exam).amount

#             amt = amount * quantity
#             user = (serializer.validated_data["user"])
#             previous_bal = user.Account_Balance
#             errors = {}
#             data = {}

#             def create_id():
#                 num = random.randint(1, 10070)
#                 num_2 = random.randint(1, 1056500)
#                 num_3 = random.randint(1, 1000)
#                 return str(num_2)+str(num_3)+str(uuid.uuid4())[:8]

#             ident = create_id()

#             if exam_name == "WAEC":

#                 if quantity == 1:
#                     q = "WRCONE"

#                 elif quantity == 2:
#                     q = "WRCTWO"
#                 elif quantity == 3:
#                     q = "WRCTHR"
#                 elif quantity == 4:
#                     q = "WRCFOU"
#                 elif quantity == 5:
#                     q = "WRCFIV"

#                 if control.provider_api == "MOBILENIG":
#                             #print('hello mojeed am going to mobilenig')
#                             #print(f"https://mobilenig.com/API/bills/waec?username={config.mobilenig_username}&api_key={config.mobilenig_api_key}&product_code={q}&price={provider_amount*quantity}&trans_id={ident}")
#                             #try:

#                             check = user.withdraw(user.id, float(amt))
#                             if check == False:
#                                 errors['error'] = u' insufficient balance '
#                                 raise serializers.ValidationError(errors)

#                             Wallet_summary.objects.create(user=user, product="{} WAEC EPIN GENERATED  N{} ".format(quantity, amt), amount=amt, previous_balance=previous_bal, after_balance=(previous_bal + float(amt)))

#                             resp = requests.get(f"https://mobilenig.com/API/bills/waec_test?username={config.mobilenig_username}&api_key={config.mobilenig_api_key}&product_code={q}&price={provider_amount*quantity}&trans_id={ident}")
#                             status = 'successful'
#                             #print(resp.text)
#                             ab = json.loads(resp.text)
#                             data = resp.text
#                             #print(data)
#                 else:


#                                     check = user.withdraw(user.id,float(amt))
#                                     if check == False:
#                                         errors['error'] = u' insufficient balance '
#                                         raise serializers.ValidationError(errors)

#                                     Wallet_summary.objects.create(user= user, product="{} WAEC EPIN GENERATED  N{} ".format(quantity,amt), amount = amt, previous_balance = previous_bal, after_balance= (previous_bal + float(amt)))

#                                     data = {"variation_code": "waecdirect","serviceID":"waec","phone":request.user.Phone,"request_id":ident,"quantity":quantity}
#                                     #print(data)
#                                     authentication = (f'{config.vtpass_email}', f'{config.vtpass_password}')
#                                     resp = requests.post("https://vtpass.com/api/pay",data= data,auth=authentication)
#                                     #print(resp.text)


#                                     status = 'successful'


#                                     try:

#                                             a = json.loads(resp.text)
#                                             status = 'successful'
#                                             data = a["purchased_code"]
#                                     except:

#                                         try:
#                                             url = 'https://vtpass.com/api/requery'
#                                             data = {"request_id":ident}
#                                             authentication = (f'{config.vtpass_email}', f'{config.vtpass_password}')
#                                             resp = requests.post(url,data= data,auth=authentication)

#                                             a = json.loads(resp.text)
#                                             data = a["purchased_code"]
#                                         except:
#                                             pass



#             elif exam_name == "NECO":
#                 if quantity == 1:
#                     q = "NECONE"

#                 elif quantity == 2:
#                     q = "NECTWO"
#                 elif quantity == 3:
#                     q = "NECTHR"
#                 elif quantity == 4:
#                     q = "NECFOU"
#                 elif quantity == 5:
#                     q = "NECFIV"
#                 if control.provider_api == "MOBILENIG":
#                         #try:



#                         check = user.withdraw(user.id, float(amt))
#                         if check == False:
#                             errors['error'] = u'Y insufficient balance '
#                             raise serializers.ValidationError(errors)
#                         Wallet_summary.objects.create(user=user, product="{} NECO EPIN GENERATED  N{} ".format(
#                             quantity, amt), amount=amt, previous_balance=previous_bal, after_balance=(previous_bal + float(amt)))

#                         resp = requests.get(
#                         f"https://mobilenig.com/API/bills/neco?username={config.mobilenig_username}&api_key={config.mobilenig_api_key}&product_code={q}&price={provider_amount*quantity}&trans_id={ident}")

#                         status = 'successful'
#                         #print(resp.text)
#                         ab = json.loads(resp.text)
#                         data = resp.text
#                         #print(data)

#                 else:
#                           errors = {}
#                           errors['error'] = u'Service is not currently available'
#                           raise serializers.ValidationError(errors)




#             serializer.save(data=data, amount=amt, previous_balance=previous_bal, after_balance=(
#                 previous_bal - amt))

#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# Result_Checker_Pin_order api
class Recharge_pin_orderAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, format=None):
        try:
            item = Recharge_pin_order.objects.filter(
                user=request.user).get(pk=id)
            serializer = Recharge_pin_orderSerializer(item)
            return Response(serializer.data)
        except Recharge_pin_order.DoesNotExist:
            return Response(status=404)


class Recharge_pin_orderAPIListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        items = Recharge_pin_order.objects.filter(
            user=request.user).order_by('-create_date')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = Recharge_pin_orderSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        status = "processing"
        fund = 0
        serializer = Recharge_pin_orderSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            order_username = (serializer.validated_data["user"]).username
            network = serializer.validated_data["network"]
            network_amount = serializer.validated_data["network_amount"]
            quantity = serializer.validated_data["quantity"]
            #amount = Result_Checker_Pin.objects.get(exam_name=exam).amount
            #amt = network_amount.amount_to_pay * quantity
            user = (serializer.validated_data["user"])
            previous_bal = user.Account_Balance
            errors = {}

            #print('............RECHARGE PRNGINTI ORDER............')
            #print(f"network = {network}")
            #print(f"network_amount = {network_amount}")

            myamount = network_amount.amount

            if request.user.user_type == "Affilliate":
                amt = network_amount.Affilliate_price * quantity

            elif request.user.user_type == "TopUser":
                amt = network_amount.TopUser_price * quantity

            elif request.user.user_type == "API":
                amt = network_amount.api_price * quantity
            else:
                amt = network_amount.amount_to_pay * quantity

            def create_id():
                num = random.randint(1, 10070)
                num_2 = random.randint(1, 1056500)
                num_3 = random.randint(1, 1000)
                return str(num_2)+str(num_3)+str(uuid.uuid4())[:8]

            ident = create_id()

            if Recharge_pin.objects.filter(network=Network.objects.get(name=network)).filter(available=True).filter(amount=myamount):
                check = user.withdraw(user.id, float(amt))
                if check == False:
                    errors['error'] = u'Y insufficient balance '
                    raise serializers.ValidationError(errors)
                Wallet_summary.objects.create(user=user, product="{} {}  N{} Airtime pin Generated".format(
                    network.name, quantity, myamount), amount=amt, previous_balance=previous_bal, after_balance=(previous_bal - amt))

                qs = Recharge_pin.objects.filter(network=Network.objects.get(name=network)).filter(
                    available=True).filter(amount=network_amount.amount)[:quantity]
                jsondata = seria2.serialize('json', qs)
                data = jsondata
                for x in qs:
                    x.available = False
                    x.save()

                #print(jsondata)
            else:
                errors['error'] = u'Airtime Pin is not Available on this network currently'
                raise serializers.ValidationError(errors)

            serializer.save(data=data, amount=amt, previous_balance=previous_bal, after_balance=(
                previous_bal - amt))

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ReferalListView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        items = Referal_list.objects.filter(user=request.user).order_by('id')
        serializer = Referal_listSerializer(items, many=True)
        return Response(serializer.data)



class KYCCreate(generic.CreateView):
    form_class = KYCForm
    template_name = 'kyc_form.html'

    def form_valid(self, form):
        form._errors[forms.forms. NON_FIELD_ERRORS] = ErrorList(
            [u'use updated browser and retry'])
        return self.form_invalid(form)

        return super(KYCCreate, self).form_valid(form)

#######################################KYC API################################


class KYCAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        items = KYC.objects.filter(user=request.user)
        serializer = KYCSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = KYCSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            user = (serializer.validated_data["user"])
            errors = {}
            First_Name = (serializer.validated_data["First_Name"])
            Middle_Name = (serializer.validated_data["Middle_Name"])
            Last_Name = (serializer.validated_data["Last_Name"])
            DOB = (serializer.validated_data["DOB"])
            Gender = (serializer.validated_data["Gender"])
            State_of_origin = (serializer.validated_data["State_of_origin"])
            Local_gov_of_origin = (
                serializer.validated_data["Local_gov_of_origin"])
            BVN = (serializer.validated_data["BVN"])
            passport_photogragh = (
                serializer.validated_data["passport_photogragh"])
            verify = False

            previous_bal = user.Account_Balance
            if 100 > user.Account_Balance:
                errors['error'] = u'Y insufficient balance '
                raise serializers.ValidationError(errors)


            def create_id():
                num = random.randint(1, 10)
                num_2 = random.randint(1, 10)
                num_3 = random.randint(80, 10000)
                return str(num_2)+str(num_3) + str(uuid.uuid4())[:8]

            url = "https://www.idchecker.com.ng/bvn_verify/"

            payload = {"bvn": BVN}

            headers = {
                'Authorization': f'Token {config.idchecker_api_key}',
                'Content-Type': 'application/json',
            }
            #print(config.idchecker_api_key)

            abd = datetime.strptime(str(DOB), '%Y-%m-%d').strftime('%d-%b-%Y')
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            #print((response.text))
            if response.status_code == 200 or  response.status_code == 201 :
                    check = user.withdraw(user.id, 100)

                    if check == False:
                        errors['error'] = u' insufficient balance '
                        raise serializers.ValidationError(errors)

                    Wallet_summary.objects.create(user=user, product="BVN VERIFY  N{}  ".format( 100), amount=100, previous_balance=previous_bal, after_balance=(previous_bal - float(100)))
                    mydata = json.loads(response.text)
                    #print(mydata['response']['data'])

                    if mydata["response"]["responsecode"]  == "00":
                            if KYC.objects.filter(user=user).exists():
                                ab = KYC.objects.filter(user=user).first()
                                if First_Name.upper() == mydata['response']['data']['firstName'].upper() and Middle_Name.upper() == mydata['response']['data']['middleName'].upper() and Last_Name.upper() == mydata['response']['data']['lastName'].upper() and abd == mydata['response']['data']['dateOfBirth'] and Gender == mydata['response']['data']['gender'].upper():
                                    message = "Information submitted successful ,Your account verification in process"
                                    ab.First_Name = First_Name
                                    ab.Middle_Name = Middle_Name
                                    ab.Last_Name = Last_Name
                                    ab.DOB = DOB
                                    ab.Gender = Gender
                                    ab.State_of_origin = State_of_origin
                                    ab.Local_gov_of_origin = Local_gov_of_origin
                                    ab.BVN = BVN
                                    ab.passport_photogragh = passport_photogragh
                                    ab.comment = "BVN MATCHED WITH DETAILS"
                                    ab.dump = response.text
                                    ab.primary_details_verified = True
                                    ab.status= "processing"
                                    ab.save()
                                    return Response({"message": message}, status=201)
                                else:
                                    ab.dump = response.text
                                    ab.comment = "BVN NOT MATCH WITH DEATILS SUPPLIED"


                                    ab.save()
                                    comment = "BVN NOT MATCH WITH DEATILS"
                                    return Response({"message": "BVN NOT MATCH WITH DETAILS SUPPLIED"}, status=400)
                            else:
                                if First_Name.upper() == mydata['response']['data']['firstName'].upper() and Middle_Name.upper() == mydata['response']['data']['middleName'].upper() and Last_Name.upper() == mydata['response']['data']['lastName'].upper() and abd == mydata['response']['data']['dateOfBirth'] and Gender == mydata['response']['data']['gender'].upper():
                                    message = "Information submitted successful ,Your account verification in process"
                                    comment = "BVN MATCHED WITH DETAILS SUPPLIED"
                                    verify = True

                                else:
                                    comment = "BVN MATCHED WITH DETAILS SUPPLIED"
                                    message = "BVN MATCHED WITH DETAILS SUPPLIED"
                                    serializer.save(comment=comment, dump=response.text, primary_details_verified=verify)
                                    return Response({"response": message}, status=400)


                    else:
                                data = json.loads(response.text)
                                return Response(data,status = 400)

            elif  response.status_code == 500:
                            data = {
                                "status":"error",
                                "message": "something went wrong, please try again",
                                }
                            return Response(data,status = 500)
            else:
                        data = json.loads(response.text)
                        return Response(data,status = 400)

            serializer.save(comment=comment, dump=response.text, primary_details_verified=verify)

            return Response({"message": message}, status=201)
        return Response(serializer.errors, status=400)





class Wallet_summaryListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        items = Wallet_summary.objects.filter(user=request.user).order_by('-create_date')
        serializer = Wallet_summarySerializer(items, many=True)
        return Response(serializer.data)



class BankpaymentAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        items = Bankpayment.objects.filter(user=request.user).order_by('-create_date')
        serializer = seria2.serialize('json', items)

        data = [x["fields"] for x in json.loads(serializer)]
        return Response(data)

    def post(self, request, format=None):
           status = "processing"
           fund = 0
           data = request.data

           user = request.user
           bank_paid_to =  request.data["bank_paid_to"]
           Reference =  request.data["Reference"]
           amount =  request.data["amount"]



           Bankpayment.objects.create(user=user,Bank_paid_to=bank_paid_to ,Reference=Reference,amount=amount)


           try:
                        sendmail(" Bank Payment Notification from husmodata.com", "{} want to fund his/her account with  bank payment {}  amount:{} https://www.husmodata.com/page-not-found-error/page/vtuapp/bankpayment/".format(user.username,bank_paid_to, amount), "usmanreal43@gmail.com", "Elecastle")
           except:
                pass
           return Response({'message':"Bank Notification submitted successful"}, status=200)



class available_recharge(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        info = ""
        if Info_Alert.objects.all():
            info = [x.message for x in Info_Alert.objects.all()[:1]][0]

        data = {
            "mtn": Recharge_pin.objects.filter(network=Network.objects.get(name="MTN")).filter(available=True).count(),
            "glo": Recharge_pin.objects.filter(network=Network.objects.get(name="GLO")).filter(available=True).count(),
            "airtel": Recharge_pin.objects.filter(network=Network.objects.get(name="AIRTEL")).filter(available=True).count(),
            "9mobile": Recharge_pin.objects.filter(network=Network.objects.get(name="9MOBILE")).filter(available=True).count(),
            "balance":request.user.Account_Balance,
            "info": info
        }

        return Response(data)






@require_POST
@csrf_exempt
def U_Webhook(request):
    data = request.body
    forwarded_for =  u'{}'.format(request.META.get('HTTP_X_FORWARDED_FOR'))
    result = json.loads(data)

    print(' ')
    print('................RECIEVED FROM HOOK................')
    print("result = ", result)

    ident = result['data']['customRef']

    # try:
    trans = Data.objects.filter(ident=ident).first()
    if trans:

        if trans.Status != 'successful' and result["status"] == "failed":
            api_msg = f"customRef({ident}) is valid, refund complete"

            trans.Status == 'failed'
            trans.save()

        else:
            api_msg = f"{ident} was successful"

    else:
        api_msg = f"customRef({ident}) not found"
        print(f"customRef({ident}) not found")

    # except:
    #     print('transaction not found')
    #     api_msg = "unable to handle request, maintenanace mode"

    return JsonResponse({'status':"connection successful",'message': f"{api_msg}"}, status=200)

