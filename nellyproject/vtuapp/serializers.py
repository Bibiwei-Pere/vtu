from rest_framework.serializers import ModelSerializer
from  .models import *
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueValidator
from django.utils.timezone import datetime  as datetimex
import uuid
import random,requests,json
from requests.auth import HTTPBasicAuth
import hashlib


config = ''
config = WebsiteConfiguration.objects.all().first()


class CustomUserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
            required=True,
           )
    username = serializers.CharField(
            )
    password = serializers.CharField(min_length=8)
    Phone = serializers.CharField(min_length=11,)
    referer_username = serializers.CharField(max_length=100,required =  False, allow_blank=True)
    wallet_balance = serializers.ReadOnlyField(source='walletb')
    bonus_balance = serializers.ReadOnlyField(source='bonusb')
    img = serializers.ReadOnlyField(source='passport')
    bank_accounts = serializers.ReadOnlyField(source='f_account')


    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'])


        try:

            def create_id():
                num = random.randint(1, 10)
                num_2 = random.randint(1, 10)
                num_3 = random.randint(1, 10)
                return str(num_2)+str(num_3)+str(uuid.uuid4())[:4]

            body = {
                 "accountReference": create_id(),
                "accountName": validated_data['username'],
                "currencyCode": "NGN",
                "contractCode": f"{config.monnify_contract_code}",
                "customerEmail": validated_data['email'],
                "incomeSplitConfig": [],
                "restrictPaymentSource": False,
                "allowedPaymentSources": {},
                "customerName": validated_data['username'],
                "getAllAvailableBanks": True,
            }

            if not user.reservedaccountNumber:

                data = json.dumps(body)
                ad = requests.post("https://api.monnify.com/api/v1/auth/login", auth=HTTPBasicAuth(f'{config.monnify_API_KEY}', f'{config.monnify_SECRET_KEY}'))
                mydata = json.loads(ad.text)
                headers = {'Content-Type': 'application/json',"Authorization": "Bearer {}" .format(mydata['responseBody']["accessToken"])}
                ab = requests.post("https://api.monnify.com/api/v2/bank-transfer/reserved-accounts",headers=headers, data=data)
                mydata = json.loads(ab.text)

                user.reservedaccountNumber = mydata["responseBody"]["accounts"][0]["accountNumber"]
                user.reservedbankName = mydata["responseBody"]["accounts"][0]["bankName"]
                user.reservedaccountReference = mydata["responseBody"]["accountReference"]
                user.accounts = json.dumps({"accounts":mydata["responseBody"]["accounts"]})
                user.save()

            else:
                pass

        except:
            pass


        user.Phone = validated_data['Phone']
        user.FullName = validated_data['FullName']
        user.Address = validated_data["Address"]
        user.referer_username = validated_data['referer_username']
        user.save()
        try:
            Referal_list.objects.create(user = CustomUser.objects.get(username__iexact = user.referer_username) , username=user.username)
        except:
            pass
        return user


    def validate(self, data):
        errors = {}
        username = data.get('username')
        email = data.get('email')
        phone = data.get('Phone')
        referer_username  = data.get('referer_username')



        if CustomUser.objects.filter(username__iexact = username).exists() :
               errors['error'] = u'This username has been taken'
               raise serializers.ValidationError(errors)

        elif CustomUser.objects.filter(email__iexact = email).exists() :
               errors['error'] = u'This email has been taken'
               raise serializers.ValidationError(errors)

        elif CustomUser.objects.filter(Phone__iexact =phone).exists() :
               errors['error'] = u'This Phone number has been taken'
               raise serializers.ValidationError(errors)

        elif not phone.isdigit() or len(phone) > 11:
            errors['error'] = u'invalid mobile number ,phone number without country code i.e 090,081,070 !'

            raise serializers.ValidationError(errors)

        elif not email.endswith(("@gmail.com",'@yahoo.com')):
             errors['error'] = u'We accept only valid gmail or yahoo mail account'
             raise serializers.ValidationError(errors)

        elif referer_username and not CustomUser.objects.filter(username__iexact = referer_username).exists():
               errors['error'] = u'Invalid referal username, kindly leave blank if you don\'t have referal username'
               raise serializers.ValidationError(errors)

        return data


    class Meta:
        model = CustomUser
        fields = ('id','email', 'username','FullName','pin','img',"Address",'Phone','user_type',"password",'Account_Balance','wallet_balance','bonus_balance','referer_username','bank_accounts',"reservedaccountNumber","reservedbankName")





class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)



class NetworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Network
        fields = ('id','name')


class PercentageSerializer(serializers.ModelSerializer):
    network_name = serializers.ReadOnlyField(source='netname')
    class Meta:
        model = Percentage
        fields = ('network','percent','network_name')


class Result_Checker_PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result_Checker_Pin
        fields = ('exam_name','amount')



