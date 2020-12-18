from django.shortcuts import render,redirect
from .models import *
from django.core.mail import send_mail
import random
from django.conf import settings
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def initiate_payment(request):
    try: 
        amount = int(request.POST['amount'])
        user = User.objects.get(email=request.session['email'])
    except:
        return render(request, 'mycart.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY
    print(settings.PAYTM_MERCHANT_ID)
    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', "sjm05990@gmail.com"),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'payments/redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'payments/callback.html', context=received_data)
        return render(request, 'payments/callback.html', context=received_data)


def home(request):
    return render(request,'home.html')

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def blog(request):
    return render(request,'blog.html')

def seller_index(request):
    return render(request,'seller_index.html')

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        telephone = request.POST['telephone']
        message = request.POST['message']

        Contact.objects.create(name=name,email=email,telephone=telephone,message=message)
        msg = "Contact Saved Successfully"
        return render(request,'contact.html',{'msg':msg})

    else:
        return render(request,'contact.html')

def detail(request):
    return render(request,'detail.html')

def shop_detail(request):
    return render(request,'shop_detail.html')

def shop(request):
    return render(request,'shop.html')

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        usertype = request.POST['usertype']

        try:
            user = User.objects.get(email=email,password=password)
            if usertype=="user":
                try:
                    user = User.objects.get(email=email,password=password,usertype=usertype)
                    request.session['email'] = user.email
                    request.session['fname'] = user.fname
                    request.session['user_image'] = user.user_image.url
                    wishlists = Wishlist.objects.filter(user=user)
                    request.session['total_wishlist']=len(wishlists)
                    carts = Cart.objects.filter(user=user)
                    request.session['total_cart']=len(carts)
                    return render(request,'index.html')                
                except Exception as e:
                    print("EXCEPTION : ",e)
                    msg = "Please Select Proper Usertype"
                    return render(request,'login.html',{'msg':msg})
            
            elif usertype=="seller":
                print("seller")
                try:
                    user = User.objects.get(email=email,password=password,usertype=usertype)
                    print("try")
                    request.session['email'] = user.email
                    request.session['fname'] = user.fname
                    request.session['user_image'] = user.user_image.url
                    return render(request,'seller_index.html')                
                except Exception as e:
                    print("seller : ",e)
                    msg = "Please Select Proper Usertype"
                    return render(request,'login.html',{'msg':msg})
        except:
            msg = "Email Id Or Password Is Incorrect"
            return render(request,'login.html',{'msg':msg})            
    else:
        return render(request,'login.html')

def signup(request):
    if request.method == "POST":
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        m = request.POST['mobile']
        p = request.POST['password']
        cp = request.POST['cpassword']
        ut = request.POST['usertype']
        ui = request.FILES['user_image']

        try:
            user = User.objects.get(email=e)
            if user:
                msg = "Email Id Already Registered"
                return render(request,'signup.html',{'msg':msg,'f':f,'l':l,'p':p,'m':m,'cp':cp,'ui':ui})

        except:
            if p == cp:
                User.objects.create(fname=f,lname=l,email=e,mobile=m,password=p,cpassword=cp,usertype=ut,user_image=ui)
                rec = [e,]
                subject = "OTP For Jewelshop Registration"
                otp = random.randint(1000,9999)
                message = "OTP For Successfull Registration Is" + str(otp)
                email_from = settings.EMAIL_HOST_USER
                send_mail(subject,message,email_from,rec)
                return render(request,'otp.html',{'email':e,'otp':otp})
            
            else:
                msg = "Password and Confirm Password did not match"
                return render(request,'signup.html',{'msg':msg,'f':f,'l':l,'e':e,'m':m,'ui':ui})

    else:
        return render(request,'signup.html')
    

