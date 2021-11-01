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
from vtuapp.forms import *
from vtuapp.models import *
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.db.models import F
from twilio.rest import Client
from django import forms
from django.core import serializers as seria2
from django.utils.translation import gettext_lazy as _
from django.forms.utils import ErrorList
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
from vtuapp.serializers import *
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






def salesAccount(request):
    form_data = request.POST
    start_date = form_data['start_date']
    end_date = form_data['end_date']

    net_1 = Network.objects.get(name='MTN')
    net_2 = Network.objects.get(name='GLO')
    net_3 = Network.objects.get(name='9MOBILE')
    net_4 = Network.objects.get(name='AIRTEL')


    mtn_dataSold_total = Data.objects.filter(network__name="MTN", Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    airtel_dataSold_total = Data.objects.filter(network__name="AIRTEL", Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    glo_dataSold_total = Data.objects.filter(network__name="GLO", Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    eti_dataSold_total = Data.objects.filter(network__name="9MOBILE", Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    smile_dataSold_total = Data.objects.filter(network__name="SMILE", Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    
    mtn_dataSold_total2 = Data.objects.filter(network__name="MTN", Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    airtel_dataSold_total2 = Data.objects.filter(network__name="AIRTEL", Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    glo_dataSold_total2 = Data.objects.filter(network__name="GLO", Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    eti_dataSold_total2 = Data.objects.filter(network__name="9MOBILE", Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    smile_dataSold_total2 = Data.objects.filter(network__name="SMILE", Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0

    mtn_dataSold_total3 = Data.objects.filter(network__name="MTN", Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    airtel_dataSold_total3 = Data.objects.filter(network__name="AIRTEL", Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    glo_dataSold_total3 = Data.objects.filter(network__name="GLO", Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    eti_dataSold_total3 = Data.objects.filter(network__name="9MOBILE", Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    smile_dataSold_total3 = Data.objects.filter(network__name="SMILE", Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0

    mtn_airtimeSold_total2 = AirtimeTopup.objects.filter(network__name="MTN", Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    airtel_airtimeSold_total2 = AirtimeTopup.objects.filter(network__name="AIRTEL", Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    glo_airtimeSold_total2 = AirtimeTopup.objects.filter(network__name="GLO", Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    eti_airtimeSold_total2 = AirtimeTopup.objects.filter(network__name="9MOBILE", Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    

    mtn_airtimeSold_total3 = AirtimeTopup.objects.filter(network__name="MTN", Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    airtel_airtimeSold_total3 = AirtimeTopup.objects.filter(network__name="AIRTEL", Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    glo_airtimeSold_total3 = AirtimeTopup.objects.filter(network__name="GLO", Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    eti_airtimeSold_total3 = AirtimeTopup.objects.filter(network__name="9MOBILE", Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    

    mtn_airtimeSold_total = AirtimeTopup.objects.filter(network__name="MTN", Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    airtel_airtimeSold_total = AirtimeTopup.objects.filter(network__name="AIRTEL", Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    glo_airtimeSold_total = AirtimeTopup.objects.filter(network__name="GLO", Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    eti_airtimeSold_total = AirtimeTopup.objects.filter(network__name="9MOBILE", Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    
    total_user_wallet = CustomUser.objects.all().aggregate(Sum('Account_Balance'))['Account_Balance__sum'] or 0
    total_user_bonus = CustomUser.objects.all().aggregate(Sum('Referer_Bonus'))['Referer_Bonus__sum'] or 0
    total_bank_payments = Bankpayment.objects.filter(Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0
    total_atm_payments = paymentgateway.objects.filter(created_on__date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0
    total_coupon_payments = CouponPayment.objects.all().filter(create_date__date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0
    bill_payment = Billpayment.objects.filter(Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    Cable_payment = Cablesub.objects.filter(Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    recharge_card = Recharge_pin_order.objects.filter(create_date__date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0
    result_checker = Result_Checker_Pin_order.objects.filter( create_date__date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0
    credit = Transactions.objects.filter(create_date__date__range=[start_date, end_date], transaction_type="CREDIT").aggregate(Sum('amount'))['amount__sum'] or 0
    debit = Transactions.objects.filter(create_date__date__range=[start_date, end_date], transaction_type="DEBIT").aggregate(Sum('amount'))['amount__sum'] or 0


    gotv =  Cablesub.objects.filter(cablename=Cable.objects.get(name="GOTV"),Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    dstv =  Cablesub.objects.filter(cablename=Cable.objects.get(name="DSTV"),Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    startime  = Cablesub.objects.filter(cablename=Cable.objects.get(name="STARTIME"),Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0

    gotv2 =  Cablesub.objects.filter(cablename=Cable.objects.get(name="GOTV"),Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    dstv2 =  Cablesub.objects.filter(cablename=Cable.objects.get(name="DSTV"),Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    startime2  = Cablesub.objects.filter(cablename=Cable.objects.get(name="STARTIME"),Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0


    gotv3 =  Cablesub.objects.filter(cablename=Cable.objects.get(name="GOTV"),Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    dstv3 =  Cablesub.objects.filter(cablename=Cable.objects.get(name="DSTV"),Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0
    startime3  = Cablesub.objects.filter(cablename=Cable.objects.get(name="STARTIME"),Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('plan_amount'))['plan_amount__sum'] or 0


    
    d1 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="IKEDC"),Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    d2 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="EKEDC"),Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    d3 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="AEDC"),Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    d4 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="IBEDC"),Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    d5 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="KEDC"),Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    d6 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="EEDC"),Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    d7 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="PHEDC"),Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    d8 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="KAEDC"),Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    d9 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="JEDC"),Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    d10 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="BEDC"),Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    d11 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="YEDC"),Status = "successful", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    

    e1 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="IKEDC"),Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    e2 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="EKEDC"),Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    e3 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="AEDC"),Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    e4 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="IBEDC"),Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    e5 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="KEDC"),Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    e6 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="EEDC"),Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    e7 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="PHEDC"),Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    e8 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="KAEDC"),Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    e9 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="JEDC"),Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    e10 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="BEDC"),Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    e11 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="YEDC"),Status = "processing", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    


    f1 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="IKEDC"),Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    f2 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="EKEDC"),Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    f3 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="AEDC"),Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    f4 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="IBEDC"),Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    f5 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="KEDC"),Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    f6 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="EEDC"),Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    f7 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="PHEDC"),Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    f8 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="KAEDC"),Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    f9 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="JEDC"),Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    f10 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="BEDC"),Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    f11 = Billpayment.objects.filter(disco_name = Disco_provider_name.objects.get(p_id="YEDC"),Status = "failed", create_date__date__range=[start_date, end_date]).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    
    
  

    data_mtn_obj = Data.objects.filter( Status = "successful",network__name="MTN", plan__plan_size__lt=60, create_date__date__range=[start_date, end_date]).aggregate(Sum('plan__plan_size'))['plan__plan_size__sum'] or 0
    data_mtn_obj_2 = Data.objects.filter( Status = "successful",network__name="MTN", plan__plan_size__gt=60, create_date__date__range=[start_date, end_date]).aggregate(Sum('plan__plan_size'))['plan__plan_size__sum'] or 0
    data_glo_obj = Data.objects.filter( Status = "successful",network__name="GLO", plan__plan_size__lt=60, create_date__date__range=[start_date, end_date]).aggregate(Sum('plan__plan_size'))['plan__plan_size__sum'] or 0
    data_glo_obj_2 = Data.objects.filter( Status = "successful",network__name="GLO", plan__plan_size__gt=60, create_date__date__range=[start_date, end_date]).aggregate(Sum('plan__plan_size'))['plan__plan_size__sum'] or 0
    data_9mobile_obj = Data.objects.filter( Status = "successful",network__name="9MOBILE", plan__plan_size__lt=60, create_date__date__range=[start_date, end_date]).aggregate(Sum('plan__plan_size'))['plan__plan_size__sum'] or 0
    data_9mobile_obj_2 = Data.objects.filter( Status = "successful",network__name="9MOBILE", plan__plan_size__gt=60, create_date__date__range=[start_date, end_date]).aggregate(Sum('plan__plan_size'))['plan__plan_size__sum'] or 0
    data_airtel_obj = Data.objects.filter( Status = "successful",network__name="AIRTEL", plan__plan_size__lt=60, create_date__date__range=[start_date, end_date]).aggregate(Sum('plan__plan_size'))['plan__plan_size__sum'] or 0
    data_airtel_obj_2 = Data.objects.filter( Status = "successful",network__name="AIRTEL", plan__plan_size__gt=60, create_date__date__range=[start_date, end_date]).aggregate(Sum('plan__plan_size'))['plan__plan_size__sum'] or 0
        
    if request.method == 'POST':
            return JsonResponse({
                "mtn_dataSold_total": str(mtn_dataSold_total)+ " ( " + str (round((data_mtn_obj) + (data_mtn_obj_2/1000),2)),
                "glo_dataSold_total": str(glo_dataSold_total) + " ( " + str (round((data_glo_obj) + (data_glo_obj_2/1000),2)),
                "airtel_dataSold_total": str(airtel_dataSold_total) + " (" + str (round((data_airtel_obj) + (data_airtel_obj_2/1000),2)),
                "eti_dataSold_total": str(eti_dataSold_total) + " (" + str (round((data_9mobile_obj) + (data_9mobile_obj_2/1000),2)),
                #############
                "mtn_airtimeSold_total": mtn_airtimeSold_total,
                "glo_airtimeSold_total": glo_airtimeSold_total,
                "airtel_airtimeSold_total": airtel_airtimeSold_total,
                "eti_airtimeSold_total": eti_airtimeSold_total,
                ###########
                "total_bank_payments": total_bank_payments,
                "bill_payment":bill_payment,
                 "Cable_payment":Cable_payment,
                "total_atm_payments": total_atm_payments,
                "total_coupon_payments": total_coupon_payments,
                "smile_dataSold_total":smile_dataSold_total,
                "result_checker":result_checker,
                 "recharge_card":recharge_card,
                 "debit":debit,
                 "credit":credit,
                 "data_list":[mtn_dataSold_total,glo_dataSold_total,airtel_dataSold_total,eti_dataSold_total,smile_dataSold_total],
                 "data_list2":[mtn_dataSold_total2,glo_dataSold_total2,airtel_dataSold_total2,eti_dataSold_total2,smile_dataSold_total2],
                 "data_list3":[mtn_dataSold_total3,glo_dataSold_total3,airtel_dataSold_total3,eti_dataSold_total3,smile_dataSold_total3],
                 "airtime_list":[mtn_airtimeSold_total,glo_airtimeSold_total,airtel_airtimeSold_total,eti_airtimeSold_total],
                "airtime_list2":[mtn_airtimeSold_total2,glo_airtimeSold_total2,airtel_airtimeSold_total2,eti_airtimeSold_total2],
                "airtime_list3":[mtn_airtimeSold_total3,glo_airtimeSold_total3,airtel_airtimeSold_total3,eti_airtimeSold_total3],
                
                
                 "cable_list":[gotv,dstv,startime],
                 "bill_list":[d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11],

                 "cable_list2":[gotv2,dstv2,startime2],
                 "bill_list2":[e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11],

                 "cable_list3":[gotv3,dstv3,startime3],
                 "bill_list3":[f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11]
            }, status=200)


    else:
        form = SalesAccountingForm()
        return JsonResponse({'message':'an error occured'},status=400)