class RechargeSerializer(serializers.ModelSerializer):
    network_name= serializers.ReadOnlyField(source='netname')
    class Meta:
        model = Recharge
        fields = ('id','network_name','amount','amount_to_pay')


class Admin_numberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admin_number
        fields = ('network','phone_number')


class Wallet_summarySerializer(serializers.ModelSerializer):


    class Meta:
        model = Wallet_summary
        fields = ('ident','product',"amount","previous_balance","after_balance","create_date")


class Referal_listSerializer(serializers.ModelSerializer):
    bonus = serializers.ReadOnlyField(source='amount')
    class Meta:
        model = Referal_list
        fields = ('username',"bonus")


class Bulk_MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bulk_Message
        fields = ('total','unit',"sendername","message","page","amount","to","ident","create_date","DND")


class BankAccount_PinSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankAccount
        fields = ("bank_name","account_name","account_number")


class TopupPercentageSerializer(serializers.ModelSerializer):

    network_name= serializers.ReadOnlyField(source='netname')
    class Meta:
        model = TopupPercentage
        fields = ('network','percent','network_name')


class PlanSerializer(serializers.ModelSerializer):

    plan_amount= serializers.ReadOnlyField(source='plan_amt')
    plan_network = serializers.ReadOnlyField(source='plan_net')
    plan= serializers.ReadOnlyField(source='plan_name')
    dataplan_id= serializers.ReadOnlyField(source='plan_id')


    class Meta:
        model = Plan
        fields = ('id','dataplan_id','plan_type','network','network','plan_network','month_validate', 'plan','plan_amount' )



class PlanSerializer2(serializers.ModelSerializer):

    plan_amount= serializers.ReadOnlyField(source='plan_amt2')
    plan_network = serializers.ReadOnlyField(source='plan_net')
    plan= serializers.ReadOnlyField(source='plan_name')
    dataplan_id= serializers.ReadOnlyField(source='plan_id')

    class Meta:
        model = Plan
        fields = ('id','dataplan_id','plan_type','TopUser_price','Affilliate_price','network','plan_network','month_validate', 'plan','plan_amount' )


class PlanSerializer3(serializers.ModelSerializer):

    plan_amount= serializers.ReadOnlyField(source='plan_amt3')
    plan_network = serializers.ReadOnlyField(source='plan_net')
    plan= serializers.ReadOnlyField(source='plan_name')
    dataplan_id= serializers.ReadOnlyField(source='plan_id')

    class Meta:
        model = Plan
        fields = ('id','dataplan_id','plan_type','TopUser_price','Affilliate_price','network','plan_network','month_validate', 'plan','plan_amount' )




class CablenameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cable
        fields = ('id','name')


class DiscoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disco_provider_name
        fields = ('id','name')


class CablePlanSerializer(serializers.ModelSerializer):

    plan_amount= serializers.ReadOnlyField(source='plan_amt')
    package= serializers.ReadOnlyField(source='plan_name')
    cableplan_id = serializers.ReadOnlyField(source='plan_id')
    cable = serializers.ReadOnlyField(source='cableplanname')


    class Meta:
        model = CablePlan
        fields = ('id','cableplan_id','cable','package', 'plan_amount', )


class paymentgatewaySerializer(serializers.ModelSerializer):



    class Meta:
        model = paymentgateway
        fields = ('id','user', 'reference','amount','Status','gateway','created_on' )





class bonus_transferSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = bonus_transfer
        fields = ('user','Current_bonus','amount','id','ident','Status','create_date' )

    def validate(self, data):
        errors = {}
        amount = data.get('amount')
        user = data.get('user')


        if float(amount) > user.Referer_Bonus:
            errors['error'] = u'You can\'t Tranfer to your wallet due to insufficient bonus balance'
            raise serializers.ValidationError(errors)

        elif float(data.get('amount')) < 500:
            errors['error'] = u'BELOW MINIMUM AMOUNT ALLOWED (₦500)'
            raise serializers.ValidationError(errors)


        return data



class WithdrawSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Withdraw
        fields = ('user','accountNumber','accountName','bankName','amount','id','ident','Status','create_date' )


    def validate(self, data):
        errors = {}
        amount = data.get('amount')
        user = data.get('user')


        if float(amount) >user.Account_Balance:
            errors['error'] = u' insufficient balance  ₦{} '.format(user.Account_Balance)
            raise serializers.ValidationError(errors)

        elif float(amount) < 1000000:
            errors['error'] = u' Minimun withdraw is #1000000 per transaction'
            raise serializers.ValidationError(errors)

        elif float(amount) > 1000000:
            errors['error'] = u' Maximum withdraw is #1000000 per transaction'
            raise serializers.ValidationError(errors)

        elif  user.is_superuser==False and Withdraw.objects.filter(create_date__date=datetimex.today()).count > 1:
               errors['error'] = u' Exceed Maximum withdraw limit for today.'
               raise serializers.ValidationError(errors)

        # elif  user.is_superuser==False and user.verify == False and  float(amount) > 1000000:
        #     errors['error'] = u'Unverify User are limit to 1000000 naira withdraw  per day'
        #     raise serializers.ValidationError(errors)


        # elif Transactions.objects.filter(user=user,transaction_type="DEBIT",create_date__date=datetimex.today()).exists():
        #     if user.verify == False and Transactions.objects.filter(user=user,transaction_type="DEBIT",create_date__date=datetimex.today()).aggregate(Sum('amount'))['amount__sum'] > 1000000:
        #         errors['error'] = u'Your have exceed  daily transactions limit for unverify account (₦1000000 ), pls verify your account to continue your daily transaction'
        #         raise serializers.ValidationError(errors)


        return data






