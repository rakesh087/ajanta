from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import Account, Stock, Order, Procucts
from .forms import ForgotPassword, CapturePassword, Register, GetOrder, OrderStatus, ProductSearch
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from datetime import date
# This view is for login page
def user_login(request):
    if request.method=="POST":
        form_data=request.POST
        fm=AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            username=fm.cleaned_data['username']
            password=fm.cleaned_data['password']
            #queryset = Account.objects.filter(username=username,mobile_number=mobile_number).values('email', 'mobile_number','username')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print('user id and password is correct')
                if request.GET.get('next',None):
                    return HttpResponseRedirect(request.GET['next'])
                else:
                    #return render(request,'woodshophome/home1.html')
                    #login_popup.html
                    return render(request,'woodshophome/login.html')
        else:
            print('invalid form, rendering login form again')
            form={'form':fm,}
            return render(request,'woodshophome/login.html',form)
    else:
        print('rendering login form')
        fm=AuthenticationForm(request=request,data=request.POST)
        form={'form':fm}
        return render(request,'woodshophome/login.html',form)

#this is for for validating user id and mobile number for resetting password
def forgot_password(request):
    if request.method=="POST":
        print('getting data from form for validation')
        data=request.POST
        print('data is: ',data)
        username=data['username']
        mobile_number=data['mobile_number']
        print('user name is: ',username)
        print('modile number  is: ',mobile_number)
        d={'username':username,'mobile_number':mobile_number}
        request.session['session_data']=d
        #fm=CapturePassword()                  
        #form={'form':fm}                     
        #return render(request,'woodshophome/capture_password.html',form) 
        queryset = Account.objects.filter(username=username,mobile_number=mobile_number).values('email', 'mobile_number','username')
        if not queryset.exists():
            messages.warning(request, 'Please enter valid email id and mobile number')
            fm=ForgotPassword()
            form={'form':fm}
            return render(request,'woodshophome/forget_password.html',form)
        else:
            print('^^^^^^^^^^^^^^')
            print('data in queryset')
            print('user name is: ',queryset[0]['username'])
            name=username
            mobile_number=mobile_number
            d={'name':name,'mobile_number':mobile_number}
            request.session['session_data']=d
            print('user name is: ',name)
            return redirect('woodshophome:capture-password')
    else:
        #need to rende form
        print('rendering forget password html page')
        fm=ForgotPassword()
        form={'form':fm}
        return render(request,'woodshophome/forget_password.html',form)

#this view is for capturing new password if user id and mobile number are validated successfully
def capture_password(request):
    print('this is capture_password view')
    session_data=request.session.get('session_data',default="Guest")
    if request.method=="POST":
        data=request.POST
        password1=data['password1']
        password2=data['password2']
        if password2==password2:
            #both password matched now update password in DB
            #return HttpResponse('password changed successfully')
            print(session_data)
            print(session_data['name'])
            queryset=Account.objects.get(username=session_data['name'],mobile_number=session_data['mobile_number'])
            queryset.set_password(password1)
            queryset.save()
            messages.success(request, 'Password changed successfully!!')
            del request.session['session_data']
            return redirect('woodshophome:login')
        else:
            messages.warning(request,"password didn't matched, password file is case sensitive")
            fm=CapturePassword()
            xyz={'form':fm,'item_name':'chairt',}
            return render(request,'woodshophome/capture_password.html',xyz)
        
    else:
        fm=CapturePassword()
        form={'form':fm}
        return render(request,'woodshophome/capture_password.html',form)

#this view is for user registration
def signup(request):
    if request.method=='POST':
        fm=Register(request.POST)
        data=request.POST
        print('-----------------validating form-----------------')
        if fm.is_valid():
            print('forms is valid')
            fm.save()
            form={'form':fm,}
            #return HttpResponse('this is signup form')
            return redirect('woodshophome:login')
            #return render(request,'login/signup.html',form)
        else:
            form={'form':fm}
            return render(request,'woodshophome/signup.html',form)
    else:
        fm=Register()
        form={'form':fm}
        return render(request,'woodshophome/signup.html',form)

#this view is for loghout
def user_logout(request):
    logout(request)
    return redirect('woodshophome:woodshophome-home')