def validate_otp(request):
        myvar = ""
        email = request.POST['email']
        otp = request.POST['otp']
        uotp = request.POST['uotp']

        try:
            myvar=request.POST['myvar']

        except:
            pass 

        if otp == uotp and myvar == "forgot_password":
            return render(request,'enter_new_password.html',{'email':email})
            
        elif otp == uotp:
            try:    
                user = User.objects.get(email=email)
                user.save()
                msg = "Sign Up Successfull"
                return render(request,'login.html',{'msg':msg})

            except:
                pass

        else:
            msg = "OTP Verification Failed"
            return render(request,'otp.html',{'msg':msg,'email':email,'otp':otp})

def logout(request):
    try:
        del request.session['fname']
        del request.session['email']
        return render(request,'home.html')
    
    except:
        return render(request,'home.html')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
            rec = [email,]
            subject = "OTP For Forgot Password"
            otp = random.randint(1000,9999)
            message = "OTP For Forgot Password Is" + str(otp)
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject,message,email_from,rec)
            myvar = "forgot_password"
            return render(request,'otp.html',{'email':email,'otp':otp,'myvar':myvar})
        
        except:
            msg = "Email Id Does Not Exists"
            return render(request,'enter_email.html',{'msg':msg})
    else:
        return render(request,'enter_email.html')

def update_password(request):
    
    email = request.POST['email']
    npassword = request.POST['npassword']
    cnpassword = request.POST['cnpassword']

    if npassword == cnpassword:
        user = User.objects.get(email=email)        
        user.password=npassword
        user.cpassword=cnpassword
        user.save()            
        msg = "Password Updated Successfully"
        return render(request,'login.html',{'msg':msg})        
                            
    else:
        msg = "New Password And Confirm New Password Did Not Matched"
        return render(request,'enter_new_password.html',{'msg':msg,'email':email})

def change_password(request):
    if request.method == "POST":
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        cnew_password = request.POST['cnew_password']

        user = User.objects.get(email=request.session['email'])
        if old_password == user.password:
            if new_password == cnew_password:
                user.password = new_password
                user.cpassword = cnew_password
                user.save()
                return request('logout')

            else:    
                msg = "New Password And Confirm New Password Did Not Matched"
                return render(request,'change_password.html',{'msg':msg})
        else:
            msg = "Old Password Did Not Matched" 
            return render(request,'change_password.html',{'msg':msg})
    
    else:
        return render(request,'change_password.html')

def profile(request):
    if request.method == "POST":
        user = User.objects.get(email=request.session['email'])
        user.fname = request.POST['fname']
        user.lname = request.POST['lname']
        user.email = request.POST['email']
        user.mobile = request.POST['mobile']

        try:
            if request.FILES['user_image']:
                print("FILE")
                if user.usertype == "seller":
                    print("SELLER1")
                    data = "seller_header.html"
                    user.user_image = request.FILES['user_image']
                    user.save()
                    request.session['user_image'] = user.user_image.url
                    return render(request,'seller_index.html',{'data':data,'user':user})                
                else:
                    user.user_image = request.FILES['user_image']
                    user.save()
                    request.session['user_image'] = user.user_image.url
                    return render(request,'index.html',{'user':user})
            
        except:
            if user.usertype == "seller":
                print("SELLER2")
                data = "seller_header.html"
                user.save()
                return render(request,'seller_index.html',{'data':data,'user':user})                
            else:
                user.save()
                return render(request,'index.html',{'user':user})

    else: 
        user = User.objects.get(email=request.session['email'])
        if user.usertype == "seller":
            print("SELLER3")
            data = "seller_header.html"
            return render(request,'profile.html',{'user':user,'data':data})        
        else:
            return render(request,'profile.html',{'user':user})