class Recharge_pin_orderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    network_name = serializers.ReadOnlyField(source="net_work")
    class Meta:
        model = Recharge_pin_order
        fields = ('user','network','network_amount','network_name','name_on_card','quantity','data_pin','id','Status',"previous_balance","after_balance","amount",'create_date' )


    def validate(self, data):
        errors = {}
        network_amount = data.get('network_amount')
        quantity = data.get('quantity')
        user = data.get('user')
        net = data.get('network')
        myamount = network_amount.amount


        if user.user_type == "Affilliate":
                amt = network_amount.Affilliate_price * quantity

        elif user.user_type == "TopUser":
                amt = network_amount.TopUser_price * quantity

        elif user.user_type == "API":
                amt = network_amount.api_price * quantity
        else:
                amt = network_amount.amount_to_pay * quantity



        if float(amt) > user.Account_Balance:
            errors['error'] = u' insufficient balance  ₦{} '.format(user.Account_Balance)
            raise serializers.ValidationError(errors)

        elif quantity > 39:
            errors['error'] = u' MAXIMUM of 39 quantity per transaction'
            raise serializers.ValidationError(errors)

        elif Recharge_pin.objects.filter(network = Network.objects.get(name=net.name)).filter(available=True).filter(amount = myamount).count() < quantity :
             errors['error'] = u'Available airtime not upto what want to buy'
             raise serializers.ValidationError(errors)

        elif Disable_Service.objects.get(service ="Recharge_printing").disable == True:
               errors['error'] = u'This Service is not currently available please check back'
               raise serializers.ValidationError(errors)

        elif Network.objects.get(name=net.name).recharge_pin_disable == True:
              errors['error'] = u'Recharge pin is not available on this network currently'
              raise serializers.ValidationError(errors)

        elif not Wallet_Funding.objects.filter(user = user).exists():
            errors['error'] = u'No Wallet Funding Record Found, Contact admin for more information'
            raise serializers.ValidationError(errors)


        elif user.verify == False and  float(amt) > 1000000:
            errors['error'] = u'Unverify User are limit to 1000000 naira airtime topup  per day'
            raise serializers.ValidationError(errors)

        elif Transactions.objects.filter(user=user,transaction_type="DEBIT",create_date__date=datetimex.today()).exists():
            if user.verify == False and Transactions.objects.filter(user=user,transaction_type="DEBIT",create_date__date=datetimex.today()).aggregate(Sum('amount'))['amount__sum'] > 50000:
                errors['error'] = u'Your have exceed  daily transactions limit for unverify account (₦50000 ), pls verify your account to continue your daily transaction'
                raise serializers.ValidationError(errors)


        return data





class Result_Checker_Pin_orderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )


    class Meta:
        model = Result_Checker_Pin_order
        fields = ('user','exam_name','quantity','id','Status',"previous_balance","after_balance","amount",'create_date' )


    def validate(self, data):
        errors = {}
        quantity = data.get('quantity')
        user = data.get('user')
        exam = data.get('exam_name')

        if user.user_type == "Affilliate":
                amount = Result_Checker_Pin.objects.get(exam_name=exam).Affilliate_price

        elif user.user_type == "TopUser":
                amount = Result_Checker_Pin.objects.get(exam_name=exam).TopUser_price

        elif user.user_type == "API":
                amount = Result_Checker_Pin.objects.get(exam_name=exam).api_price
        else:
                amount = Result_Checker_Pin.objects.get(exam_name=exam).amount


        amt = quantity * amount


        if float(amt) > user.Account_Balance:
            errors['error'] = u' insufficient balance  ₦{} '.format(user.Account_Balance)
            raise serializers.ValidationError(errors)

        elif quantity > 5:
            errors['error'] = u' MAXIMUM of 5 quantity per transaction'
            raise serializers.ValidationError(errors)

        elif Disable_Service.objects.get(service ="Result_checker").disable == True:
               errors['error'] = u'This Service is not currently available please check back'
               raise serializers.ValidationError(errors)

        elif Result_Checker_Pin.objects.get(exam_name=exam).disable_this_exam == True:
               errors['error'] = u'This Service is not currently available please check back'
               raise serializers.ValidationError(errors)

        elif not Wallet_Funding.objects.filter(user = user).exists():
            errors['error'] = u'No Wallet Funding Record Found, Contact admin for more information'
            raise serializers.ValidationError(errors)

        elif Transactions.objects.filter(user=user,transaction_type="DEBIT",create_date__date=datetimex.today()).exists():
            if user.verify == False and Transactions.objects.filter(user=user,transaction_type="DEBIT",create_date__date=datetimex.today()).aggregate(Sum('amount'))['amount__sum'] > 1000000:
                errors['error'] = u'Your have exceed  daily transactions limit for unverify account (₦1000000 ), pls verify your account to continue your daily transaction'
                raise serializers.ValidationError(errors)

        return data


class TransferSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Transfer
        fields = ('user','receiver_username','amount','id','ident','Status','create_date' )


    def validate(self, data):
        errors = {}
        amount = data.get('amount')
        user = data.get('user')
        receiver_username = data.get('receiver_username')


        if float(amount) >user.Account_Balance:
            errors['error'] = u' insufficient balance  ₦{} '.format(user.Account_Balance)
            raise serializers.ValidationError(errors)

        elif not CustomUser.objects.filter(username__iexact = receiver_username).exists():
               errors['error'] = u'Invalid user or no user with that username.'
               raise serializers.ValidationError(errors)


        elif  user.username.lower() == receiver_username.lower():
               errors['error'] = u'You cannot transfer to yourself.'
               raise serializers.ValidationError(errors)

        elif float(data.get('amount')) < 1:
            errors['error'] = u'BELOW MINIMUM AMOUNT ALLOWED (₦1)'
            raise serializers.ValidationError(errors)


        elif  user.is_superuser==False and user.verify == False and  float(amount) > 1000000:
            errors['error'] = u'Unverify User are limit to 1000000 naira transfer  per day'
            raise serializers.ValidationError(errors)

        elif  user.is_superuser==False and Transfer.objects.filter(create_date__date=datetimex.today()).count > 2:
               errors['error'] = u'Exceed Maximum tranfer limit for today.'
               raise serializers.ValidationError(errors)


        elif Transactions.objects.filter(user=user,transaction_type="DEBIT",create_date__date=datetimex.today()).exists():
          if user.verify == False and Transactions.objects.filter(user=user,transaction_type="DEBIT",create_date__date=datetimex.today()).aggregate(Sum('amount'))['amount__sum'] > 1000000:
                errors['error'] = u'Your have exceed  daily transactions limit for unverify account (₦1000000 ), pls verify your account to continue your daily transaction'
                raise serializers.ValidationError(errors)

        return data




class KYCSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault() )

    class Meta:
        model = KYC
        fields =  ('user','First_Name','Middle_Name',"Last_Name","DOB","Gender","State_of_origin","Local_gov_of_origin","BVN","passport_photogragh")

    def validate(self, data):
        errors = {}
        user = data.get('user')


        if 100 > user.Account_Balance:
            errors['error'] = u' insufficientr balance N{} '.format(user.Account_Balance)
            raise serializers.ValidationError(errors)

        return data




class CablesubSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    package = serializers.ReadOnlyField(source='cableplan.plan_name')
    plan_amount= serializers.ReadOnlyField(source='cableplan.plan_amt')
    paid_amount = serializers.ReadOnlyField(source='plan_amount')


    class Meta:
        model = Cablesub
        fields = ('id','ident','user', 'cablename','cableplan','package','plan_amount','paid_amount', 'balance_before', 'balance_after','smart_card_number','Status','create_date', 'customer_name')


    def validate(self, data):
        errors = {}
        num = data.get('smart_card_number')
        plan =  data.get('cableplan')
        user = data.get('user')

        print(data)

        plan_amount = float(plan.plan_amount)

        service = ServicesCharge.objects.filter(service = "Cablesub").first()

        if user.user_type == "Affilliate":
                if service.Affilliate_charge  > 0.0 :
                        amount = float(plan_amount) + float(service.Affilliate_charge)

                elif service.Affilliate_discount > 0.0 :
                        amount = float(plan_amount) - (float(plan_amount) * service.Affilliate_discount/100)
                else:
                        amount = float(plan_amount)

        elif user.user_type == "TopUser":
                if service.topuser_charge  > 0.0 :
                        amount = float(plan_amount) + float(service.topuser_charge)

                elif service.topuser_discount > 0.0 :
                        amount = float(plan_amount) - (float(plan_amount) * service.topuser_discount/100)
                else:
                        amount = float(plan_amount)

        elif user.user_type == "API":
                if service.api_charge  > 0.0 :
                        amount = float(plan_amount) + float(service.api_charge)

                elif service.api_discount > 0.0 :
                        amount = float(plan_amount) - (float(plan_amount) * service.api_discount/100)

                else:
                        amount = float(plan_amount)
        else:

                    if service.charge > 0.0 :
                        amount = float(plan_amount) + float(service.charge)

                    elif service.discount > 0.0 :
                        amount = float(plan_amount) - (float(plan_amount) * service.discount/100)

                    else:
                        amount = float(plan_amount)





        if not num.isdigit():
            errors['error'] = u'invalid smart_card_number {}!'.format(num)

            raise serializers.ValidationError(errors)


        elif float(amount) >   user.Account_Balance:
            errors['error'] = u'You can\'t topup due to insufficient balance #{} '.format(user.Account_Balance)
            raise serializers.ValidationError(errors)

        elif Disable_Service.objects.get(service ="Cablesub").disable == True:
                errors['error'] = u'This Service is not currently available please check back'.format(user.Account_Balance)
                raise serializers.ValidationError(errors)

        elif not user.Phone :
            errors['error'] = u' Please add phone number to your account '
            raise serializers.ValidationError(errors)

        elif Black_List_Phone_Number.objects.filter(phone=num).exists():
              errors['error'] = u'iuc number has been Blacklist'
              raise serializers.ValidationError(errors)

        elif not Wallet_Funding.objects.filter(user = user).exists():
            errors['error'] = u'No Wallet Funding Record Found, Contact admin for more information'
            raise serializers.ValidationError(errors)


        elif Transactions.objects.filter(user=user,transaction_type="DEBIT",create_date__date=datetimex.today()).exists():
          if user.verify == False and Transactions.objects.filter(user=user,transaction_type="DEBIT",create_date__date=datetimex.today()).aggregate(Sum('amount'))['amount__sum'] >1000000:
                errors['error'] = u'Your have exceed  daily transactions limit for unverify account (₦1000000 ), pls verify your account to continue your daily transaction'
                raise serializers.ValidationError(errors)

        return data


class BillpaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    package = serializers.ReadOnlyField(source='disco_name.name')



    class Meta:
        model = Billpayment
        fields = ('id','ident','user','package','disco_name','amount','Customer_Phone','meter_number','token','MeterType','paid_amount', 'balance_before', 'balance_after','Status','create_date', 'customer_name', 'customer_address')


    def validate(self, data):
        errors = {}

        amount =  data.get('amount')
        meter =  data.get('meter_number')
        user = data.get('user')

        service = ServicesCharge.objects.filter(service = "Bill").first()

        if user.user_type == "Affilliate":
                if service.Affilliate_charge  > 0.0 :
                        paid_amount = float(amount) + float(service.Affilliate_charge)

                elif service.Affilliate_discount > 0.0 :
                        paid_amount = float(amount) - (float(amount) * service.Affilliate_discount/100)
                else:
                        paid_amount = float(amount)

        elif user.user_type == "TopUser":
                if service.topuser_charge  > 0.0 :
                        paid_amount = float(amount) + float(service.topuser_charge)

                elif service.topuser_discount > 0.0 :
                        paid_amount = float(amount) - (float(amount) * service.topuser_discount/100)
                else:
                        paid_amount = float(amount)

        elif user.user_type == "API":
                if service.api_charge  > 0.0 :
                        paid_amount = float(amount) + float(service.api_charge)

                elif service.api_discount > 0.0 :
                        paid_amount = float(amount) - (float(amount) * service.api_discount/100)

                else:
                        paid_amount = float(amount)
        else:

                    if service.charge > 0.0 :
                        paid_amount = float(amount) + float(service.charge)

                    elif service.discount > 0.0 :
                        paid_amount = float(amount) - (float(amount) * service.discount/100)

                    else:
                        paid_amount = float(amount)


        print(data)


        if paid_amount > user.Account_Balance:
            errors['error'] = u'insufficient balance,  your current balance ₦{}  '.format(user.Account_Balance)
            raise serializers.ValidationError(errors)

        elif not meter.isdigit():
            errors['error'] = u'invalid Meter number {}!'.format(meter)

            raise serializers.ValidationError(errors)

        elif Disable_Service.objects.get(service ="Bill").disable == True:
                errors['error'] = u'This Service is not currently available please check back'.format(user.Account_Balance)
                raise serializers.ValidationError(errors)

        elif Black_List_Phone_Number.objects.filter(phone=meter).exists():
              errors['error'] = u'Meter number has been Blacklist'
              raise serializers.ValidationError(errors)

        elif float(data.get('amount')) < 500:
            errors['error'] = u'BELOW MINIMUM AMOUNT ALLOWED (₦500)'
            raise serializers.ValidationError(errors)

        elif user.verify == False and  float(data.get('amount')) > 1000000:
            errors['error'] = u'Unverify User are limit to ₦1000000 naira airtime topup  per day'
            raise serializers.ValidationError(errors)

        elif Billpayment.objects.filter(user=user,create_date__date=datetimex.today()).exists():
            if user.verify == False and Billpayment.objects.filter(user=user,create_date__date=datetimex.today()).aggregate(Sum('amount'))['amount__sum'] > 1000000:
                errors['error'] = u'Your have exceed  daily transactions limit for unverify account (₦1000000 ), pls verify your account to continue your daily transaction'
                raise serializers.ValidationError(errors)

        elif not Wallet_Funding.objects.filter(user = user).exists():
            errors['error'] = u'No Wallet Funding Record Found, Contact admin for more information'
            raise serializers.ValidationError(errors)


        elif Transactions.objects.filter(user=user,transaction_type="DEBIT",create_date__date=datetimex.today()).exists():
            if user.verify == False and Transactions.objects.filter(user=user,transaction_type="DEBIT",create_date__date=datetimex.today()).aggregate(Sum('amount'))['amount__sum'] > 1000000:
                errors['error'] = u'Your have exceed  daily transactions limit for unverify account (₦1000000 ), pls verify your account to continue your daily transaction'
                raise serializers.ValidationError(errors)


        return data