def place_order(request):
    print('place order form view')
    if request.user.is_authenticated:
        #render form for capturing order and get the order details
        if request.method=="POST":
            #Get the order and save in database
            fm=GetOrder(request.POST)
            data=request.POST
            if fm.is_valid():
                print('username of placcing user is: ', request.user)
                queryset = Account.objects.filter(username=request.user).values('id')
                username_id=''
                print('queryset is: ',queryset)
                #item_selected=fm.cleaned_data['dropdown-item']
                #print(item_selected)
                print(data['dropdown-item'])
                for each in queryset:
                    username_id=each['id']
                account = Account.objects.get(pk=username_id)
                order=Order(order_item=data['dropdown-item'],username=account,order_unit=data['order_unit'],order_date=date.today())
                order.save()
                messages.success(request, 'Thanyou for placing order')
                return redirect('woodshophome:woodshophome-home')
                #return HttpResponse('valid form data')

        else:
            print('this is getting oprder form')
            products=[]
            queryset = Stock.objects.values('product_name')
            for each in queryset:
                products.append(each['product_name'])
                #print('product name is: ',each['product_name'])
            print(queryset)
            fm=GetOrder()
            print(products)
            form={'form':fm,'item_name':products}
            return render(request,'woodshophome/capture_order.html',form)
            #return HttpResponse('this is getting oprder form')
            #render form for getting new order

    else:
        return redirect('woodshophome:login')

#this view is for checking order status and my order
@login_required
def order_status(request):
    print('order id is: ',id)
    if request.user.is_authenticated:
        print('username of tracking user is: ', request.user)
        queryset = Account.objects.filter(username=request.user).values('id')
        username_id=''
        for each in queryset:
            username_id=each['id']
            print(username_id)
        account = Account.objects.get(pk=username_id)
        order=Order.objects.all().filter(username=username_id).values('id','order_status','order_date')
        print(order)
        print('printing order details for user', request.user)
        #order_info=[]
        order_data=[]
        for each in order:
            #print(each)
            l=[]
            l.append(each['id'])
            l.append(each['order_status'])
            if each['order_date']==None:
                l.append('')
            else:
                l.append(each['order_date'])
            order_data.append(l)
        order_details={'order_info':order_data}
        return render(request,'woodshophome/order_status.html',order_details)
    else:
        #redirect to login page
        return redirect('woodshophome:login')

def order_status_details(request,id):
    print('oder id is: ',id)
    queryset=Order.objects.filter(pk=id).values('order_item','order_unit','order_date','order_desc','order_status')
    print(queryset)
    order_info=[]
    for each in queryset:
        l=[]
        l.append(each['order_item'])
        l.append(each['order_unit'])
        l.append(each['order_date'])
        l.append(each['order_desc'])
        order_info.append(l)
    order_details={'order_info':order_info,}
    return render(request,'woodshophome/order1_full_details.html',order_details)
    return HttpResponse('this is full details')

#this is for home page
def home(request):
    if request.method=="POST":
        #the the form data
        print('trying to get data from form')
        product_name=request.POST['product_name']
        print('product name is: ',product_name)
        qs=Procucts.objects.all().filter(product_name__icontains=product_name)
        if len(qs)==0:
            print('Opps no data found')
            fm=ProductSearch(request.POST)
            form={'form':fm}
            return render(request,'woodshophome/show_products.html',form)
        else:
            prod={}
            for each in qs:
                print(each.product_id,each.product_name, each.prduct_img_path,each.product_brand,each.pk)
                #will create a dictionary based on product_id, each key(product-id) will have all details for that products
                prod[each.product_id]=[each.product_name,each.prduct_img_path,each.product_brand,each.product_description,each.product_model,each.pk]
            fm=ProductSearch(request.POST)
            form={'form':fm,'prod':prod}
            return render(request,'woodshophome/show_products.html',form)
    else:
        fm=ProductSearch(request.POST)
        form={'form':fm}
        return render(request,'woodshophome/home.html',form)

def show_selected_prod(request,id,*args):
    if request.method=="POST":
        print('this is for seacrhing products')

    else:
        print('this is for displaying form')
        qs=Procucts.objects.get(id=id)
        prod={}
        print('got queryset is: ',qs)
        print(qs.product_id)
        print(qs.product_name)
        prod[qs.product_id]=[qs.product_name,qs.prduct_img_path,qs.product_brand,qs.product_description,qs.product_model]
        # for each in qs:
        #     print(each.product_id,each.product_name, each.prduct_img_path,each.product_brand,each.pk)
        #     #will create a dictionary based on product_id, each key(product-id) will have all details for that products
        #     prod[each.product_id]=[each.product_name,each.prduct_img_path,each.product_brand,each.product_description,each.product_model,each.pk]
        fm=ProductSearch(request.POST)
        form={'form':fm,'prod':prod}
        return render(request,'woodshophome/show_selected_prod_detail.html',form)