def add_gold_jewelry(request):
    if request.method == "POST":

        user = User.objects.get(email=request.session['email'])
        gcat = request.POST['gold_category']
        print("Gold Categoty : ",gcat)
        # if gcat=="rings":
        #      size=[9,10,11,12]

        # elif gcat == "necklace":
        #      size=[2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,2.10,2.11,2.12]
            
        gna = request.POST['gold_name']
        gpr = request.POST['gold_price']
        gdc = request.POST['gold_des_code']
        gg = request.POST['gold_gross']
        gne = request.POST['gold_net']
        gsw  = request.POST['gold_stone_wt']
        ggen = request.POST['gold_gender']
        gmc = request.POST['gold_metal_colour']
        gpu = request.POST['gold_purity']
        gcert = request.POST['gold_certification']
        gi = request.FILES['gold_image']

        Gold_jewelry.objects.create(gold_category=gcat,gold_name=gna,gold_price=gpr,gold_des_code=gdc,
        gold_gross=gg,gold_net=gne,gold_image=gi,user=user,gold_stone_wt=gsw,gold_gender=ggen,
        gold_metal_colour=gmc)
        msg = "Gold Jewelry Added Successfully"
        return render(request,'gold/add_gold_jewelry.html',{'gcat':gcat,'msg':msg})
    
    else:
        return render(request,'gold/add_gold_jewelry.html')

def view_gold_rings(request):
    user = User.objects.get(email=request.session['email'])
    goldjew = Gold_jewelry.objects.filter(user=user,gold_category="rings")
    return render(request,'gold/view_gold_rings.html',{'goldjew':goldjew})

def view_gold_necklace(request):
    user = User.objects.get(email=request.session['email'])
    goldjew = Gold_jewelry.objects.filter(user=user,gold_category="necklace")
    return render(request,'gold/view_gold_necklace.html',{'goldjew':goldjew})

def view_gold_earrings(request):
    user = User.objects.get(email=request.session['email'])
    goldjew = Gold_jewelry.objects.filter(user=user,gold_category="earrings")
    return render(request,'gold/view_gold_earrings.html',{'goldjew':goldjew})

def view_gold_pendants(request):
    user = User.objects.get(email=request.session['email'])
    goldjew = Gold_jewelry.objects.filter(user=user,gold_category="pendants")
    return render(request,'gold/view_gold_pendants.html',{'goldjew':goldjew})

def view_gold_bangles(request):
    user = User.objects.get(email=request.session['email'])
    goldjew = Gold_jewelry.objects.filter(user=user,gold_category="bangles")
    return render(request,'gold/view_gold_bangles.html',{'goldjew':goldjew})

def view_gold_bracelet(request):
    user = User.objects.get(email=request.session['email'])
    goldjew = Gold_jewelry.objects.filter(user=user,gold_category="bracelet")
    return render(request,'gold/view_gold_bracelet.html',{'goldjew':goldjew})

def view_gold_chains(request):
    user = User.objects.get(email=request.session['email'])
    goldjew = Gold_jewelry.objects.filter(user=user,gold_category="chains")
    return render(request,'gold/view_gold_chains.html',{'goldjew':goldjew})



def add_diamond_jewelry(request):
    if request.method == "POST":

        user = User.objects.get(email=request.session['email'])
        dcat = request.POST['diamond_category']
        dna = request.POST['diamond_name']
        dpr = request.POST['diamond_price']
        ddc = request.POST['diamond_des_code']
        dg = request.POST['diamond_gross']
        dne = request.POST['diamond_net']
        dgen = request.POST['diamond_gender']
        dmc = request.POST['diamond_metal_colour']
        dgpu = request.POST['diamond_gold_purity']
        dgcert = request.POST['diamond_gold_certification']
        dcert = request.POST['diamond_certification']
        di = request.FILES['diamond_image']

        Diamond_jewelry.objects.create(user=user,diamond_category=dcat,diamond_name=dna,diamond_price=dpr,diamond_des_code=ddc,
        diamond_gross=dg,diamond_net=dne,diamond_gender=dgen,diamond_metal_colour=dmc,diamond_image=di)
        msg = "Diamond Jewelry Added Successfully"
        return render(request,'diamond/add_diamond_jewelry.html',{'msg':msg})
    
    else:
        return render(request,'diamond/add_diamond_jewelry.html')

def view_diamond_rings(request):
    user = User.objects.get(email=request.session['email'])
    diajew = Diamond_jewelry.objects.filter(user=user,diamond_category="rings")
    return render(request,'diamond/view_diamond_rings.html',{'diajew':diajew})

