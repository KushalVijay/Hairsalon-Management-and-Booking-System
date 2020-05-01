from django.contrib.auth import authenticate, login, get_user_model,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from .models import Client,Store,Employee
from payment.models import Salarie

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import generate_token
from django.contrib.auth.models import User

class ActivateAccount(View):
    def get(self,request,uidb64,token,status):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if user is not None:
                if status=='store':
                    obj = Store.objects.filter(user=user).first()
                elif status=='employee':
                    obj = Employee.objects.filter(user=user).first()
                else:
                    obj = Client.objects.filter(user=user).first()
        except Exception:
            user = None

        if user is not None and generate_token.check_token(user,token):
            obj.active = True
            obj.save()
            messages.info(request,'Account Verified.Please login')
            return redirect('login')

        return render(request,'activate_fail.html',status=401)



def send_activation(request,user,status):

    current_site = get_current_site(request)
    email_sub = "Activate your Account"
    message = render_to_string('activate.html',
               {
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user),
                'status':status
               }
               )
    email_message = EmailMessage(
        email_sub,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    
    email_message.send()

def RegisterUser(request):

    if request.method=='POST':
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')

        status = request.POST.get('status')
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
        except:
            messages.info(request,"User already exists")
            redirect('login')
        print(user,user.pk,urlsafe_base64_encode(force_bytes(user.pk)))
        if status=='store':
            obj = Store.objects.create(user=user,contact=contact,active=False)
            send_activation(request,user,status)
        elif status=='employee':
            obj = Employee.objects.create(user=user,contact=contact,active=False)
            send_activation(request, user, status)
        else:
            obj = Client.objects.create(user=user,contact=contact,active=False)
            send_activation(request, user, status)

        messages.info(request,"Verification mail is sent to email provided.Please Login post verification")

        return redirect('login')
    return render(request,'register.html')



def LoginUser(request):

    if request.method=='POST':
        request.session['status'] = None
        status = request.POST.get('status')
        email = request.POST.get('email')
        password = request.POST.get('password')
        flag = 0
        user  = User.objects.filter(username=email).first()

        if status=='store':
            obj = Store.objects.filter(user=user).first()
            try:
                if obj.active:
                    user = authenticate(request,username=email,password=password)
                    if user is not None:
                        login(request,user)
                        request.user = user
                        request.session['status'] = True
                        return redirect('dashboard')
                    else:
                        messages.info(request,"Invalid Credentials.Make sure you have already registered.")
                        return redirect('login')
            except:
                messages.info(request,"Make sure you have already registered and activated your account")
                return redirect('login')
        elif status=='employee':
            obj = Employee.objects.filter(user=user).first()
            try:
                if obj.active:
                    user = authenticate(request, username=email, password=password)
                    if user is not None:
                        login(request, user)
                        request.user = user
                        return redirect('home')
                    else:
                        messages.info(request, "Invalid Credentials.Make sure you have already registered.")
                        return redirect('login')
            except:
                messages.info(request, "Make sure you have already registered and activated your account")
                return redirect('login')
        else:
            obj = Client.objects.filter(user=user).first()
            try:
                if obj.active:
                    user = authenticate(request, username=email, password=password)
                    if user is not None:
                        login(request, user)
                        request.user = user
                        return redirect('home')
                    else:
                        messages.info(request, "Invalid Credentials.Make sure you have already registered.")
                        return redirect('login')
            except:
                messages.info(request, "Make sure you have already registered and activated your account")
                return redirect('login')
    return render(request,'login.html')



def dashboard(request):
    emp_name = None
    emp_info = None
    sal_info = None
    if request.method=='POST':
        emp_name = request.POST.get('emp_name')
        emp_info = Employee.objects.filter(name=emp_name)[0]
        sal_info = Salarie.objects.filter(user=emp_info)[0]
        print(sal_info)
    user = request.user
    store = Store.objects.filter(user=user).first()
    store_name = store.name
    employees_ = Employee.objects.all()
    employees = []
    for i in employees_:
        if i.store == store:
            employees.append(i.name)
    context = {
        'store_name':store_name,
        'emp_name':emp_name,
        'emp_info':emp_info,
        'employees':employees,
        'sal_info':sal_info,
    }
    return render(request,'dashboard.html',context=context)
    

def Logout_view(request):

    logout(request)
    return redirect("home")


def password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        newpass = request.POST.get('newpass')
        try:
            obj = User.objects.filter(username=email).first()
            obj.set_password(newpass)
            obj.save()
            messages.info(request,'Password successfully changed,Please login now')
            return redirect('login')
        except:
            messages.info(request, "Account with this email does not exists.Make a new one")
            return redirect('password')


    return render(request, 'password_change.html')