class Airtime_fundingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    plan_network = serializers.ReadOnlyField(source='plan_net')


    class Meta:
        model = Airtime_funding
        fields = ('id','ident','user','use_to_fund_wallet','plan_network','network','mobile_number','amount','Receivece_amount','Status','create_date')


    def validate(self, data):
        errors = {}
        Mtn= ["0702","0704","0706",'0703','0903','0906','0706','0803','0806','0810','0813','0816','0814']
        ETISALATE =  ['0809','0817','0818','0909','0908']
        GLO = ['0705','0805','0811','0807','0815','0905']
        AIRTEL = ['0708','0802','0808','0812','0907','0701','0902','0901',"0904"]


        amount =  data.get('amount')
        num =  data.get('mobile_number')
        net =  data.get('network')
        user = data.get('user')

        print(data)


        if net == '9MOBILE' and not num.startswith(tuple(ETISALATE)):

                errors['error'] = u'Please check entered number is not 9MOBILE user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif net == 'MTN' and not num.startswith(tuple(Mtn)):
                errors['error'] = u'Please check entered number is not MTN user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif net == 'GLO' and not num.startswith(tuple(GLO)):
                errors['error'] = u'Please check entered number is not GLO user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif net == 'AIRTEL' and not num.startswith(tuple(AIRTEL)):
                errors['error'] = u'Please check entered number is not AIRTEL user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif not num.isdigit():
            errors['error'] = u'invalid mobile number {}!'.format(num)

            raise serializers.ValidationError(errors)


        elif float(data.get('amount')) < 500:
            errors['error'] = u'BELOW MINIMUM AMOUNT ALLOWED (₦500)'
            raise serializers.ValidationError(errors)

        elif Disable_Service.objects.get(service ="Airtime_Funding").disable == True:
               errors['error'] = u'This Service is not currently available please check back'
               raise serializers.ValidationError(errors)

        return data


class CouponPaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )


    class Meta:
        model = CouponPayment
        fields = ('id','user', 'Code','amount','Status','create_date' )


    def validate(self, data):
        errors = {}
        Code = data.get('Code')

        print(data)

        if not Couponcode.objects.filter(Coupon_Code =Code).exists():#exists()
            errors['error'] = u'Invalid Coupon code note that its case sensetive{}!'.format(Code)
            raise serializers.ValidationError(errors)


        elif Couponcode.objects.filter(Coupon_Code =Code, Used =True).exists():
            errors['error'] = u'This Coupon code has been used {}'.format(Code)
            raise serializers.ValidationError(errors)


        return data