def view_diamond_necklace(request):
    user = User.objects.get(email=request.session['email'])
    diajew = Diamond_jewelry.objects.filter(user=user,diamond_category="necklace")
    return render(request,'diamond/view_diamond_necklace.html',{'diajew':diajew})

def view_diamond_earrings(request):
    user = User.objects.get(email=request.session['email'])
    diajew = Diamond_jewelry.objects.filter(user=user,diamond_category="earrings")
    return render(request,'diamond/view_diamond_earrings.html',{'diajew':diajew})

def view_diamond_pendants(request):
    user = User.objects.get(email=request.session['email'])
    diajew = Diamond_jewelry.objects.filter(user=user,diamond_category="pendants")
    return render(request,'diamond/view_diamond_pendants.html',{'diajew':diajew})

def view_diamond_bangles(request):
    user = User.objects.get(email=request.session['email'])
    diajew = Diamond_jewelry.objects.filter(user=user,diamond_category="bangles")
    return render(request,'diamond/view_diamond_bangles.html',{'diajew':diajew})

def view_diamond_bracelet(request):
    user = User.objects.get(email=request.session['email'])
    diajew = Diamond_jewelry.objects.filter(user=user,diamond_category="bracelet")
    return render(request,'diamond/view_diamond_bracelet.html',{'diajew':diajew})



def add_platinum_jewelry(request):
    if request.method == "POST":

        user = User.objects.get(email=request.session['email'])
        pcat = request.POST['platinum_category']
        pna = request.POST['platinum_name']
        ppr = request.POST['platinum_price']
        pdc = request.POST['platinum_des_code']
        pg = request.POST['platinum_gross']
        pne = request.POST['platinum_net']
        pgen = request.POST['platinum_gender']
        pmc = request.POST['platinum_metal_colour']
        ppu = request.POST['platinum_purity']
        pcert = request.POST['platinum_certification']
        pdcert = request.POST['platinum_diamond_certification']
        pi = request.FILES['platinum_image']

        Platinum_jewelry.objects.create(user=user,platinum_category=pcat,platinum_name=pna,platinum_price=ppr,platinum_des_code=pdc,
        platinum_gross=pg,platinum_net=pne,platinum_gender=pgen,platinum_metal_colour=pmc,platinum_image=pi)
        msg = "Platinum Jewelry Added Successfully"
        return render(request,'platinum/add_platinum_jewelry.html',{'msg':msg})
    
    else:
        return render(request,'platinum/add_platinum_jewelry.html')

def view_platinum_rings(request):
    user = User.objects.get(email=request.session['email'])
    ptjew = Platinum_jewelry.objects.filter(user=user,platinum_category="rings")
    return render(request,'platinum/view_platinum_rings.html',{'ptjew':ptjew})

def view_platinum_necklace(request):
    user = User.objects.get(email=request.session['email'])
    ptjew = Platinum_jewelry.objects.filter(user=user,platinum_category="necklace")
    return render(request,'platinum/view_platinum_necklace.html',{'ptjew':ptjew})

def view_platinum_earrings(request):
    user = User.objects.get(email=request.session['email'])
    ptjew = Platinum_jewelry.objects.filter(user=user,platinum_category="earrings")
    return render(request,'platinum/view_platinum_earrings.html',{'ptjew':ptjew})

def view_platinum_pendants(request):
    user = User.objects.get(email=request.session['email'])
    ptjew = Platinum_jewelry.objects.filter(user=user,platinum_category="pendants")
    return render(request,'platinum/view_platinum_pendants.html',{'ptjew':ptjew})

def view_platinum_bracelet(request):
    user = User.objects.get(email=request.session['email'])
    ptjew = Platinum_jewelry.objects.filter(user=user,platinum_category="bracelet")
    return render(request,'platinum/view_platinum_bracelet.html',{'ptjew':ptjew})

