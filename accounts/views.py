from django.core.checks import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.mail import send_mail,BadHeaderError
from django.http import HttpResponse
import hashlib
def texttosha1(str):
    result = hashlib.sha1(str.encode())
    return(result.hexdigest())

value=""
global i
i=0
global usernam 
usernam="NULL"
global maill
# Create your views here.
def register(request):
    if request.method=='POST':
        first_name=request.POST['Full Name']
        username=request.POST['username']
        email=request.POST['email']
        lastname=request.POST['Last_nme']
        password1=request.POST['password']
        password2=request.POST['confirm_password']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:
                msg=texttosha1(password1)
                user= User.objects.create_user(username=username,last_name=lastname,first_name=first_name,password=msg,email=email)
                user.save();
                messages.info(request,"You have sucessfully registered yourself")
                return redirect('/')
                
        else:
            messages.info(request,'Password not Matching')
            return redirect('register')
        


    else:
        
        return render(request, 'signup.html')

def login(request):

    # If the user wants to visit the login page
    if request.method == 'GET':
        return render(request, 'login.html')

    # If the user wants to login by entering username and password
    else:
        USERNAME = request.POST['username']
        request.session['username'] = USERNAME
        pass1 = request.POST['password']
        uss=USERNAME;
        global maill
        pass1=texttosha1(pass1)
        user = auth.authenticate(username=USERNAME, password=pass1)
        if user is not None:
            x = User.objects.get(username=uss) 
            global value
            global i
            i=0
            global name
            maill=x.email
            global usernam 
            usernam=USERNAME 
            name=x.first_name
            value=x.last_name
            print(x.last_name)
            if value=="NULL":
            
                messages.info(request,"This account is locked you cannot login! You must have gotten an email for unlocking")
                n=None
                return redirect('/')
            else:
            # Checks if the user is a valid user stored in the database
            
            # If user is found, redirect to further page for the image authentication
                if user is not None:
                    
                    return redirect('/accounts/authenticate')

                # If user is not found, then redirected to login page with error message
                else:
                    
                    print('login error')
                    messages.info(
                        request, 'Invalid credentials! Please try again', extra_tags='login_error')
                    return redirect('/accounts/login')
        else:
        # Checks if the user is a valid user stored in the database
        
        # If user is found, redirect to further page for the image authentication
            if user is not None:
                
                return redirect('/accounts/authenticate')

            # If user is not found, then redirected to login page with error message
            else:
                
                print('login error')
                messages.info(
                    request, 'Invalid credentials! Please try again', extra_tags='login_error')
                return redirect('/accounts/login')
def authenticate(request):
    return render(request,'authenticate.html')
def image_authenticate(request):
    global value
    global i
    global name
    global maill
    i=i+1
    
    if request.method == 'POST':
        Last_name= request.POST['Last_nme']
        global usernam
        u = User.objects.get(username=usernam)
        
        if i<3:
                if Last_name==value:
                    print(value,Last_name)
                    messages.info(request,"Hello "+ name +" You are Logged in Sucessfully")
                    return redirect('/')
                if value!=Last_name :
                    print(i)
                    messages.info(request,'Incorrect   Sequence '+ str(i) + '/3 chances')
                    return redirect('authenticate') 
        else:
                # messages.info(request,'Your account has been locked we have sent a reset link on your mail')
                # return redirect('authenticate')
                u = User.objects.get(username=usernam)
                u.last_name="NULL"
                u.save()
                try:
                    print(maill)
                    send_mail(
                    'LINK FOR UNLOCKING YOUR ACCOUNT',
                    'REDIRECT TO THIS LINK FOR FURTHER PROCESSING  http://127.0.0.1:8000/accounts/reauthen',
                    'resetsource404@gmail.com',
                    [maill],
                    fail_silently=False,
                )
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
            
                messages.info(request,"Your account has been lockout we have sent a reset link on your mail")
                return redirect('/')
        
    else:
            return redirect('/accounts/login')
    

def reauthen(request):
    return render(request,'reauthen.html')
def update(request):
    
    if request.method == 'POST':
        USERNAME = request.POST['username']
        if USERNAME!="NULL":
            lastname=request.POST['Last_nme']
            u = User.objects.get(username=USERNAME)
            u.last_name=lastname
            u.save()
            messages.info(request,"You have sucessfully changed your info")
                    
            return redirect('/')
        else:
            messages.info(request,"Unauthorized Access")
                    
            return redirect('/')
    else:
        return redirect('/')