class DataSerializer(ModelSerializer):
    #user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    plan_name= serializers.ReadOnlyField(source='plan.plan_name')
    plan_amount= serializers.ReadOnlyField(source='data_amount')
    plan_network= serializers.ReadOnlyField(source='plan.plan_net')
    Ported_number= serializers.BooleanField()



    class Meta:
        model = Data
        fields =  ('user','id','network','ident','balance_before','balance_after','mobile_number','plan','Status','plan_network','plan_name','plan_amount','create_date',"Ported_number")


    def validate(self, data):
        errors = {}
        Mtn= ["0702","0704","0706",'0703','0903','0906','0706','0803','0806','0810','0813','0816','0814']
        ETISALATE =  ['0809','0817','0818','0909','0908']
        GLO = ['0705','0805','0811','0807','0815','0905']
        AIRTEL = ['0702','0708','0802','0808','0812','0907','0701','0902','0901',"0904"]
        num = data.get('mobile_number')
        amount =  data.get('plan')
        user = data.get('user')
        net = data.get('network')
        plan = data.get('plan')
        Ported_number  = data.get('Ported_number')

        print(Ported_number)


        if user.user_type == "Affilliate":
               amount = float(plan.Affilliate_price)

        elif user.user_type == "API":
                amount = float(plan.api_price)

        elif user.user_type == "TopUser":

               amount = float(plan.TopUser_price)
        else:
                amount = float(plan.plan_amount)


        print(data)

        if len(str(num)) != 11   :
            errors['error'] = u'invalid mobile number {}!'.format(num)
            raise serializers.ValidationError(errors)

        elif Ported_number !=  True and net.name == '9MOBILE' and not num.startswith(tuple(ETISALATE)):

                errors['error'] = u'Please check entered number is not 9MOBILE user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif Ported_number !=  True and net.name == 'MTN' and not num.startswith(tuple(Mtn)):
                errors['error'] = u'Please check entered number is not MTN user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif Ported_number !=  True and net.name == 'GLO' and not num.startswith(tuple(GLO)):
                errors['error'] = u'Please check entered number is not GLO user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif Ported_number !=  True and net.name == 'AIRTEL' and not num.startswith(tuple(AIRTEL)):
                errors['error'] = u'Please check entered number is not AIRTEL user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif plan.plan_type == "GIFTING" and Network.objects.get(name=net).gifting_disable == True:
              errors['error'] = u'Gifting Data not available on this network currently'
              raise serializers.ValidationError(errors)

        elif plan.plan_type == "CORPORATE GIFTING" and Network.objects.get(name=net).corporate_gifting_disable == True:
              errors['error'] = u'CORPORATE Gifting Data not available on this network currently'
              raise serializers.ValidationError(errors)

        elif plan.plan_type == "SME" and Network.objects.get(name=net).sme_disable == True:
              errors['error'] = u'SME Data not available on this network currently'
              raise serializers.ValidationError(errors)

        elif not num.isdigit():
            errors['error'] = u'invalid mobile number {}!'.format(num)

            raise serializers.ValidationError(errors)

        elif not Wallet_Funding.objects.filter(user = user).exists():
            errors['error'] = u'No Wallet Funding Record Found, Contact admin for more information'
            raise serializers.ValidationError(errors)


        elif Network.objects.get(name=net.name).data_disable == True:
              errors['error'] = u'Data not available on this network currently'
              raise serializers.ValidationError(errors)

        elif Disable_Service.objects.get(service ="Data").disable == True:
               errors['error'] = u'This Service is not currently available please check back'
               raise serializers.ValidationError(errors)

        elif Black_List_Phone_Number.objects.filter(phone=num).exists():
              errors['error'] = u'Phone number has been Blacklist'
              raise serializers.ValidationError(errors)


        elif not  Plan.objects.filter (network =net).filter(id=plan.id).exists():
            errors['error'] = u'invalid plan id {} for {}, check here for available plan list '.format(plan.id,net)
            raise serializers.ValidationError(errors)

        elif float(amount) >user.Account_Balance:
            errors['error'] = u'You can\'t purchase this plan due to insufficient balance  ₦{} Kindly Fund your Wallet'.format(user.Account_Balance)
            raise serializers.ValidationError(errors)

        elif user.verify == False and  float(amount) > 1000000:
            errors['error'] = u'Unverify User are limit to 1000000 naira datatopup topup  per day'
            raise serializers.ValidationError(errors)

        elif Transactions.objects.filter(user=user,transaction_type="DEBIT",create_date__date=datetimex.today()).exists():
            if user.verify == False and Transactions.objects.filter(user=user,transaction_type="DEBIT",create_date__date=datetimex.today()).aggregate(Sum('amount'))['amount__sum'] > 1000000:
                errors['error'] = u'Your have exceed  daily transactions limit for unverify account (₦1000000 ), pls verify your account to continue your daily transaction'
                raise serializers.ValidationError(errors)



        return data