def view_platinum_chains(request):
    user = User.objects.get(email=request.session['email'])
    ptjew = Platinum_jewelry.objects.filter(user=user,platinum_category="chains")
    return render(request,'platinum/view_platinum_chains.html',{'ptjew':ptjew})


#Gold details, Stock availability, editing and deleting jewelry 

def gold_product_detail(request,pk):
    gold_jew = Gold_jewelry.objects.get(pk=pk)
    print("Gold Rings : ",gold_jew.gold_gender)
    return render(request,'gold/gold_product_detail.html',{'gold_jew':gold_jew})


def gold_stock_availability(request,pk):
    gold_jew = Gold_jewelry.objects.get(pk=pk)
    print("PK")
    if gold_jew.gold_stock == "Available":
        print("AVAILABLE")
        gold_jew.gold_stock = "Make To Order"
        gold_jew.save()
        return redirect('gold_product_detail',pk)
    else:
        gold_jew.gold_stock = "Available"
        gold_jew.save()
        return redirect('gold_product_detail',pk)

def edit_gold_jewelry(request,pk):
    if request.method == "POST":
        gold_jew = Gold_jewelry.objects.get(pk=pk)
        gold_jew.gold_name = request.POST['gold_name']
        gold_jew.gold_des_code = request.POST['gold_des_code']
        gold_jew.gold_price = request.POST['gold_price']
        gold_jew.gold_gross = request.POST['gold_gross']
        gold_jew.gold_net = request.POST['gold_net']
        gold_jew.gold_stone_wt = request.POST['gold_stone_wt']
        gold_jew.gold_gender = request.POST['gold_gender']
        print(request.POST['gold_gender'])
        gold_jew.gold_metal_colour = request.POST['gold_metal_colour']
        
        try:
            if request.FILES['gold_image']:
                gold_jew.gold_image = request.FILES['gold_image']
                gold_jew.save()
                return redirect('gold_product_detail',pk)
        
        except:
            gold_jew.save()
            return redirect('gold_product_detail',pk)
            
    else:
        gold_jew = Gold_jewelry.objects.get(pk=pk)
        print("pk")
        return render(request,'gold/edit_gold_jewelry.html',{'gold_jew':gold_jew})

def delete_gold_jewelry(request,pk):
    gold_jew = Gold_jewelry.objects.get(pk=pk)
    gold_jew.delete()
    return redirect('seller_index')

#Gold details, Stock availability, editing and deleting jewelry end.........

#Diamond details, Stock availability, editing and deleting jewelry 

def diamond_product_detail(request,pk):
    dia_jew = Diamond_jewelry.objects.get(pk=pk)
    return render(request,'diamond/diamond_product_detail.html',{'dia_jew':dia_jew})


def diamond_stock_availability(request,pk):
    dia_jew = Diamond_jewelry.objects.get(pk=pk)
    print("PK")
    if dia_jew.diamond_stock == "Available":
        print("AVAILABLE")
        dia_jew.diamond_stock = "Make To Order"
        dia_jew.save()
        return redirect('diamond_product_detail',pk)
    else:
        dia_jew.gold_stock = "Available"
        dia_jew.save()
        return redirect('diamond_product_detail',pk)

def edit_diamond_jewelry(request,pk):
    if request.method == "POST":
        dia_jew = Diamond_jewelry.objects.get(pk=pk)
        dia_jew.diamond_name = request.POST['diamond_name']
        dia_jew.diamond_des_code = request.POST['diamond_des_code']
        dia_jew.diamond_price = request.POST['diamond_price']
        dia_jew.diamond_gross = request.POST['diamond_gross']
        dia_jew.diamond_net = request.POST['diamond_net']
        dia_jew.diamond_gender = request.POST['diamond_gender']
        dia_jew.diamond_metal_colour = request.POST['diamond_metal_colour']
        
        try:
            if request.FILES['diamond_image']:
                dia_jew.diamond_image = request.FILES['diamond_image']
                dia_jew.save()
                return redirect('diamond_product_detail',pk)
        
        except:
            dia_jew.save()
            return redirect('diamond_product_detail',pk)
            
    else:
        dia_jew = Diamond_jewelry.objects.get(pk=pk)
        return render(request,'diamond/edit_diamond_jewelry.html',{'dia_jew':dia_jew})

