from.models import *


def categories_processor(request):

    config = WebsiteConfiguration.objects.all().first()
    # config = ""
    net = Network.objects.all()
    checkbank = Disable_Service.objects.get(service="Bankpayment").disable
    monnifybank = Disable_Service.objects.get(service="Monnfy bank").disable
    monnifyATM = Disable_Service.objects.get(service="Monnify ATM").disable
    paystack = Disable_Service.objects.get(service="paystack").disable
    aircash = Disable_Service.objects.get( service="Airtime_Funding").disable

    return {"banks":BankAccount.objects.all(), "networks":net,'whatsapp_group_link': config.whatsapp_group_link ,"support_phone":config.support_phone_number,"air2cash": aircash,"bank2": checkbank,"monnifyatm2": monnifyATM, "paystack2": paystack,"monnifybank2": monnifybank}
