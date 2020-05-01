from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.
import random
from accounts.models import Employee
from paypal.standard.forms import PayPalPaymentsForm

from .models import Invoice
from accounts.models import Client
from django.contrib.auth.models import User

from django.conf import settings
import stripe


stripe_pub  = settings.STRIPE_PUBLIC_KEY
stripe_private = settings.STRIPE_PRIVATE_KEY
stripe.api_key = stripe_private

def checkout(request):
    if request.user.is_authenticated:
        order_id = None
        return render(request,'checkout_home.html',{'order_id':order_id})
    return redirect('login')

def payhome(request):
    if request.POST.get('submit')=='button2':
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        email = request.POST.get('email')
        service = request.POST.get('service')
        stylist = request.POST.get('stylist')
        date = request.POST.get('date')
        time = request.POST.get('time')
        context = {
            'order_id':order_id,
            'amount':amount,
            'name':name,
            'email':email,
            'service':service,
            'stylist':stylist,
            'date':date,
            'time':time,
            'next':True,
        }
        return render(request,'login.html',context=context)
    
    if request.POST.get('submit')=='button3' and request.user.is_authenticated:
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        email = request.POST.get('email')
        service = request.POST.get('service')
        stylist = request.POST.get('stylist')
        date = request.POST.get('date')
        time = request.POST.get('time')
        request.session['amount'] = int(float(amount))
        
        obj = Invoice.objects.create(order_id=order_id,name=name,email=email,service=service,stylist=stylist,date=date,time=time,bill=amount)
        context = {
            'key':stripe_pub,
            'amount':float(amount)*100,
            'desp':service,
        }
        return render(request,'stripe_home.html',context=context)
    
    if request.POST.get('submit')=='button1' and request.user.is_authenticated:
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        email = request.POST.get('email')
        service = request.POST.get('service')
        stylist = request.POST.get('stylist')
        date = request.POST.get('date')
        time = request.POST.get('time')

        obj = Invoice.objects.create(order_id=order_id,name=name,email=email,service=service,stylist=stylist,date=date,time=time,bill=amount)

        paypal_dict = {
            "business": "example@gmail.com",
            "amount": amount,
            "item_name": service,
            "invoice": order_id,
            "notify_url": 'http://127.0.0.1:8000/hardurl',#"https://johnhairsalon.herokuapp.com/hardurl",#
            "return": 'http://127.0.0.1:8000/paymentreturn',#"https://johnhairsalon.herokuapp.com/paymentreturn",#
            "cancel_return": 'http://127.0.0.1:8000/paymentcancel',#"https://johnhairsalon.herokuapp.com/paymentcancel", #

        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {
            'form':form
        }

        return render(request,'payment_home.html',context=context)
    
    return redirect('home')

@csrf_exempt
def payreturn(request):
    print("Return krk aaya")
    user = request.user
    email = user.email
    order_id = request.POST.get('order_id')
    invoice = Invoice.objects.filter(order_id=order_id).first()
    invoice.paid = True
    invoice.save()
    args = {'post':request.POST,'get':request.GET}
    return render(request,'payment_return.html',args)


def paycancel(request):
    return redirect('home')



def stripecheckout(request):
    print("Here")
    print(request.POST)
    amount = int(request.session.get('amount'))
    customer = stripe.Customer.create(
        email=request.POST.get('stripeEmail'),
        source=request.POST.get('stripeToken')
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Payment'
    )
    
    return render(request,'stripe_success.html',{'amount':amount})

def stripesuccess(request):
    return render(request,'stripe_success.html')