def delete_diamond_jewelry(request,pk):
    dia_jew = Diamond_jewelry.objects.get(pk=pk)
    dia_jew.delete()
    return redirect('seller_index')

#Diamond details, Stock availability, editing and deleting jewelry end.........

#Platinum details, Stock availability, editing and deleting jewelry 

def platinum_product_detail(request,pk):
    pt_jew = Platinum_jewelry.objects.get(pk=pk)
    return render(request,'platinum/platinum_product_detail.html',{'pt_jew':pt_jew})


def platinum_stock_availability(request,pk):
    pt_jew = Platinum_jewelry.objects.get(pk=pk)
    print("PK")
    if pt_jew.platinum_stock == "Available":
        print("AVAILABLE")
        pt_jew.platinum_stock = "Make To Order"
        pt_jew.save()
        return redirect('platinum_product_detail',pk)
    else:
        pt_jew.platinum_stock = "Available"
        pt_jew.save()
        return redirect('platinum_product_detail',pk)

def edit_platinum_jewelry(request,pk):
    if request.method == "POST":
        pt_jew = Platinum_jewelry.objects.get(pk=pk)
        pt_jew.platinum_name = request.POST['platinum_name']
        pt_jew.platinum_des_code = request.POST['platinum_des_code']
        pt_jew.platinum_price = request.POST['platinum_price']
        pt_jew.platinum_gross = request.POST['platinum_gross']
        pt_jew.platinum_net = request.POST['platinum_net']
        pt_jew.platinum_gender = request.POST['platinum_gender']
        pt_jew.platinum_metal_colour = request.POST['platinum_metal_colour']
        
        try:
            if request.FILES['platinum_image']:
                pt_jew.platinum_image = request.FILES['platinum_image']
                pt_jew.save()
                return redirect('platinum_product_detail',pk)
        
        except:
            pt_jew.save()
            return redirect('platinum_product_detail',pk)
            
    else:
        pt_jew = Platinum_jewelry.objects.get(pk=pk)
        return render(request,'platinum/edit_platinum_jewelry.html',{'pt_jew':pt_jew})

def delete_platinum_jewelry(request,pk):
    pt_jew = Platinum_jewelry.objects.get(pk=pk)
    pt_jew.delete()
    return redirect('seller_index')
    
#Platinum details, Stock availability, editing and deleting jewelry end.........

# User view for Gold, Diamond and Platinum Jewelry

def user_view_gold_jew(request,gj):
    goldjew = Gold_jewelry.objects.filter(gold_category__iexact = gj)
    return render(request,'gold/user_view_gold_jew.html',{'goldjew':goldjew})

def user_view_diamond_jew(request,dj):
    diajew = Diamond_jewelry.objects.filter(diamond_category__contains = dj)
    return render(request,'diamond/user_view_diamond_jew.html',{'diajew':diajew})

def user_view_platinum_jew(request,pj):
    ptjew = Platinum_jewelry.objects.filter(platinum_category__contains = pj)
    return render(request,'platinum/user_view_platinum_jew.html',{'ptjew':ptjew})


#User View Gold, Diamond and Platinum Jewelry Details

def user_gold_product_detail(request,pk):
    flag = False
    flag1 = False
    gold_jew = Gold_jewelry.objects.get(pk=pk)
    user = User.objects.get(email=request.session['email'])
    wishlists = Wishlist.objects.filter(user=user,gold_jew=gold_jew)
    carts = Cart.objects.filter(user=user,gold_jew=gold_jew)
    for i in wishlists:
            if i.gold_jew.pk == gold_jew.pk:
                flag = True
                break
    for i in carts:
            if i.gold_jew.pk == gold_jew.pk:
                flag1 = True
                break
    return render(request,'gold/user_gold_product_detail.html',{'gold_jew':gold_jew,'flag':flag,'flag1':flag1})