class AirtimeTopupSerializer(ModelSerializer):
        #user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    plan_amount= serializers.ReadOnlyField(source='plan_amt')
    plan_network= serializers.ReadOnlyField(source='plan_net')
    Ported_number= serializers.BooleanField()


    class Meta:
        model = AirtimeTopup
        fields =  ('user','id','ident','airtime_type','network','airtime_type','paid_amount','mobile_number','amount','plan_amount','plan_network','balance_before','balance_after','Status','create_date',"Ported_number")


    def validate(self, data):
        errors = {}
        Mtn= ["0706",'0703','0704','0903','0906','0706','0803','0806','0810','0813','0816','0814']
        ETISALATE =  ['0809','0817','0818','0909','0908']
        GLO = ['0705','0805','0811','0807','0815','0905']
        AIRTEL = ['0702','0708','0802','0808','0812','0907','0701','0902','0901']

        num = data.get('mobile_number')
        amount =  data.get('amount')
        amt =  data.get('amount')
        user = data.get('user')
        net = data.get('network')
        Ported_number  = data.get('Ported_number')
        airtime_type = data.get("airtime_type")
        print(Ported_number)
        print(Ported_number)

        if user.user_type == "Affilliate":
               perc = TopupPercentage.objects.get(network = Network.objects.get(name=net)).Affilliate_percent
               perc2 = TopupPercentage.objects.get(network = Network.objects.get(name=net)).share_n_sell_affilliate_percent

        elif user.user_type == "API":
              perc = TopupPercentage.objects.get(network = Network.objects.get(name=net)).api_percent
              perc2 = TopupPercentage.objects.get(network = Network.objects.get(name=net)).share_n_sell_api_percent

        elif user.user_type == "TopUser":

              perc = TopupPercentage.objects.get(network = Network.objects.get(name=net)).topuser_percent
              perc2 = TopupPercentage.objects.get(network = Network.objects.get(name=net)).share_n_sell_topuser_percent
        else:
              perc = TopupPercentage.objects.get(network = Network.objects.get(name=net)).percent
              perc2 = TopupPercentage.objects.get(network = Network.objects.get(name=net)).share_n_sell_percent


        if airtime_type == "VTU":
             amount = float(amount) * int(perc)/100

        else:
             amount = float(amount) * int(perc2)/100


        if float(amount) >user.Account_Balance:
            errors['error'] = u'You can\'t topup due to insufficient balance  ₦{} '.format(user.Account_Balance)
            raise serializers.ValidationError(errors)

        elif float(data.get('amount')) < 50:
            errors['error'] = u'minimum airtime topup is ₦50'
            raise serializers.ValidationError(errors)

        elif user.verify == False and  float(amount) > 1000000:
            errors['error'] = u'Unverify User are limit to ₦1000000  airtime topup  per day'
            raise serializers.ValidationError(errors)

        elif airtime_type == "Share and Sell" and float(data.get('amount')) < 100:
            errors['error'] = u'minimum airtime share and sell topup is ₦100'
            raise serializers.ValidationError(errors)


        elif len(str(num)) != 11   :
            errors['error'] = u'invalid mobile number {}!'.format(num)

            raise serializers.ValidationError(errors)

        elif not num.isdigit():
            errors['error'] = u'invalid mobile number {}!'.format(num)

            raise serializers.ValidationError(errors)

        elif Ported_number !=  True and  net.name == '9MOBILE' and not num.startswith(tuple(ETISALATE)):

                errors['error'] = u'Please check entered number is not 9MOBILE user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif  Ported_number !=  True and net.name == 'MTN' and not num.startswith(tuple(Mtn)):
                errors['error'] = u'Please check entered number is not MTN user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif  Ported_number !=  True and net.name == 'GLO' and not num.startswith(tuple(GLO)):
                errors['error'] = u'Please check entered number is not GLO user {}!'.format(num)
                raise serializers.ValidationError(errors)

        elif  Ported_number !=  True  and net.name == 'AIRTEL' and not num.startswith(tuple(AIRTEL)):
                errors['error'] = u'Please check entered number is not AIRTEL user {}!'.format(num)
                raise serializers.ValidationError(errors)


        elif Network.objects.get(name=net.name).airtime_disable == True:
              errors['error'] = u'Airtime is  not available on this network currently'
              raise serializers.ValidationError(errors)

        elif airtime_type == "Share and Sell" and Network.objects.get(name=net.name).share_and_sell_disable == True:
              errors['error'] = u'Airtime share and sell is not available on this network currently'
              raise serializers.ValidationError(errors)

        elif Disable_Service.objects.get(service ="Airtime").disable == True:
               errors['error'] = u'This Service is not currently available please check back'
               raise serializers.ValidationError(errors)

        elif AirtimeTopup.objects.filter(user=user,create_date__date=datetimex.today()).exists():
            if user.verify == False and AirtimeTopup.objects.filter(user=user,create_date__date=datetimex.today()).aggregate(Sum('amount'))['amount__sum'] > 1000000:
                errors['error'] = u'Your have exceed  daily transactions limit for unverify account (₦1000000 ), pls verify your account to continue your daily transaction'
                raise serializers.ValidationError(errors)

        elif Black_List_Phone_Number.objects.filter(phone=num).exists():
              errors['error'] = u'Phone number has been Blacklist'
              raise serializers.ValidationError(errors)

        elif not Wallet_Funding.objects.filter(user = user).exists():
            errors['error'] = u'No Wallet Funding Record Found, Contact admin for more information'
            raise serializers.ValidationError(errors)

        elif Transactions.objects.filter(user=user,transaction_type="DEBIT",create_date__date=datetimex.today()).exists():
            if user.verify == False and Transactions.objects.filter(user=user,transaction_type="DEBIT",create_date__date=datetimex.today()).aggregate(Sum('amount'))['amount__sum'] > 1000000:
                errors['error'] = u'Your have exceed  daily transactions limit for unverify account (₦1000000 ), pls verify your account to continue your daily transaction'
                raise serializers.ValidationError(errors)




        return data