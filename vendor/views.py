from django.shortcuts import redirect, render
from .models import otp, vendor, address, company
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import random, math, string
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/vendor/login/')
def home(request):
    try:
        ven = vendor.objects.get(user=request.user)
        try:
            com = company.objects.get(vendor=ven)
            return redirect("verifysite")
        except:
            return redirect("verifyaccount")
    except:
        return render(request, "verification.html")

def check_username(request):
    try:
        username = request.GET.get("username")
        user = User.objects.get(username=username)
        return HttpResponse("False")
    except:
        return HttpResponse("True")

def send_email(request):
    email = request.GET.get("email")
    try:
        user = User.objects.get(email=email)
        return HttpResponse("failed")
    except:
        otp.objects.filter(email=email).delete()
        digits = [i for i in range(0, 10)]
        random_str = ""
        for i in range(6):
            index = math.floor(random.random() * 10)
            random_str += str(digits[index])
        random_str = int(random_str)

        send_otp = otp(email=email, otp=random_str)
        send_mail('Email verification for HopON','Thanks for you interest in HopON.'+ '\n\nYour OTP is '+ str(random_str) , settings.EMAIL_HOST_USER,  [email])

        send_otp.save()
        
        return HttpResponse("success")

def verify_email(request):
    email = request.GET.get("email")
    incoming_otp = request.GET.get("otp")

    try:
        db_otp = otp.objects.get(email=email, otp=int(incoming_otp))
        return HttpResponse("success")
    except Exception as e:

        return HttpResponse("failed")

def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {"message": "Invalid Credentials!"})
    else:
        return render(request, "login.html")

def logout(request):
    auth_logout(request)
    return redirect("home")

def signup(request):
    if request.method == "POST":
        try:
            userform = User(username=request.POST["username"], first_name=request.POST["firstname"], last_name=request.POST["lastname"],
                        password=make_password(request.POST['password']), email=request.POST["email"])
            userform.save()
            return HttpResponse("success")
        except Exception as e:
            return HttpResponse("failed")

    if request.user.is_authenticated:
        auth_logout(request)
    
    return render(request, "signup.html")


def forgot(request):
    if request.method == "POST":
        try:
            email = request.POST["email"]
            user = User.objects.get(email=email)
            temp_pass = id_generator()
            send_mail('Reset Password for HopON','Thanks for you reaching out to HopON.'+ '\n\nYour Username is '+ str(user.username) +". \nYour temporary password is: "
                        + str(temp_pass)+". \n Please rest your password soon after login.", settings.EMAIL_HOST_USER,  [email])

            user.password = make_password(temp_pass)
            user.save()

            return redirect("login")
        except:
            pass

    return render(request, "forgot.html")

def id_generator(size=8, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def chngpwd(request):
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        if request.method == "POST":
            errors = []
            if request.POST["password"] == request.POST["old_password"]:
                errors.append("Please do not user previous password.")
            if request.POST["password"] != request.POST["confirm_password"]:
                errors.append("Please confirm password correctly.")
            if not errors:
                try:
                    a = authenticate(request, username=request.user, password=request.POST["password"])
                    if a:
                        user = User.objects.get(username=request.user)
                        user.set_password(request.POST["password"])
                        user.save()
                        auth_logout(request)
                except Exception as e:
                    errors.append("Please enter correct password")
                if errors:
                    return render(request, "chngpwd.html", {"errors": errors})
                else:
                    return redirect("login")
            
    return render(request, "chngpwd.html")

@login_required(login_url='/vendor/login/')
def verifyaccount(request):
    if request.method == "POST":
        dob = datefilter_converter(request.POST["dob"])
        aadhar_number = request.POST["aadhar"]
        phone = request.POST["phone"]
        adrs = request.POST["address"]
        city = request.POST["city"]
        state = request.POST["state"]
        pincode = request.POST["pincode"]

        try:
            add = address(line1=adrs, city=city, state=state, pincode=pincode)
            add.save()
        except:
            print("Error in creating Address")
        if add:
            try:
                ven = vendor(user=request.user, birth_date=dob, phone=phone,aadhar_number=aadhar_number,address=add,
                                aadhar_front=request.FILES["aadhar_frontimg"],aadhar_back=request.FILES["aadhar_backimg"],status=1)
                ven.save()
                send_mail('Account verification request recieved','Thanks for enrolling with HopON.'+ '\n\nAccount user name: '+ str(ven.user) +". \nWe will notify once we made our decision. ", settings.EMAIL_HOST_USER,  [ven.user.email])
                send_mail('Account verification request: '+str(ven.user),'Hi Admin,'+ '\n\nPlease verify our new account for vendor. \nAccount user name: '+ str(ven.user) +". \n Url: localhost/admin/vendor/"+ str(ven.id) +"/change/", settings.EMAIL_HOST_USER,  [settings.EMAIL_HOST_USER])
            except:
                print("Error in creating vendor")

        return redirect("verifyaccount")
    else:
        try:
            ven = vendor.objects.get(user=request.user)
            return render(request, "verification.html", {"vendor": ven})
        except:
            print("No vendor for this user")
            return render(request, "verification.html")

def datefilter_converter(date):
    if date:
        return(date[-4:]+'-'+date[3:5]+'-'+date[:2])
    else:
        return None

def verifysite(request):
    if request.method == "POST":
        company_name = request.POST["company_name"]
        cars = request.POST["Num_Cars"]
        adrs = request.POST["address"]
        city = request.POST["city"]
        state = request.POST["state"]
        pincode = request.POST["pincode"]

        try:
            add = address(line1=adrs, city=city, state=state, pincode=pincode)
            add.save()
            ven = vendor.objects.get(user=request.user)
        except:
            print("Error in creating Address")

        if add:
            try:
                site = company(vendor=ven, name=company_name, cars=cars, address=add,site_docFront = request.FILES["document_frontimg"], 
                                site_docBack=request.FILES["document_backimg"], status=1)
                site.save()
                send_mail('Site verification request recieved','Thanks for enrolling your site with HopON.'+ '\n\nAccount user name: '+ str(ven.user) +".\n Company name:"+ str(company_name)+" \nWe will notify once we made our decision. ", settings.EMAIL_HOST_USER,  [ven.user.email])
                send_mail('Site verification request: '+str(ven.user),'Hi Admin,'+ '\n\nPlease verify our new site for vendor. \nAccount user name: '+ str(ven.user) + ".\n Company name:"+ str(company_name)+". \n Url: localhost/admin/site/"+ str(site.id) +"/change/", settings.EMAIL_HOST_USER,  [settings.EMAIL_HOST_USER])
            except:
                print("Error in creating Site")

        return redirect("verifysite")

    try:
        ven = vendor.objects.get(user=request.user)
        try:
            site = company.objects.get(vendor=ven)
            return render(request, "verifysite.html", {"company": site})
        except:
            if ven.status == "2":
                return render(request, "verifysite.html")
            else:
                return redirect("verifyaccount")
    except:
        return redirect("verifyaccount")