def user_diamond_product_detail(request,pk):
    flag = False
    flag1 = False
    dia_jew = Diamond_jewelry.objects.get(pk=pk)
    user = User.objects.get(email=request.session['email'])
    wishlists = Wishlist.objects.filter(user=user,dia_jew=dia_jew)
    carts = Cart.objects.filter(user=user,dia_jew=dia_jew)
    for i in wishlists:
            if i.dia_jew.pk == dia_jew.pk:
                flag = True
                break
    for i in carts:
            if i.dia_jew.pk == dia_jew.pk:
                flag1 = True
                break
    return render(request,'diamond/user_diamond_product_detail.html',{'dia_jew':dia_jew,'flag':flag,'flag1':flag1})

def user_platinum_product_detail(request,pk):
    flag = False
    flag1 = False
    pt_jew = Platinum_jewelry.objects.get(pk=pk)
    user = User.objects.get(email=request.session['email'])
    wishlists = Wishlist.objects.filter(user=user,pt_jew=pt_jew)
    carts = Cart.objects.filter(user=user,pt_jew=pt_jew)
    for i in wishlists:
            if i.pt_jew.pk == pt_jew.pk:
                flag = True
                break
    for i in carts:
            if i.pt_jew.pk == pt_jew.pk:
                flag1 = True
                break
    return render(request,'platinum/user_platinum_product_detail.html',{'pt_jew':pt_jew,'flag':flag,'flag1':flag1})



def add_to_wishlist(request,pk,a):
    user = User.objects.get(email=request.session['email'])
    if a == "gj":
        gold_jew = Gold_jewelry.objects.get(pk=pk)
        Wishlist.objects.create(user=user,gold_jew=gold_jew)
    elif a == "dj":
        dia_jew = Diamond_jewelry.objects.get(pk=pk)
        Wishlist.objects.create(user=user,dia_jew=dia_jew)  
    elif a == "pj":
        pt_jew = Platinum_jewelry.objects.get(pk=pk)
        Wishlist.objects.create(user=user,pt_jew=pt_jew)
    return redirect('mywishlist')

def remove_from_wishlist(request,pk,c):
    user = User.objects.get(email=request.session['email'])
    if c == "gj":
        gold_jew = Gold_jewelry.objects.get(pk=pk)
        wishlist = Wishlist.objects.get(user=user,gold_jew=gold_jew)
        wishlist.delete()
    elif c == "dj":
        dia_jew = Diamond_jewelry.objects.get(pk=pk)
        wishlist = Wishlist.objects.get(user=user,dia_jew=dia_jew)
        wishlist.delete()
    elif c == "pj":
        pt_jew = Platinum_jewelry.objects.get(pk=pk)
        wishlist = Wishlist.objects.get(user=user,pt_jew=pt_jew)
        wishlist.delete()
    return redirect('mywishlist')

def mywishlist(request):
    user = User.objects.get(email=request.session['email'])
    request.session['user_image'] = user.user_image.url
    wishlists = Wishlist.objects.filter(user=user)
    request.session['total_wishlist']=len(wishlists)
    return render(request,'mywishlist.html',{'wishlists':wishlists,'user':user})



def add_to_cart(request,pk,b):
    user = User.objects.get(email=request.session['email'])
    if b == "gj":
        gold_jew = Gold_jewelry.objects.get(pk=pk)
        Cart.objects.create(user=user,gold_jew=gold_jew,total_price=gold_jew.gold_price,total_qty=1)
    elif b == "dj":
        dia_jew = Diamond_jewelry.objects.get(pk=pk)
        Cart.objects.create(user=user,dia_jew=dia_jew,total_price=dia_jew.diamond_price,total_qty=1)
    elif b == "pj":
        pt_jew = Platinum_jewelry.objects.get(pk=pk)
        Cart.objects.create(user=user,pt_jew=pt_jew,total_price=pt_jew.platinum_price,total_qty=1)
    return redirect('mycart')

def remove_from_cart(request,pk,d):
    user = User.objects.get(email=request.session['email'])
    if d == "gj":
        gold_jew = Gold_jewelry.objects.get(pk=pk)
        cart = Cart.objects.get(user=user,gold_jew=gold_jew)
        cart.delete()
    elif d == "dj":
        dia_jew = Diamond_jewelry.objects.get(pk=pk)
        cart = Cart.objects.get(user=user,dia_jew=dia_jew)
        cart.delete()  
    elif d == "pj":
        pt_jew = Platinum_jewelry.objects.get(pk=pk)
        cart = Cart.objects.get(user=user,pt_jew=pt_jew)
        cart.delete()
    return redirect('mycart')

def mycart(request):
    net_price = 0
    user = User.objects.get(email=request.session['email'])
    request.session['user_image'] = user.user_image.url
    carts = Cart.objects.filter(user=user)
    for i in carts:
        net_price = net_price+i.total_price
    request.session['total_cart']=len(carts)
    return render(request,'mycart.html',{'carts':carts,'net_price':net_price,'user':user})

def move_to_cart(request,pk,f):
    user = User.objects.get(email=request.session['email'])
    if f == "gj":
        gold_jew = Gold_jewelry.objects.get(pk=pk)
        Cart.objects.create(user=user,gold_jew=gold_jew,total_price=gold_jew.gold_price,total_qty=1)
        wishlist = Wishlist.objects.get(user=user,gold_jew=gold_jew)
        wishlist.delete()
        wishlists = Wishlist.objects.filter(user=user)
        request.session['total_wishlist']=len(wishlists)
    elif f == "dj":
        dia_jew = Diamond_jewelry.objects.get(pk=pk)
        Cart.objects.create(user=user,dia_jew=dia_jew,total_price=dia_jew.diamond_price,total_qty=1)
        wishlist = Wishlist.objects.get(user=user,dia_jew=dia_jew)
        wishlist.delete()
        wishlists = Wishlist.objects.filter(user=user)
        request.session['total_wishlist']=len(wishlists)
    elif f == "pj":
        pt_jew = Platinum_jewelry.objects.get(pk=pk)
        Cart.objects.create(user=user,pt_jew=pt_jew,total_price=pt_jew.platinum_price,total_qty=1)
        wishlist = Wishlist.objects.get(user=user,pt_jew=pt_jew)
        wishlist.delete()
        wishlists = Wishlist.objects.filter(user=user)
        request.session['total_wishlist']=len(wishlists)
    return redirect('mycart')

def move_to_wishlist(request,pk,e):
    user = User.objects.get(email=request.session['email'])
    if e == "gj":
        gold_jew = Gold_jewelry.objects.get(pk=pk)
        Wishlist.objects.create(user=user,gold_jew=gold_jew)
        cart = Cart.objects.get(user=user,gold_jew=gold_jew)
        cart.delete()
        carts = Cart.objects.filter(user=user)
        request.session['total_cart']=len(carts)
    elif e == "dj":
        dia_jew = Diamond_jewelry.objects.get(pk=pk)
        Wishlist.objects.create(user=user,dia_jew=dia_jew)
        cart = Cart.objects.get(user=user,dia_jew=dia_jew)
        cart.delete()
        carts = Cart.objects.filter(user=user)
        request.session['total_cart']=len(carts)
    elif e == "pj":
        pt_jew = Platinum_jewelry.objects.get(pk=pk)
        Wishlist.objects.create(user=user,pt_jew=pt_jew)
        cart = Cart.objects.get(user=user,pt_jew=pt_jew)
        cart.delete()
        carts = Cart.objects.filter(user=user)
        request.session['total_cart']=len(carts)
    return redirect('mywishlist')

def update_price(request):
    price = request.POST['price']
    qty = request.POST['qty']
    pk = request.POST['pk']

    cart = Cart.objects.get(pk=pk)
    total_price = int(price)*int(qty)
    cart.total_price=total_price
    cart.total_qty=qty
    cart.save()
    return redirect('mycart')
